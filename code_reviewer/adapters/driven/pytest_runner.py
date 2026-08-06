import subprocess
from code_reviewer.ports.test_runner import TestRunnerPort

class PytestRunnerAdapter(TestRunnerPort):
    def execute_tests(self) -> str:
        try:
            # Execute pytest capturing stdout and stderr
            res = subprocess.run(
                [".venv/bin/pytest"],
                env={"PYTHONPATH": ".:code_reviewer"},
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
            return f"Test Run Status: {status}\n\n{output}"
        except FileNotFoundError:
            return "Error: pytest executable not found in .venv/bin/pytest."
        except Exception as e:
            return f"Error executing pytest: {str(e)}"
