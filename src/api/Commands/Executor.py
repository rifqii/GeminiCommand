import subprocess
import sys
import os
from pathlib import Path

def run_command(method: str, **kwargs):
    """Execute Commands.py with method and arguments dynamically."""
    
    python_exe = sys.executable

    # Path to project root (adjust the number of parents based on your structure)
    project_root = Path(__file__).resolve().parents[3]
    script_path = project_root / "src" / "api" / "Commands" / "Commands.py"
    
    # Convert kwargs into CLI arguments
    args = [f"--{key}={value}" for key, value in kwargs.items()]
    
    # Construct command to run the script directly
    command = [python_exe, str(script_path), method] + args

    print("Executing command:", ' '.join(command))
    
    # Set PYTHONPATH to include project root for module resolution
    env = os.environ.copy()
    env['PYTHONPATH'] = str(project_root) + os.pathsep + env.get('PYTHONPATH', '')
    
    # Run the command with the modified environment
    result = subprocess.run(command, env=env, capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print("Error:", result.stderr)