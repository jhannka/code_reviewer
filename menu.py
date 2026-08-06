import os
import sys
import subprocess
import tempfile

# Obtener el directorio de instalación absoluto de este script
INSTALL_DIR = os.path.dirname(os.path.abspath(__file__))

__version__ = "1.2.0"
CLI_LANG = "es"  # Idioma por defecto

# ANSI escape codes for modern terminal coloring
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
GRAY = "\033[90m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Enable virtual terminal processing on Windows natively
if os.name == 'nt':
    os.system('')

LOCALES = {
    "es": {
        "title": "AGENTE ARQUITECTO - MENÚ DE REVISIÓN",
        "opt_1": "Revisar cambios de Git (pendientes de commit)",
        "opt_2": "Revisar un archivo de código específico",
        "opt_3": "Analizar y listar las directivas (skills)",
        "opt_4": "Configurar API Key, Modelo e Idioma",
        "opt_5": "Salir",
        "status_bar": "[↑/↓] Navegar  |  [Enter] Seleccionar  |  [Esc/Q] Salir",
        "config_status_bar": "[↑/↓] Navegar  |  [Enter] Editar  |  [S] Guardar  |  [Esc/Q] Cancelar",
        "update_available": "✨ ¡NUEVA ACTUALIZACIÓN DISPONIBLE: v{}! ✨",
        "update_changes": "Cambios en esta versión:",
        "update_prompt": "¿Deseás descargar e instalar la actualización? [s/N]: ",
        "update_in_progress": "\n📦 Iniciando actualización limpia y segura...",
        "update_dirty_error": "\n❌ Error: Tenés cambios locales no committeados en el revisor de código.\nGuardá tus cambios (git stash o git commit) antes de actualizar.",
        "update_fetching": "📥 Buscando nuevas etiquetas en GitHub...",
        "update_checkout": "🔄 Cambiando a la versión {}...",
        "update_symlink": "🔄 Actualizando enlace simbólico global...",
        "update_success": "\n✅ ¡Actualización completada con éxito!\nReiniciando el programa...",
        "update_error": "\n❌ Error durante el proceso de actualización: {}\nSe recomienda realizar un 'git pull' manual.",
        "press_enter": "\nPresioná Enter para volver al menú...",
        "press_enter_continue": "\nPresioná Enter para continuar...",
        "git_title": "--- REVISANDO CAMBIOS PENDIENTES DE GIT ---",
        "git_query": "Inicia el flujo de revisión secuencial para analizar todos los cambios pendientes (git diff). Ejecuta obligatoriamente los agentes del 1 al 4 y presentá el informe de discrepancias y refactorización.",
        "file_title": "--- REVISAR ARCHIVO ESPECÍFICO ---",
        "file_prompt": "Ingresá la ruta del archivo, o el nombre de una clase/método a buscar: ",
        "file_empty": "Ruta vacía. Cancelando operación.",
        "file_not_exist": "\n❌ El archivo '{}' no existe en el disco.",
        "file_query": "Inicia el flujo de revisión secuencial para analizar el archivo '{}'. Ejecuta obligatoriamente los agentes del 1 al 4 y presentá el informe de discrepancias y refactorización.",
        "skills_title": "--- ANALIZAR Y LISTAR SKILLS ---",
        "skills_query": "Leé todas las skills del proyecto usando 'read_project_skills', listalas y generá un breve resumen explicativo de cada una.",
        "config_title": "--- CONFIGURAR CONFIGURACIÓN ---",
        "config_status": "Estado actual:",
        "config_key": "- Google API Key: {}",
        "config_model": "- Modelo de Gemini: {}",
        "config_lang": "- Idioma actual: {}",
        "config_key_prompt": "\nIngresá el nuevo valor (presioná Enter para mantener el actual): ",
        "config_saved": "\n✅ Configuración guardada correctamente.",
        "not_configured": "No configurada",
        "exit_msg": "\n¡Nos vemos! Éxitos en el código.",
        "invalid_opt": "\nOpción no válida. Por favor ingresá un número de 1 a 5.",
        "running_rev": "\n🚀 Iniciando revisión: '{}'\n",
        "agent_err": "\n⚠️  El agente terminó con algún error (código de salida diferente de 0).",
        "rev_canceled": "\n\n(Revisión cancelada por el usuario)",
        "exec_err": "\n❌ Error al ejecutar el agente: {}",
        "adk_missing": "\n❌ Error: No se encontró el ejecutable de ADK en el entorno virtual.\nAsegurate de haber creado el entorno virtual '.venv' e instalado los paquetes.",
        
        "config_opt_key": "Clave API Google",
        "config_opt_anthropic_key": "Clave API Anthropic",
        "config_opt_openai_key": "Clave API OpenAI",
        "config_opt_model": "Modelo: {}",
        "config_opt_veracity": "Nivel de Veracidad: {}",
        "config_opt_lang": "Idioma: {}",
        "config_api_keys_title": "Configurar API Keys (Tokens)",
        
        "model_menu_title": "SELECCIONAR MODELO",
        "model_custom": "Ingresar modelo personalizado...",
        "lang_menu_title": "SELECCIONAR IDIOMA DEL CLI",
        "veracity_menu_title": "SELECCIONAR VERACIDAD (PRECISIÓN)",
        "back": "Regresar",
        "custom_model_prompt": "Ingresá el identificador del modelo (ej: gemini-1.5-pro): ",
        
        "veracity_strict": "Estricto",
        "veracity_desc_strict": "Temp: 0.0 - Riguroso y determinista, ideal para bugs",
        "veracity_balanced": "Balanceado",
        "veracity_desc_balanced": "Temp: 0.4 - Recomendaciones y explicaciones moderadas",
        "veracity_creative": "Creativo",
        "veracity_desc_creative": "Temp: 0.7 - Alternativas y lluvia de ideas de refactorización",
        "api_503": "\n❌ Error: Los servidores del modelo de IA están saturados (503 UNAVAILABLE). Espera un momento y vuelve a intentarlo, o cambia de modelo en Configuración.",
        "api_invalid": "\n❌ Error: La clave de API configurada es inválida o expiró. Por favor revisa la Configuración del menú."
    },
    "en": {
        "title": "ARCHITECT AGENT - CODE REVIEW MENU",
        "opt_1": "Review Git Changes (uncommitted diffs)",
        "opt_2": "Review a specific code file",
        "opt_3": "Analyze and list design guidelines (skills)",
        "opt_4": "Configure API Key, Model & Language",
        "opt_5": "Exit",
        "status_bar": "[↑/↓] Navigate  |  [Enter] Select  |  [Esc/Q] Exit",
        "config_status_bar": "[↑/↓] Navigate  |  [Enter] Edit  |  [S] Save  |  [Esc/Q] Cancel",
        "update_available": "✨ NEW UPDATE AVAILABLE: v{}! ✨",
        "update_changes": "Changes in this version:",
        "update_prompt": "Do you want to download and install the update? [y/N]: ",
        "update_in_progress": "\n📦 Starting clean and safe update...",
        "update_dirty_error": "\n❌ Error: You have uncommitted changes in your code reviewer repository.\nStash or commit your changes before updating to prevent loss.",
        "update_fetching": "📥 Fetching new tags from GitHub...",
        "update_checkout": "🔄 Switching to version {}...",
        "update_symlink": "🔄 Updating global symbolic link...",
        "update_success": "\n✅ Update completed successfully!\nRestarting program...",
        "update_error": "\n❌ Error during the update process: {}\nWe recommend performing a manual 'git pull'.",
        "press_enter": "\nPress Enter to return to the menu...",
        "press_enter_continue": "\nPress Enter to continue...",
        "git_title": "--- REVIEWING UNCOMMITTED GIT CHANGES ---",
        "git_query": "Start the sequential review flow to analyze all uncommitted changes. You must execute agents 1 through 4 and present the discrepancies and refactoring report.",
        "file_title": "--- REVIEW SPECIFIC FILE ---",
        "file_prompt": "Enter the relative path, or a class/method name to search: ",
        "file_empty": "Empty path. Canceling operation.",
        "file_not_exist": "\n❌ The file '{}' does not exist on disk.",
        "file_query": "Start the sequential review flow to analyze the file '{}'. You must execute agents 1 through 4 and present the discrepancies and refactoring report.",
        "skills_title": "--- ANALYZING AND LISTING GUIDELINES ---",
        "skills_query": "Read all project design skills using 'read_project_skills', list them, and generate a brief summary of each.",
        "config_title": "--- CONFIGURE CONFIGURATION ---",
        "config_status": "Current status:",
        "config_key": "- Google API Key: {}",
        "config_model": "- Gemini Model: {}",
        "config_lang": "- Current Language: {}",
        "config_key_prompt": "\nEnter new value (press Enter to keep current): ",
        "config_saved": "\n✅ Configuration saved successfully.",
        "not_configured": "Not configured",
        "exit_msg": "\nGoodbye! Happy coding.",
        "invalid_opt": "\nInvalid option. Please enter a number between 1 and 5.",
        "running_rev": "\n🚀 Starting review: '{}'\n",
        "agent_err": "\n⚠️  The agent exited with an error (exit code not equal to 0).",
        "rev_canceled": "\n\n(Review canceled by user)",
        "exec_err": "\n❌ Error running the agent: {}",
        "adk_missing": "\n❌ Error: ADK executable not found in virtual environment.\nMake sure you created the '.venv' directory and installed packages.",
        
        "config_opt_key": "Google API Key",
        "config_opt_anthropic_key": "Anthropic API Key",
        "config_opt_openai_key": "OpenAI API Key",
        "config_opt_model": "Model: {}",
        "config_opt_veracity": "Veracity Level: {}",
        "config_opt_lang": "Language: {}",
        "config_api_keys_title": "Configure API Keys (Tokens)",
        
        "model_menu_title": "SELECT MODEL",
        "model_custom": "Enter custom model ID...",
        "lang_menu_title": "SELECT CLI LANGUAGE",
        "veracity_menu_title": "SELECT VERACITY (ACCURACY)",
        "back": "Back",
        "custom_model_prompt": "Enter custom model ID (eg: gemini-1.5-pro): ",
        
        "veracity_strict": "Strict",
        "veracity_desc_strict": "Temp: 0.0 - Rigorous and deterministic, ideal for bugs",
        "veracity_balanced": "Balanced",
        "veracity_desc_balanced": "Temp: 0.4 - Moderate recommendations and explanations",
        "veracity_creative": "Creative",
        "veracity_desc_creative": "Temp: 0.7 - Alternatives and refactoring brainstorming",
        "api_503": "\n❌ Error: The AI model servers are overloaded (503 UNAVAILABLE). Please wait a moment and try again, or switch models in Settings.",
        "api_invalid": "\n❌ Error: The configured API key is invalid or expired. Please check Settings in the menu."
    }
}

