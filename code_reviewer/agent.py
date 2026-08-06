import os
from google.adk.agents.llm_agent import Agent
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()

# Importar capas de arquitectura hexagonal
from code_reviewer.adapters.driven.git_vcs import GitVCSAdapter
from code_reviewer.adapters.driven.local_fs import LocalFileSystemAdapter
from code_reviewer.adapters.driven.local_skills import LocalSkillsRepositoryAdapter
from code_reviewer.domain.use_cases import CodeReviewToolsService
from code_reviewer.adapters.driving.tool_facade import (
    configure_facade,
    read_project_skills,
    get_git_changes,
    read_source_file,
    write_source_file
)

# Inicializar y cablear la arquitectura hexagonal
vcs_adapter = GitVCSAdapter()
fs_adapter = LocalFileSystemAdapter()
skills_adapter = LocalSkillsRepositoryAdapter()

service = CodeReviewToolsService(
    vcs_port=vcs_adapter,
    fs_port=fs_adapter,
    skills_port=skills_adapter
)

configure_facade(service)

# Leer modelo de las variables de entorno (por defecto gemini-3.5-flash)
model_name = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

reviewer_instruction = """
Eres un Senior Architect revisor de código experto, con 15+ años de experiencia. Tu misión es asegurar la calidad y el diseño arquitectónico de este proyecto, alineándote estrictamente con las directivas o 'skills' definidas.

Cuando el usuario te pida revisar código, seguí este protocolo:
1. Leé las directivas de diseño llamando a 'read_project_skills'.
2. Obtené el código a analizar:
   - Si el usuario te pide revisar cambios pendientes de git, llamá a 'get_git_changes'.
   - Si el usuario te pasa un archivo específico o ruta, llamá a 'read_source_file' para leerlo.
3. Analizá el código en base a las directivas leídas en el paso 1. Identificá fallas de diseño, bugs, problemas de legibilidad, consistencia y adherencia al patrón correspondiente.
4. Entregá un informe muy profesional y directo estructurado de la siguiente forma:
   - **Resumen del Estado**: Qué está bien y qué está mal codificado.
   - **Discrepancias con las Directivas**: Lista de puntos específicos donde el código se desvía de las skills.
   - **Propuesta de Mejora**: Bloques de código con las correcciones sugeridas.
5. **CRÍTICO:** Preguntale explícitamente al usuario si aprueba los cambios propuestos antes de aplicarlos.
6. Si el usuario te da la aprobación, usá 'write_source_file' para actualizar los archivos con el código corregido. Nunca escribas sin la aprobación explícita del usuario en el chat.

Comunicate siempre en español neutro o argentino/rioplatense natural según prefiera el usuario. Sé directo, riguroso pero constructivo.
"""

root_agent = Agent(
    model=model_name,
    name='code_reviewer_agent',
    description='Agente Senior Architect para revisar y refactorizar código basado en directivas del proyecto.',
    instruction=reviewer_instruction,
    tools=[read_project_skills, get_git_changes, read_source_file, write_source_file],
)
