# Code Reviewer Agent (Hexagonal Architecture)

Un agente de revisión de código interactivo basado en la terminal, diseñado con **Google ADK (Agent Development Kit)** y estructurado bajo **Arquitectura Hexagonal**. El agente inspecciona cambios de Git y archivos del proyecto para verificar la adherencia a directivas de diseño (skills) y proponer refactorizaciones seguras.

---

## Quick path

1. **Instalar dependencias**:
   ```bash
   python3 -m venv .venv
   .venv/bin/pip install google-adk python-dotenv pytest
   npm install
   ```
2. **Configurar variables**:
   Copia el archivo de plantilla y configúralo con tu clave de API de Gemini:
   ```bash
   cp code_reviewer/.env.example code_reviewer/.env
   # Edita code_reviewer/.env y añade tu GOOGLE_API_KEY
   ```
3. **Ejecutar el menú**:
   ```bash
   npm run menu   # O alternativamente: python3 menu.py
   ```
4. **Verificar tests**:
   ```bash
   PYTHONPATH=.:code_reviewer .venv/bin/pytest
   ```

---

## Details

| Componente | Rol en la Arquitectura Hexagonal |
|------------|-----------------------------------|
| **`code_reviewer/domain`** | Contiene la lógica de dominio pura (`CodeReviewToolsService`), totalmente aislada de la infraestructura. |
| **`code_reviewer/ports`** | Define los contratos de entrada (Driving) y salida (Driven) del sistema. |
| **`code_reviewer/adapters`** | Implementaciones concretas de la infraestructura (Git VCS, Local FileSystem, Carga dinámica de Skills desde el Home del usuario). |
| **`code_reviewer/agent.py`** | Punto de composición raíz que conecta los adaptadores con el dominio y declara el `root_agent` de ADK. |
| **`menu.py`** | Interfaz CLI interactiva que orquesta las consultas al agente ADK. |

---

## Checklist de Verificación

- [ ] Las pruebas unitarias pasan con éxito en el entorno local (`5/5 passed`).
- [ ] El archivo `code_reviewer/.env` contiene una clave API de Gemini válida.
- [ ] El comando `python3 menu.py` levanta el menú sin errores de importación de módulos.
- [ ] El agente lee dinámicamente las directivas de diseño en `~/.gemini/config/skills/`.

---

## Next step

Para agregar nuevas directivas de diseño que el agente deba hacer cumplir, simplemente crea archivos de skill (por ejemplo `MI_DIRECTIVA_SKILL.md`) bajo la ruta global `~/.gemini/config/skills/` o dentro de carpetas locales como `.agents/skills/`. El agente las cargará y aplicará de forma automática en su próxima revisión.
