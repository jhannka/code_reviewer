import os
import sys
import threading
import time
from google.adk.agents.llm_agent import Agent
from google.genai import types
from dotenv import load_dotenv

# Cargar variables del .env
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)

# Importar capas de arquitectura hexagonal
from code_reviewer.adapters.driven.git_vcs import GitVCSAdapter
from code_reviewer.adapters.driven.local_fs import LocalFileSystemAdapter
from code_reviewer.adapters.driven.local_skills import LocalSkillsRepositoryAdapter
from code_reviewer.adapters.driven.pytest_runner import PytestRunnerAdapter
from code_reviewer.domain.use_cases import CodeReviewToolsService
from code_reviewer.adapters.driving.tool_facade import (
    configure_facade,
    read_project_skills,
    get_git_changes,
    read_source_file,
    write_source_file,
    execute_unit_tests
)

# Inicializar y cablear la arquitectura hexagonal
vcs_adapter = GitVCSAdapter()
fs_adapter = LocalFileSystemAdapter()
skills_adapter = LocalSkillsRepositoryAdapter()
test_runner_adapter = PytestRunnerAdapter()

service = CodeReviewToolsService(
    vcs_port=vcs_adapter,
    fs_port=fs_adapter,
    skills_port=skills_adapter,
    test_runner_port=test_runner_adapter
)

configure_facade(service)

# Leer modelo de las variables de entorno (por defecto gemini-3.5-flash)
model_name = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

# Cargar configuración de veracidad y mapear a temperatura de LLM
veracity = os.getenv("REVIEW_VERACITY", "strict").strip().lower()
temp_map = {"strict": 0.0, "balanced": 0.4, "creative": 0.7}
temp_val = temp_map.get(veracity, 0.0)
gen_config = types.GenerateContentConfig(temperature=temp_val)

# --- Callbacks de progreso para agentes ---

class SpinnerThread(threading.Thread):
    def __init__(self, message: str):
        super().__init__()
        self.message = message
        self.stop_event = threading.Event()
        self.daemon = True

    def run(self):
        chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        idx = 0
        while not self.stop_event.is_set():
            sys.stdout.write(f"\r{chars[idx]} {self.message}")
            sys.stdout.flush()
            idx = (idx + 1) % len(chars)
            time.sleep(0.1)
        sys.stdout.write("\r\033[K")
        sys.stdout.flush()

_spinner = None
_spinner_lock = threading.Lock()

def before_agent(callback_context):
    global _spinner
    agent_name = callback_context.agent_name
    if agent_name == "coordinator_agent":
        return None
    with _spinner_lock:
        if _spinner is None:
            _spinner = SpinnerThread(f"Running specialized agent '{agent_name}'...")
            _spinner.start()
    return None

def after_agent(callback_context):
    global _spinner
    agent_name = callback_context.agent_name
    if agent_name == "coordinator_agent":
        return None
    with _spinner_lock:
        if _spinner is not None:
            _spinner.stop_event.set()
            _spinner.join()
            _spinner = None
    sys.stdout.write(f"✅ Completed specialized agent '{agent_name}'\n")
    sys.stdout.flush()
    return None

# --- Definición de Agentes Especializados (Pipeline Inverso para permitir transferencias) ---

# 6. Agente Ejecutor de Tests
test_executor = Agent(
    model=model_name,
    name='test_executor',
    description='Agente especializado en ejecutar pruebas unitarias del proyecto.',
    instruction='Tu única tarea es ejecutar las pruebas unitarias usando la herramienta "execute_unit_tests" e informar si pasaron o fallaron de manera exacta y concisa. Una vez termines, devuelve el reporte final.',
    tools=[execute_unit_tests],
    before_agent_callback=before_agent,
    after_agent_callback=after_agent,
    generate_content_config=gen_config
)

# 5. Agente Aplicador de Cambios
change_applier = Agent(
    model=model_name,
    name='change_applier',
    description='Agente especializado en aplicar las modificaciones de código aprobadas.',
    instruction='Tu única tarea es aplicar los cambios de código aprobados usando "write_source_file". Si existe un Plan de Refactorización Incremental provisto por el refactoring_advisor, debes aplicar las correcciones paso a paso, deteniéndose en cada paso para que el test_executor valide el cambio antes de continuar. Al finalizar tus cambios, transfiere obligatoriamente el control al "test_executor".',
    tools=[write_source_file],
    sub_agents=[test_executor],
    before_agent_callback=before_agent,
    after_agent_callback=after_agent,
    generate_content_config=gen_config
)

