#!/usr/bin/env python3

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, Optional


class ProjectGenerator:
    """Universal and lightweight Python project structure generator."""

    def __init__(self, project_name: str, options: Dict[str, bool]):
        """
        Initialize the ProjectGenerator.

        Args:
            project_name (str): Name of the project to be created.
            options (Dict[str, bool]): Configuration options for the project.
        """
        self.project_name: str = project_name
        self.options: Dict[str, bool] = options
        self.base_path: Path = Path.cwd() / self.project_name

    def generate_structure(self) -> None:
        """Generate the base structure of the project."""
        try:
            self.base_path.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            self._exit_with_error(f"Error creating project folder: {e}")

        files: Dict[str, str] = {
            "main.py": self._get_main_py_content(),
            "setup.py": self._get_setup_py_content(),
            ".gitignore": self._get_gitignore_content(),
            "README.md": self._get_readme_content(),
            "requirements.txt": "",
        }

        for filename, content in files.items():
            self._write_file(filename, content)

        if not self.options.get('no_venv', False):
            self._create_venv()

        if self.options.get('init_git', False):
            self._init_git()

        print(f"\n✅ Project '{self.project_name}' created successfully.")

    def _create_venv(self) -> None:
        """Create a Python virtual environment."""
        print("🔧 Creating virtual environment...")
        try:
            subprocess.run([sys.executable, "-m", "venv", "venv"], cwd=self.base_path, check=True)
            print("✅ Virtual environment created.")
        except subprocess.CalledProcessError as e:
            self._exit_with_error(f"Error creating virtual environment: {e}")

    def _init_git(self) -> None:
        """Initialize a Git repository in the project folder."""
        print("🔧 Initializing Git repository...")
        if shutil.which("git"):
            try:
                subprocess.run(["git", "init"], cwd=self.base_path, check=True)
                print("✅ Git repository initialized.")
            except subprocess.CalledProcessError as e:
                self._exit_with_error(f"Error initializing Git repository: {e}")
        else:
            print("❌ Git is not installed or not in PATH.")

    def _get_main_py_content(self) -> str:
        """Return the content of the main.py file."""
        return '''
def main():
    """Entry point of the application."""
    print("Hello, World!")


if __name__ == "__main__":
    main()
'''.strip()

    def _get_setup_py_content(self) -> str:
        """Return the content of the setup.py file."""
        return '''
#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path


def main():
    """Set up the project environment."""
    venv_dir = Path.cwd() / 'venv'

    if not venv_dir.is_dir():
        print("🔧 Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)

    if sys.platform.startswith('win'):
        python_executable = venv_dir / 'Scripts' / 'python.exe'
    else:
        python_executable = venv_dir / 'bin' / 'python3'

    print("🔧 Updating pip...")
    subprocess.run([str(python_executable), "-m", "pip", "install", "--upgrade", "pip"], check=True)

    requirements_file = Path('requirements.txt')
    if requirements_file.exists() and requirements_file.stat().st_size > 0:
        print("🔧 Installing dependencies...")
        subprocess.run([str(python_executable), "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed.")
    else:
        print("ℹ️ No dependencies to install (requirements.txt is empty or doesn't exist).")


if __name__ == "__main__":
    main()
'''.strip()

    def _get_gitignore_content(self) -> str:
        """Return the content of the .gitignore file."""
        return '''
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Virtual environment
venv/

# IDE files
.vscode/
.idea/

# OS generated files
.DS_Store
Thumbs.db

# Distribution / packaging
dist/
build/
*.egg-info/

# Logs
*.log

# Unit test / coverage reports
htmlcov/
.coverage
.pytest_cache/
'''.strip()

    def _get_readme_content(self) -> str:
        """Return the content of the README.md file."""
        return f'''
# {self.project_name}

![Python Project](https://media.giphy.com/media/KAq5w47R9rmTuvWOWa/giphy.gif)

A Python project structure.

## 💊 Getting Started

1. **Set up the project environment**:
   ```bash
   python setup.py
   ```

2. **Run your application**:
   ```bash
   python main.py
   ```

## 📂 Project Structure

- `main.py`: Entry point of the application
- `setup.py`: Script to set up the project environment
- `requirements.txt`: List of project dependencies
- `.gitignore`: Specifies intentionally untracked files to ignore
- `README.md`: This file, containing project information

## 🕶️ Development

1. Activate the virtual environment:
   - On Windows: `venv\\Scripts\\activate`
   - On macOS and Linux: `source venv/bin/activate`

2. Install dependencies: `pip install -r requirements.txt`

3. Start coding!

---

🔵 Happy coding! 🔴
"""
'''.strip()

    def _write_file(self, filename: str, content: str) -> None:
        """Write content to a file in the project directory."""
        file_path = self.base_path / filename
        try:
            file_path.write_text(content, encoding='utf-8')
        except OSError as e:
            self._exit_with_error(f"Error writing file {filename}: {e}")

    @staticmethod
    def _exit_with_error(message: str) -> None:
        """Print an error message and exit the script."""
        print(f"❌ {message}")
        sys.exit(1)


def main() -> None:
    """Main entry point of the script."""
    parser = argparse.ArgumentParser(description="Universal Python Project Structure Generator")
    parser.add_argument("project_name", nargs='?', help="Name of the project to create")
    parser.add_argument("--init-git", action="store_true", help="Initialize a Git repository")
    parser.add_argument("--no-venv", action="store_true", help="Don't create a virtual environment")
    args = parser.parse_args()

    project_name: str = args.project_name if args.project_name else input("Enter project name: ").strip()

    if not project_name:
        print("❌ Project name cannot be empty.")
        sys.exit(1)

    options: Dict[str, bool] = {
        "init_git": args.init_git,
        "no_venv": args.no_venv,
    }

    generator = ProjectGenerator(project_name, options)
    generator.generate_structure()

    print("\n🔵 All set! Start coding now.")
    print(f"🔴 Project folder: {generator.base_path}")
    print("\n🌐 Happy development!")


if __name__ == "__main__":
    main()