def t(key, *args):
    """Obtiene el texto localizado para el idioma actual."""
    lang_dict = LOCALES.get(CLI_LANG, LOCALES["es"])
    text = lang_dict.get(key, key)
    if args:
        return text.format(*args)
    return text

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_env_vars():
    """Lee las variables del archivo .env local en el directorio de instalación."""
    global CLI_LANG
    env_path = os.path.join(INSTALL_DIR, "code_reviewer", ".env")
    vars = {}
    if os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, val = line.split("=", 1)
                        vars[key.strip()] = val.strip()
        except Exception as e:
            print(f"Error al leer .env: {str(e)}")
    CLI_LANG = vars.get("CLI_LANG", "es").strip().lower()
    if CLI_LANG not in ["es", "en"]:
        CLI_LANG = "es"
    return vars

def save_env_vars(vars):
    """Guarda las variables en el archivo .env local en el directorio de instalación."""
    global CLI_LANG
    CLI_LANG = vars.get("CLI_LANG", CLI_LANG)
    env_path = os.path.join(INSTALL_DIR, "code_reviewer", ".env")
    try:
        with open(env_path, "w", encoding="utf-8") as f:
            for key, val in vars.items():
                f.write(f"{key}={val}\n")
    except Exception as e:
        print(f"Error al escribir en .env: {str(e)}")