# 4. Agente Propositor de Refactorización
refactoring_advisor = Agent(
    model=model_name,
    name='refactoring_advisor',
    description='Agente especializado en diseñar propuestas de refactorización y planes incrementales.',
    instruction='Tu única tarea es proponer mejoras y refactorizaciones basadas en el reporte de discrepancias. Si los cambios propuestos son extensivos (más de 50 líneas de código en total o afectan a múltiples módulos), debes diseñar obligatoriamente un Plan de Refactorización Incremental paso a paso. Si el cambio es menor, entrega el código corregido directamente. IMPORTANTÍSIMO: Muestra la propuesta final al usuario y ESPERA SU CONFIRMACIÓN antes de usar tu herramienta para transferir el control a "change_applier".',
    tools=[read_source_file],
    sub_agents=[change_applier],
    before_agent_callback=before_agent,
    after_agent_callback=after_agent,
    generate_content_config=gen_config
)

# 3. Agente Analizador de Errores
error_analyzer = Agent(
    model=model_name,
    name='error_analyzer',
    description='Agente especializado en identificar discrepancias de codificación y asegurar su veracidad.',
    instruction='Tu única tarea es analizar el código fuente provisto comparándolo minuciosamente contra las directivas de diseño (skills) obtenidas. Identifica bugs, problemas de legibilidad y desviaciones arquitectónicas. Realiza un chequeo estricto de la veracidad y exactitud técnica de los errores. Entrega un informe de discrepancias detallado y AL TERMINAR TRANSFIERE INMEDIATAMENTE EL CONTROL AL AGENTE "refactoring_advisor" pasándole tu reporte.',
    tools=[read_source_file],
    sub_agents=[refactoring_advisor],
    before_agent_callback=before_agent,
    after_agent_callback=after_agent,
    generate_content_config=gen_config
)

# 2. Agente Buscador de Cambios
change_finder = Agent(
    model=model_name,
    name='change_finder',
    description='Agente especializado en buscar cambios de código pendientes en git o leer archivos específicos.',
    instruction='Tu única tarea es identificar los cambios pendientes en el repositorio de Git usando "get_git_changes" o leer un archivo de código específico con "read_source_file" si te pasan una ruta. Entrega el código fuente actual o el diff de cambios. AL TERMINAR, DEBES TRANSFERIR INMEDIATAMENTE EL CONTROL AL AGENTE "error_analyzer" pasándole los cambios que encontraste y el resumen de skills.',
    tools=[get_git_changes, read_source_file],
    sub_agents=[error_analyzer],
    before_agent_callback=before_agent,
    after_agent_callback=after_agent,
    generate_content_config=gen_config
)

# 1. Agente Explorador de Skills
skills_explorer = Agent(
    model=model_name,
    name='skills_explorer',
    description='Agente especializado en leer y resumir las directivas y skills de diseño del proyecto.',
    instruction='Tu única tarea es leer y extraer todas las skills y directivas de diseño del proyecto usando la herramienta "read_project_skills". Entrega un informe consolidado con estas guías. AL TERMINAR, DEBES TRANSFERIR INMEDIATAMENTE EL CONTROL AL AGENTE "change_finder" para que proceda con su tarea.',
    tools=[read_project_skills],
    sub_agents=[change_finder],
    before_agent_callback=before_agent,
    after_agent_callback=after_agent,
    generate_content_config=gen_config
)

# Agente Coordinador Central (Root Agent)
coordinator_instruction = """
Eres el Agente Coordinador del proceso de revisión de código. Tu única misión es INICIAR el flujo de revisión transfiriendo inmediatamente el control al agente 'skills_explorer' pasándole la petición del usuario.
El flujo continuará secuencialmente entre ellos. NO HAGAS NADA MÁS QUE INVOCAR AL PRIMER AGENTE.
"""

root_agent = Agent(
    model=model_name,
    name='coordinator_agent',
    description='Agente Coordinador que orquesta el proceso de revisión de código secuencial usando sub-agentes.',
    instruction=coordinator_instruction,
    sub_agents=[
        skills_explorer
    ],
    generate_content_config=gen_config
)
