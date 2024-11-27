import os
import sys
import subprocess
from pathlib import Path

class ProjectGenerator:
    def __init__(self, project_name, options):
        self.project_name = project_name
        self.options = options
        self.base_path = Path.cwd() / self.project_name

    def generate_structure(self):
        self.base_path.mkdir(parents=True, exist_ok=True)
        
        files = {
            "main.py": """
def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
""",
            "go.ps1": r"""
.\venv\Scripts\activate
python.exe -m pip install --upgrade pip
if (Test-Path requirements.txt) {
    pip install -r requirements.txt
} else {
    Write-Host "Le fichier requirements.txt n'existe pas. Aucune dépendance installée."
}
python .\main.py
""",
            ".gitignore": """
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
""",
            "README.md": f"""
# {self.project_name}

Description de votre projet.

## Installation

1. Clonez ce dépôt
2. Exécutez `go.ps1` pour créer l'environnement virtuel et installer les dépendances

## Utilisation

1. Activez l'environnement virtuel
2. Exécutez `python main.py`
""",
            "requirements.txt": ""
        }

        for filename, content in files.items():
            (self.base_path / filename).write_text(content, encoding='utf-8')

        self.create_venv()

        if self.options.get('init_git', False):
            self.init_git()
        
        print(f"Projet '{self.project_name}' créé avec succès.")

    def init_git(self):
        if shutil.which("git"):
            subprocess.run(["git", "init"], cwd=self.base_path, check=True)
            print("Dépôt Git initialisé.")
        else:
            print("Git n'est pas installé ou n'est pas dans le PATH.")

    def create_venv(self):
        subprocess.run([sys.executable, "-m", "venv", "venv"], cwd=self.base_path, check=True)
        print("Environnement virtuel créé.")

def main():
    if len(sys.argv) == 1:
        project_name = input("Entrez le nom du projet : ").strip()
        init_git = input("Initialiser un dépôt Git ? (o/N) : ").lower().startswith('o')
        options = {"init_git": init_git}
    else:
        parser = argparse.ArgumentParser(description="Générateur de structure de projet Python")
        parser.add_argument("project_name", help="Nom du projet à créer")
        parser.add_argument("--init-git", action="store_true", help="Initialiser un dépôt Git")
        args = parser.parse_args()
        project_name = args.project_name
        options = {"init_git": args.init_git}

    generator = ProjectGenerator(project_name, options)
    generator.generate_structure()

    print("\nActions post-création :")
    print("1. Ajoutez vos dépendances au 'requirements.txt' et exécutez 'go.ps1' pour installer les dépendances.")
    print("2. Commencez à coder votre projet dans main.py!")
    
    input("\nAppuyez sur Entrée pour quitter...")

if __name__ == "__main__":
    main()