def check_for_updates():
    """Verifica si hay actualizaciones en el repositorio remoto usando la API de GitHub."""
    import urllib.request
    import json
    import ssl
    
    # 1. Intentar primero obtener la última release publicada (con descripción de cambios)
    release_url = "https://api.github.com/repos/jhannka/code_reviewer/releases/latest"
    req = urllib.request.Request(release_url, headers={"User-Agent": "code-reviewer-cli"})
    try:
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(req, timeout=1.5, context=context) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                tag_name = data.get("tag_name", "").strip()
                body = data.get("body", "Sin descripción.")
                _prompt_update_if_needed(tag_name, body)
                return
    except Exception:
        pass

    # 2. Si falla (ej. si no hay releases publicadas aún), caer a la lista de tags
    tags_url = "https://api.github.com/repos/jhannka/code_reviewer/tags"
    req = urllib.request.Request(tags_url, headers={"User-Agent": "code-reviewer-cli"})
    try:
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(req, timeout=1.5, context=context) as response:
            if response.status == 200:
                tags = json.loads(response.read().decode("utf-8"))
                if tags:
                    tag_name = tags[0].get("name", "").strip()
                    body = "Hay una nueva versión disponible en GitHub. Consultá el CHANGELOG.md para ver los detalles." if CLI_LANG == "es" else "A new version is available on GitHub. Check CHANGELOG.md for details."
                    _prompt_update_if_needed(tag_name, body)
    except Exception:
        pass

def _prompt_update_if_needed(tag_name: str, body: str):
    remote_ver = tag_name.lstrip("v")
    local_ver = __version__.lstrip("v")
    if remote_ver != local_ver:
        try:
            remote_parts = [int(x) for x in remote_ver.split(".")]
            local_parts = [int(x) for x in local_ver.split(".")]
            if remote_parts > local_parts:
                _show_update_dialog(tag_name, remote_ver, body)
        except ValueError:
            if remote_ver > local_ver:
                _show_update_dialog(tag_name, remote_ver, body)

