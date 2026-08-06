import os
import sys
import threading
import time
from google.adk.agents.llm_agent import Agent
from google.genai import types
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()

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

# Leer modelo de las variables de entorno (por defecto gemini-2.5-flash)
model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

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

# --- Definicón de Agentes Especializados ---

# 1. Agente Explorador de Skills
skills_explorer = Agent(
    model=model_name,
    name='skills_explorer',
    description='Agente especializado en leer y resumir las directivas y skills de diseño del proyecto.',
    instruction='Tu única tarea es leer y extraer todas las skills y directivas de diseño del proyecto usando la herramienta "read_project_skills". Entrega un informe consolidado con estas guías.',
    tools=[read_project_skills],
    before_agent_callback=before_agent,
    after_agent_callback=after_agent,
    generate_content_config=gen_config
)

# 2. Agente Buscador de Cambios
change_finder = Agent(
    model=model_name,
    name='change_finder',
    description='Agente especializado en buscar cambios de código pendientes en git o leer archivos específicos.',
    instruction='Tu única tarea es identificar los cambios pendientes en el repositorio de Git usando "get_git_changes" o leer un archivo de código específico con "read_source_file" si te pasan una ruta. Entrega el código fuente actual o el diff de cambios.',
    tools=[get_git_changes, read_source_file],
    before_agent_callback=before_agent,
    after_agent_callback=after_agent,
    generate_content_config=gen_config
)

# 3. Agente Analizador de Errores
error_analyzer = Agent(
    model=model_name,
    name='error_analyzer',
    description='Agente especializado en identificar discrepancias de codificación y asegurar su veracidad.',
    instruction='Tu única tarea es analizar el código fuente provisto comparándolo minuciosamente contra las directivas de diseño (skills) obtenidas. Identifica bugs, problemas de legibilidad y desviaciones arquitectónicas. Realiza un chequeo estricto de la veracidad y exactitud técnica de los errores. Entrega un informe de discrepancias detallado.',
    tools=[read_source_file],
    before_agent_callback=before_agent,
    after_agent_callback=after_agent,
    generate_content_config=gen_config
)

# 4. Agente Propositor de Refactorización
refactoring_advisor = Agent(
    model=model_name,
    name='refactoring_advisor',
    description='Agente especializado en diseñar propuestas de refactorización y planes incrementales.',
    instruction='Tu única tarea es proponer mejoras y refactorizaciones basadas en el reporte de discrepancias. Si los cambios propuestos son extensivos (más de 50 líneas de código en total o afectan a múltiples módulos), debes diseñar obligatoriamente un Plan de Refactorización Incremental paso a paso, de modo que cada paso sea verificable de forma aislada corriendo los tests. Si el cambio es menor, entrega el código corregido directamente.',
    tools=[read_source_file],
    before_agent_callback=before_agent,
    after_agent_callback=after_agent,
    generate_content_config=gen_config
)

# 5. Agente Aplicador de Cambios
change_applier = Agent(
    model=model_name,
    name='change_applier',
    description='Agente especializado en aplicar las modificaciones de código aprobadas.',
    instruction='Tu única tarea es aplicar los cambios de código aprobados usando "write_source_file". Si existe un Plan de Refactorización Incremental provisto por el refactoring_advisor, debes aplicar las correcciones paso a paso, deteniéndose en cada paso para que el test_executor valide el cambio antes de continuar.',
    tools=[write_source_file],
    before_agent_callback=before_agent,
    after_agent_callback=after_agent,
    generate_content_config=gen_config
)

# 6. Agente Ejecutor de Tests
test_executor = Agent(
    model=model_name,
    name='test_executor',
    description='Agente especializado en ejecutar pruebas unitarias del proyecto.',
    instruction='Tu única tarea es ejecutar las pruebas unitarias usando la herramienta "execute_unit_tests" e informar si pasaron o fallaron de manera exacta y concisa.',
    tools=[execute_unit_tests],
    before_agent_callback=before_agent,
    after_agent_callback=after_agent,
    generate_content_config=gen_config
)

# Agente Coordinador Central (Root Agent)
coordinator_instruction = """
Eres el Agente Coordinador del proceso de revisión de código. Tu misión es guiar la revisión secuencialmente, asegurando que se cumplan las tareas al 100% sin olvidar nada.
Debes delegar las tareas a los siguientes sub-agentes en este orden exacto:

1. 'skills_explorer': Para leer las directivas (skills) del proyecto.
2. 'change_finder': Para obtener los cambios de Git o leer archivos específicos.
3. 'error_analyzer': Para identificar desviaciones y errores técnicos con veracidad.
4. 'refactoring_advisor': Para generar la propuesta de refactorización y el plan incremental si los cambios son extensos (>50 líneas).
5. 'change_applier': Para escribir las modificaciones aprobadas.
6. 'test_executor': Para ejecutar la suite de pruebas unitarias.

Reglas del Proceso:
- Ejecuta los agentes estrictamente del 1 al 6. No te saltees pasos ni asumas resultados.
- Después de la propuesta de 'refactoring_advisor', detente para presentar el informe de discrepancias y la propuesta al usuario, y pídele confirmación antes de delegar a 'change_applier'.
- Comunicate siempre en español neutro o argentino/rioplatense natural. Sé directo y riguroso.
"""

root_agent = Agent(
    model=model_name,
    name='coordinator_agent',
    description='Agente Coordinador que orquesta el proceso de revisión de código secuencial usando sub-agentes.',
    instruction=coordinator_instruction,
    sub_agents=[
        skills_explorer,
        change_finder,
        error_analyzer,
        refactoring_advisor,
        change_applier,
        test_executor
    ],
    generate_content_config=gen_config
)
