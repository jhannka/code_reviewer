import os
import shlex
import subprocess
from code_reviewer.ports.test_runner import TestRunnerPort

class PytestRunnerAdapter(TestRunnerPort):
    def _detect_test_command(self) -> str:
        # 1. Si hay una variable de entorno explícita, usarla
        env_cmd = os.getenv("TEST_COMMAND")
        if env_cmd:
            return env_cmd
            
        # 2. Detección automática según archivos del proyecto
        if os.path.exists("artisan"):
            return "php artisan test"
        elif os.path.exists("composer.json") and os.path.exists("vendor/bin/phpunit"):
            return "./vendor/bin/phpunit"
        elif os.path.exists("package.json"):
            return "npm test"
        elif os.path.exists("pytest.ini") or os.path.exists(".venv/bin/pytest") or os.path.exists(".venv/Scripts/pytest.exe"):
            if os.path.exists(".venv/Scripts/pytest.exe"):
                return ".venv/Scripts/pytest.exe"
            elif os.path.exists(".venv/bin/pytest"):
                return ".venv/bin/pytest"
            return "pytest"
        elif os.path.exists("go.mod"):
            return "go test ./..."
        elif os.path.exists("pom.xml"):
            return "mvn test"
        elif os.path.exists("build.gradle"):
            return "./gradlew test"
        elif os.path.exists("Cargo.toml"):
            return "cargo test"
            
        # Fallback genérico si no se detecta nada (para compatibilidad hacia atrás)
        return "pytest"

    def execute_tests(self) -> str:
        try:
            test_cmd_str = self._detect_test_command()
            test_cmd = shlex.split(test_cmd_str)
            
            # Execute command capturing stdout and stderr
            res = subprocess.run(
                test_cmd,
                capture_output=True,
                text=True,
                check=False
            )
            
            # Combine stdout and stderr for full test logs
            output = ""
            if res.stdout:
                output += f"STDOUT:\n{res.stdout.strip()}\n\n"
            if res.stderr:
                output += f"STDERR:\n{res.stderr.strip()}\n\n"
            
            status = "PASSED" if res.returncode == 0 else f"FAILED (exit code {res.returncode})"
            return f"Test Run Status: {status}\nCommand auto-detected and executed: {test_cmd_str}\n\n{output}"
        except FileNotFoundError:
            return f"Error: executable not found for the auto-detected test command '{test_cmd_str}'."
        except Exception as e:
            return f"Error executing tests ({test_cmd_str}): {str(e)}"