def _show_update_dialog(tag_name: str, remote_ver: str, body: str):
    print("\n==================================================")
    print(t("update_available", remote_ver))
    print("==================================================")
    print(f"{t('update_changes')}\n{body}")
    print("--------------------------------------------------")
    ans = input(t("update_prompt")).strip().lower()
    if ans in ["s", "si", "yes", "y"]:
        apply_update(tag_name)
        sys.exit(0)

def apply_update(tag_name: str):
    """Aplica la actualización de manera segura utilizando comandos de Git."""
    print(t("update_in_progress"))
    try:
        diff_status = subprocess.run(["git", "diff", "--quiet"], cwd=INSTALL_DIR)
        cached_status = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=INSTALL_DIR)
        if diff_status.returncode != 0 or cached_status.returncode != 0:
            print(t("update_dirty_error"))
            input(t("press_enter_continue"))
            return
    except Exception as e:
        print(t("update_error", str(e)))
        input(t("press_enter_continue"))
        return
        
    try:
        print(t("update_fetching"))
        subprocess.run(["git", "fetch", "--tags"], cwd=INSTALL_DIR, check=True)
        
        print(t("update_checkout", tag_name))
        subprocess.run(["git", "checkout", f"tags/{tag_name}"], cwd=INSTALL_DIR, check=True)
        
        if os.name != 'nt':
            install_sh = os.path.join(INSTALL_DIR, "install.sh")
            if os.path.exists(install_sh):
                print(t("update_symlink"))
                subprocess.run(["chmod", "+x", install_sh], cwd=INSTALL_DIR)
                sym_path = "/opt/homebrew/bin/code-reviewer"
                wrapper_path = os.path.join(INSTALL_DIR, "bin", "code-reviewer")
                if os.path.exists(sym_path):
                    subprocess.run(["ln", "-sf", wrapper_path, sym_path])
                    
        print(t("update_success"))
        input(t("press_enter_continue"))
    except Exception as e:
        print(t("update_error", str(e)))
        input(t("press_enter_continue"))

def get_key():
    """Lee una sola pulsación de tecla y retorna una cadena descriptiva."""
    if os.name == 'nt':
        import msvcrt
        ch = msvcrt.getch()
        if ch in (b'\x00', b'\xe0'):
            ch2 = msvcrt.getch()
            if ch2 == b'H': return "up"
            if ch2 == b'P': return "down"
            if ch2 == b'M': return "right"
            if ch2 == b'K': return "left"
            return None
        if ch == b'\r': return "enter"
        if ch == b'\x1b': return "esc"
        try:
            char = ch.decode('utf-8').lower()
            if char == 'q': return "esc"
            return char
        except Exception:
            return None
    else:
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == '\x1b':
                ch2 = sys.stdin.read(1)
                if ch2 == '[':
                    ch3 = sys.stdin.read(1)
                    if ch3 == 'A': return "up"
                    if ch3 == 'B': return "down"
                    if ch3 == 'C': return "right"
                    if ch3 == 'D': return "left"
                return "esc"
            if ch == '\r' or ch == '\n': return "enter"
            if ch == 'q' or ch == 'Q': return "esc"
            return ch.lower()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def is_interactive():
    """Retorna True si la entrada estándar es una terminal interactiva (TTY)."""
    return sys.stdin.isatty()

def select_from_menu(title: str, options: list) -> int:
    """Muestra un menú de selección interactiva y retorna el índice de la opción elegida.
    Si se presiona Esc, retorna -1.
    """
    selected_index = 0
    while True:
        clear_screen()
        print(f"{CYAN}┌──────────────────────────────────────────────────┐{RESET}")
        print(f"{CYAN}│{BOLD} {title.center(48)} {RESET}{CYAN}│{RESET}")
        print(f"{CYAN}└──────────────────────────────────────────────────┘{RESET}")
        
        for idx, opt in enumerate(options):
            if idx == selected_index:
                print(f" {GREEN}➔ {BOLD}{opt}{RESET}")
            else:
                print(f"    {GRAY}{opt}{RESET}")
        
        print(f"{CYAN}--------------------------------------------------{RESET}")
        print(f"{GRAY}{t('status_bar')}{RESET}")
        
        key = get_key()
        if key == "up":
            selected_index = (selected_index - 1) % len(options)
        elif key == "down":
            selected_index = (selected_index + 1) % len(options)
        elif key in [str(i+1) for i in range(len(options))]:
            selected_index = int(key) - 1
            return selected_index
        elif key == "enter":
            return selected_index
        elif key == "esc":
            return -1

