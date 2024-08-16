import os
import sys
import argparse
import subprocess
from pathlib import Path

class ProjectGenerator:
    def __init__(self, project_name, options):
        self.project_name = project_name
        self.options = options
        self.base_path = Path.cwd() / self.project_name

    def create_directory(self, path):
        path.mkdir(parents=True, exist_ok=True)

    def create_file(self, path, content=""):
        with open(path, 'w', encoding='utf-8') as file:
            file.write(content)

    def generate_structure(self):
        self.create_directory(self.base_path)

        self.create_main_py()
        self.create_additional_files()
        
        if self.options.get('init_git', False):
            self.init_git()
        
        if self.options.get('create_venv', False):
            self.create_venv()

        print(f"Projet '{self.project_name}' créé avec succès.")

    def create_main_py(self):
        main_content = """
def main():
    print("Hello, World!")

if __name__ == "__main__":
    main()
"""
        self.create_file(self.base_path / "main.py", main_content)

    def create_additional_files(self):
        # Création de go.ps1
        go_script_content = r"""
.\venv\Scripts\activate
python.exe -m pip install --upgrade pip
if (Test-Path requirements.txt) {
    pip install -r requirements.txt
} else {
    Write-Host "Le fichier requirements.txt n'existe pas. Aucune dépendance installée."
}
"""
        self.create_file(self.base_path / "go.ps1", go_script_content)

        # Création de .gitignore
        gitignore_content = """
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
"""
        self.create_file(self.base_path / ".gitignore", gitignore_content)

        # Création de README.md
        readme_content = f"""
# {self.project_name}

Description de votre projet.

## Installation

1. Clonez ce dépôt
2. Exécutez `go.ps1` pour créer l'environnement virtuel et installer les dépendances

## Utilisation

1. Activez l'environnement virtuel
2. Exécutez `python main.py`

## Tests

Exécutez `python -m unittest discover tests` pour lancer les tests.

## Licence

Spécifiez votre licence ici.
"""
        self.create_file(self.base_path / "README.md", readme_content)

    def init_git(self):
        try:
            subprocess.run(["git", "init"], cwd=self.base_path, check=True)
            print("Dépôt Git initialisé.")
        except subprocess.CalledProcessError:
            print("Erreur lors de l'initialisation du dépôt Git.")
        except FileNotFoundError:
            print("Git n'est pas installé ou n'est pas dans le PATH.")

    def create_venv(self):
        try:
            subprocess.run([sys.executable, "-m", "venv", "venv"], cwd=self.base_path, check=True)
            print("Environnement virtuel créé.")
        except subprocess.CalledProcessError:
            print("Erreur lors de la création de l'environnement virtuel.")

def interactive_mode():
    project_name = input("Entrez le nom du projet : ").strip()
    while not project_name:
        project_name = input("Le nom du projet ne peut pas être vide. Réessayez : ").strip()

    init_git = input("Initialiser un dépôt Git ? (o/N) : ").lower().startswith('o')
    create_venv = input("Créer un environnement virtuel ? (o/N) : ").lower().startswith('o')

    return project_name, {"init_git": init_git, "create_venv": create_venv}

def main():
    if len(sys.argv) == 1:
        project_name, options = interactive_mode()
    else:
        parser = argparse.ArgumentParser(description="Générateur de structure de projet Python")
        parser.add_argument("project_name", help="Nom du projet à créer")
        parser.add_argument("--init-git", action="store_true", help="Initialiser un dépôt Git")
        parser.add_argument("--create-venv", action="store_true", help="Créer un environnement virtuel")
        args = parser.parse_args()

        project_name = args.project_name
        options = {"init_git": args.init_git, "create_venv": args.create_venv}

    generator = ProjectGenerator(project_name, options)
    generator.generate_structure()

    print("\nActions post-création :")
    print("1. Ajoutes vos dépendances au 'requirements.txt' et exécutez 'go.ps1' pour installer les dépendances.")
    print("2. Commencez à coder votre projet dans main.py!")
    
    input("\nAppuyez sur Entrée pour quitter...")

if __name__ == "__main__":
    main()