def run_agent_query(query: str):
    """Ejecuta el agente ADK usando la CLI compartiendo la terminal interactiva."""
    adk_path = os.path.join(INSTALL_DIR, ".venv", "bin", "adk")
    if not os.path.exists(adk_path):
        adk_path = os.path.join(INSTALL_DIR, ".venv", "Scripts", "adk")
        if not os.path.exists(adk_path):
            adk_path = os.path.join(INSTALL_DIR, ".venv", "Scripts", "adk.exe")
            if not os.path.exists(adk_path):
                print(t("adk_missing"))
                return
            
    print(t("running_rev", query))
    try:
        env = os.environ.copy()
        env["PYTHONWARNINGS"] = "ignore"
        env["PYTHONPATH"] = f"{INSTALL_DIR}:{env.get('PYTHONPATH', '')}"
        env["PYTHONIOENCODING"] = "utf-8" # Prevenir error de Unicode en el spinner
        
        agent_dir = os.path.join(INSTALL_DIR, "code_reviewer")
        import uuid
        session_id = f"review_{uuid.uuid4().hex[:8]}"
        session_file = os.path.join(agent_dir, ".adk", "sessions", f"{session_id}.json")
        
        def run_step(prompt: str, is_first: bool):
            cmd = [adk_path, "run", "--log_level", "error"]
            if not is_first and os.path.exists(session_file):
                cmd.extend(["--resume", session_file])
            else:
                cmd.extend(["--save_session", "--session_id", session_id])
                
            cmd.extend([agent_dir, prompt])
            
            result = subprocess.run(cmd, env=env)
            if result.returncode != 0:
                error_found = False
                log_path = os.path.join(tempfile.gettempdir(), "agents_log", "agent.latest.log")
                if os.path.exists(log_path):
                    try:
                        with open(log_path, "r", encoding="utf-8", errors="replace") as f:
                            log_content = f.read()
                            if "503 UNAVAILABLE" in log_content:
                                print(t("api_503"))
                                error_found = True
                            elif "API_KEY_INVALID" in log_content or "API key not valid" in log_content:
                                print(t("api_invalid"))
                                error_found = True
                    except:
                        pass
                if not error_found:
                    print(t("agent_err"))
                return False
            return True
            
        # Ejecutar la primera instrucción
        if not run_step(query, is_first=True):
            return
            
        # Iniciar ciclo interactivo manual (para sortear el single-step de subprocess)
        while True:
            user_input = input(f"\n{GREEN}Tú (Enter vacío para salir): {RESET}").strip()
            if not user_input:
                break
            print("\n")
            if not run_step(user_input, is_first=False):
                print(f"{YELLOW}⚠️ No se pudo procesar la respuesta. Puedes intentar enviarla nuevamente.{RESET}")
                continue

    except KeyboardInterrupt:
        print(t("rev_canceled"))
    except Exception as e:
        print(t("exec_err", str(e)))

def execute_option(choice: int):
    """Ejecuta la acción asociada al número de opción elegido."""
    if choice == 1:
        clear_screen()
        print(f"{CYAN}{t('git_title')}{RESET}")
        run_agent_query(t("git_query"))
        input(t("press_enter"))
        
    elif choice == 2:
        clear_screen()
        print(f"{CYAN}{t('file_title')}{RESET}")
        file_path = input(t("file_prompt")).strip()
        if not file_path:
            print(t("file_empty"))
            input(t("press_enter"))
            return
            
        if not os.path.exists(file_path):
            print(f"Buscando '{file_path}' en los archivos locales...")
            found = []
            for root, dirs, files in os.walk("."):
                dirs[:] = [d for d in dirs if d not in [".git", "node_modules", ".venv", "__pycache__", "vendor"]]
                for f in files:
                    if f.endswith((".py", ".js", ".ts", ".php", ".java", ".cs", ".go", ".rb", ".json", ".md")):
                        p = os.path.join(root, f)
                        try:
                            with open(p, "r", encoding="utf-8") as fp:
                                if file_path in fp.read():
                                    found.append(p)
                        except:
                            pass
            if not found:
                print(t("file_not_exist", file_path))
                input(t("press_enter"))
                return
            elif len(found) > 1:
                idx = select_from_menu(f"Múltiples coincidencias para '{file_path}':", found)
                if idx >= 0:
                    file_path = found[idx]
                else:
                    return
            else:
                file_path = found[0]
                print(f"Encontrado en: {file_path}")
            
        run_agent_query(t("file_query", file_path))
        input(t("press_enter"))
        
    elif choice == 3:
        clear_screen()
        print(f"{CYAN}{t('skills_title')}{RESET}")
        run_agent_query(t("skills_query"))
        input(t("press_enter"))
        
    elif choice == 4:
        configure_settings()
        
    elif choice == 5:
        print(t("exit_msg"))

def configure_settings_interactive():
    """Panel de configuración interactiva con submenús dinámicos y atajos de guardado/cancelado."""
    vars = load_env_vars()
    temp_key = vars.get("GOOGLE_API_KEY", "")
    temp_anthropic_key = vars.get("ANTHROPIC_API_KEY", "")
    temp_openai_key = vars.get("OPENAI_API_KEY", "")
    temp_model = vars.get("GEMINI_MODEL", "gemini-2.5-flash")
    temp_lang = vars.get("CLI_LANG", "es").strip().lower()
    temp_veracity = vars.get("REVIEW_VERACITY", "strict").strip().lower()
    
    selected_index = 0
    while True:
        items = []
        items.append((t('config_api_keys_title'), "api_keys"))
        
        display_lang = "Español" if temp_lang == "es" else "English"
        
        items.append((f"{t('config_opt_model', temp_model)}", "model"))
        items.append((f"{t('config_opt_veracity', t('veracity_' + temp_veracity))}", "veracity"))
        items.append((f"{t('config_opt_lang', display_lang)}", "lang"))
        
        # Ajustar el índice si disminuye el tamaño del menú
        selected_index = selected_index % len(items)
        
        clear_screen()
        print(f"{CYAN}┌──────────────────────────────────────────────────┐{RESET}")
        print(f"{CYAN}│{BOLD} {t('config_title').center(48)} {RESET}{CYAN}│{RESET}")
        print(f"{CYAN}└──────────────────────────────────────────────────┘{RESET}")
        
        for idx, (label, _) in enumerate(items):
            if idx == selected_index:
                print(f" {GREEN}➔ {BOLD}[{idx+1}] {label}{RESET}")
            else:
                print(f"    {GRAY}[{idx+1}] {label}{RESET}")
        
        print(f"{CYAN}--------------------------------------------------{RESET}")
        print(f"{GRAY}{t('config_status_bar')}{RESET}")
        
        key = get_key()
        if key == "up":
            selected_index = (selected_index - 1) % len(items)
            continue
        elif key == "down":
            selected_index = (selected_index + 1) % len(items)
            continue
        elif key == "s":  # Atajo Guardar
            vars["GOOGLE_API_KEY"] = temp_key
            vars["ANTHROPIC_API_KEY"] = temp_anthropic_key
            vars["OPENAI_API_KEY"] = temp_openai_key
            vars["GEMINI_MODEL"] = temp_model
            vars["CLI_LANG"] = temp_lang
            vars["REVIEW_VERACITY"] = temp_veracity
            save_env_vars(vars)
            print(t("config_saved"))
            input(t("press_enter"))
            break
        elif key == "esc":  # Atajo Cancelar
            load_env_vars()  # Restaurar idioma global original cargado de .env al cancelar
            break
        elif key in [str(i+1) for i in range(len(items))]:
            selected_index = int(key) - 1
            tag = items[selected_index][1]
        elif key == "enter":
            tag = items[selected_index][1]
        else:
            continue
            
        if tag == "api_keys":
            while True:
                s_google = "Configurado" if temp_key else "No configurado"
                s_anthropic = "Configurado" if temp_anthropic_key else "No configurado"
                s_openai = "Configurado" if temp_openai_key else "No configurado"
                
                key_opts = [
                    f"Google (Gemini) - {s_google}",
                    f"Anthropic (Claude) - {s_anthropic}",
                    f"OpenAI (GPT/DeepSeek) - {s_openai}",
                    t("back")
                ]
                idx_key = select_from_menu(t("config_api_keys_title"), key_opts)
                if idx_key == 3:
                    break
                elif idx_key == 0:
                    clear_screen()
                    print(f"{CYAN}--- {t('config_opt_key')} ---{RESET}")
                    new_key = input(t("config_key_prompt")).strip()
                    if new_key: temp_key = new_key
                elif idx_key == 1:
                    clear_screen()
                    print(f"{CYAN}--- {t('config_opt_anthropic_key')} ---{RESET}")
                    new_key = input(t("config_key_prompt")).strip()
                    if new_key: temp_anthropic_key = new_key
                elif idx_key == 2:
                    clear_screen()
                    print(f"{CYAN}--- {t('config_opt_openai_key')} ---{RESET}")
                    new_key = input(t("config_key_prompt")).strip()
                    if new_key: temp_openai_key = new_key
                
        elif tag == "model":
            while True:
                provider_options = [
                    "Google (Gemini)",
                    "Anthropic (Claude)",
                    "OpenAI (GPT)",
                    "OpenAI-Compatible (DeepSeek, Kimi...)",
                    t("model_custom"),
                    t("back")
                ]
                idx_prov = select_from_menu(t("model_menu_title"), provider_options)
                
                if idx_prov == 5:  # t("back")
                    break
                    
                if idx_prov == 0:
                    opts = ["gemini-3.5-flash", "gemini-3.5-pro", "gemini-3.0-flash", t("back")]
                    idx_m = select_from_menu("Google (Gemini)", opts)
                    if idx_m >= 0 and idx_m < len(opts) - 1:
                        temp_model = opts[idx_m]
                        break
                elif idx_prov == 1:
                    opts = ["claude-3-5-sonnet", "claude-3-5-haiku", "claude-3-opus", t("back")]
                    idx_m = select_from_menu("Anthropic (Claude)", opts)
                    if idx_m >= 0 and idx_m < len(opts) - 1:
                        temp_model = opts[idx_m]
                        break
                elif idx_prov == 2:
                    opts = ["openai/gpt-4o", "openai/gpt-4o-mini", "openai/o1-mini", t("back")]
                    idx_m = select_from_menu("OpenAI (GPT)", opts)
                    if idx_m >= 0 and idx_m < len(opts) - 1:
                        temp_model = opts[idx_m]
                        vars["OPENAI_API_BASE"] = ""  # Limpiar URL base para OpenAI oficial
                        break
                elif idx_prov == 3:
                    clear_screen()
                    print(f"{CYAN}--- Configurar Modelo Compatible con OpenAI ---{RESET}")
                    custom = input("Ingresa el identificador (ej: openai/deepseek-chat): ").strip()
                    if custom:
                        if not custom.startswith("openai/"): custom = f"openai/{custom}"
                        base_url = input("Ingresa el Base URL (ej: https://api.deepseek.com/v1): ").strip()
                        temp_model = custom
                        if base_url: vars["OPENAI_API_BASE"] = base_url
                        break
                elif idx_prov == 4:
                    clear_screen()
                    custom = input(t("custom_model_prompt")).strip()
                    if custom:
                        temp_model = custom
                        break
                    
        elif tag == "veracity":
            veracity_options = [
                f"{t('veracity_strict')} - {t('veracity_desc_strict')}",
                f"{t('veracity_balanced')} - {t('veracity_desc_balanced')}",
                f"{t('veracity_creative')} - {t('veracity_desc_creative')}",
                t("back")
            ]
            idx_ver = select_from_menu(t("veracity_menu_title"), veracity_options)
            if idx_ver == 0:
                temp_veracity = "strict"
            elif idx_ver == 1:
                temp_veracity = "balanced"
            elif idx_ver == 2:
                temp_veracity = "creative"
                
        elif tag == "lang":
            lang_options = [
                "Español",
                "English",
                t("back")
            ]
            idx_lang = select_from_menu(t("lang_menu_title"), lang_options)
            if idx_lang == 0:
                temp_lang = "es"
                global CLI_LANG
                CLI_LANG = "es"
            elif idx_lang == 1:
                temp_lang = "en"
                CLI_LANG = "en"

def configure_settings_non_interactive():
    """Configuración secuencial fallback para entornos no-interactivos."""
    vars = load_env_vars()
    current_model = vars.get("GEMINI_MODEL", "gemini-2.5-flash")
    current_lang = vars.get("CLI_LANG", "es").strip().lower()
    current_veracity = vars.get("REVIEW_VERACITY", "strict").strip().lower()
    
    print(f"{CYAN}{t('config_title')}{RESET}")
    print(t("config_status"))
    print(t("config_model", current_model))
    print(t("config_lang", "Español" if current_lang == "es" else "English"))
    print(t("config_opt_veracity", current_veracity))
    print("----------------------------------")
    
    new_key = input(t("config_key_prompt")).strip()
    if new_key:
        vars["GOOGLE_API_KEY"] = new_key
        
    print(t("config_model_title"))
    print("1. Google (Gemini)\n2. Anthropic (Claude)\n3. OpenAI (GPT)\n4. OpenAI-Compatible (DeepSeek, Kimi...)\n5. Custom")
    sel_prov = input("Select provider [1-5]: ").strip()
    if sel_prov == "1":
        print("1. gemini-3.5-flash\n2. gemini-3.5-pro\n3. gemini-3.0-flash")
        sel_m = input("Select model [1-3]: ").strip()
        models = {"1": "gemini-3.5-flash", "2": "gemini-3.5-pro", "3": "gemini-3.0-flash"}
        if sel_m in models: vars["GEMINI_MODEL"] = models[sel_m]
    elif sel_prov == "2":
        print("1. claude-3-5-sonnet\n2. claude-3-5-haiku\n3. claude-3-opus")
        sel_m = input("Select model [1-3]: ").strip()
        models = {"1": "claude-3-5-sonnet", "2": "claude-3-5-haiku", "3": "claude-3-opus"}
        if sel_m in models: vars["GEMINI_MODEL"] = models[sel_m]
    elif sel_prov == "3":
        print("1. openai/gpt-4o\n2. openai/gpt-4o-mini\n3. openai/o1-mini")
        sel_m = input("Select model [1-3]: ").strip()
        models = {"1": "openai/gpt-4o", "2": "openai/gpt-4o-mini", "3": "openai/o1-mini"}
        if sel_m in models: 
            vars["GEMINI_MODEL"] = models[sel_m]
            vars["OPENAI_API_BASE"] = ""
    elif sel_prov == "4":
        custom = input("Enter identifier (eg: openai/deepseek-chat): ").strip()
        if custom:
            if not custom.startswith("openai/"): custom = f"openai/{custom}"
            base_url = input("Enter Base URL (eg: https://api.deepseek.com/v1): ").strip()
            vars["GEMINI_MODEL"] = custom
            if base_url: vars["OPENAI_API_BASE"] = base_url
    elif sel_prov == "5":
        custom = input("Enter model ID: ").strip()
        if custom: vars["GEMINI_MODEL"] = custom
            
    # Si requiere otras llaves, solicitarlas
    target_model = vars.get("GEMINI_MODEL", current_model)
    if target_model.startswith("claude-") or "anthropic" in target_model:
        a_key = input("Enter Anthropic API Key: ").strip()
        if a_key:
            vars["ANTHROPIC_API_KEY"] = a_key
    if target_model.startswith("openai/") or "gpt" in target_model:
        o_key = input("Enter OpenAI / Compatible API Key: ").strip()
        if o_key:
            vars["OPENAI_API_KEY"] = o_key
            
    print("Select Veracity: 1. Strict, 2. Balanced, 3. Creative")
    ver_sel = input("Veracity choice [1-3]: ").strip()
    if ver_sel == "1":
        vars["REVIEW_VERACITY"] = "strict"
    elif ver_sel == "2":
        vars["REVIEW_VERACITY"] = "balanced"
    elif ver_sel == "3":
        vars["REVIEW_VERACITY"] = "creative"
        
    print(t("config_lang_title"))
    print(t("config_lang_options"))
    
    sel_lang = input(t("config_lang_prompt")).strip()
    if sel_lang == "1":
        vars["CLI_LANG"] = "es"
    elif sel_lang == "2":
        vars["CLI_LANG"] = "en"
        
    if "GOOGLE_GENAI_USE_ENTERPRISE" not in vars:
        vars["GOOGLE_GENAI_USE_ENTERPRISE"] = "0"
        
    save_env_vars(vars)
    print(t("config_saved"))
    input(t("press_enter"))

def configure_settings():
    """Elige el flujo de configuración según el tipo de terminal."""
    if is_interactive():
        configure_settings_interactive()
    else:
        configure_settings_non_interactive()

def menu_interactive():
    """Loop del menú interactivo principal por teclado."""
    selected_index = 0
    options = ["opt_1", "opt_2", "opt_3", "opt_4", "opt_5"]
    
    while True:
        clear_screen()
        print(f"{CYAN}┌──────────────────────────────────────────────────┐{RESET}")
        print(f"{CYAN}│{BOLD} {t('title').center(48)} {RESET}{CYAN}│{RESET}")
        print(f"{CYAN}└──────────────────────────────────────────────────┘{RESET}")
        
        for idx, opt_key in enumerate(options):
            if idx == selected_index:
                print(f" {GREEN}➔ {BOLD}[{idx+1}] {t(opt_key)}{RESET}")
            else:
                print(f"    {GRAY}[{idx+1}] {t(opt_key)}{RESET}")
        
        print(f"{CYAN}--------------------------------------------------{RESET}")
        print(f"{GRAY}{t('status_bar')}{RESET}")
        
        key = get_key()
        if key == "up":
            selected_index = (selected_index - 1) % len(options)
        elif key == "down":
            selected_index = (selected_index + 1) % len(options)
        elif key in ["1", "2", "3", "4", "5"]:
            selected_index = int(key) - 1
            execute_option(selected_index + 1)
            if selected_index == 4:
                break
        elif key == "enter":
            execute_option(selected_index + 1)
            if selected_index == 4:
                break
        elif key == "esc":
            execute_option(5)
            break

def menu_non_interactive():
    """Fallback del menú no-interactivo para pipelines o tuberías."""
    while True:
        clear_screen()
        print("==================================================")
        print(f"      {t('title')}        ")
        print("==================================================")
        print(f"1. {t('opt_1')}")
        print(f"2. {t('opt_2')}")
        print(f"3. {t('opt_3')}")
        print(f"4. {t('opt_4')}")
        print(f"5. {t('opt_5')}")
        print("==================================================")
        
        try:
            opcion = input("Seleccioná una opción [1-5]: ").strip()
        except KeyboardInterrupt:
            print(t("exit_msg"))
            break
        except EOFError:
            break
            
        if opcion in ["1", "2", "3", "4", "5"]:
            execute_option(int(opcion))
            if opcion == "5":
                break
        else:
            print(t("invalid_opt"))
            input(t("press_enter_continue"))

def menu():
    load_env_vars()
    check_for_updates()
    if is_interactive():
        menu_interactive()
    else:
        menu_non_interactive()

if __name__ == "__main__":
    menu()
