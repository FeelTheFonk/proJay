import sys, subprocess
from pathlib import Path

def main():
    args = sys.argv[1:]
    pn = args[0] if args else input("Entrez le nom du projet : ").strip()
    git = '--init-git' in args if args else input("Initialiser un dépôt Git ? (o/N) : ").lower().startswith('o')
    p = Path(pn)
    p.mkdir(parents=True, exist_ok=True)
    files = {
        "main.py": 'def main():\n    print("Hello, World!")\n\nif __name__ == "__main__":\n    main()\n',
        "go.ps1": r'.\venv\Scripts\activate; python -m pip install --upgrade pip; if(Test-Path requirements.txt){pip install -r requirements.txt}else{Write-Host "Le fichier requirements.txt n\'existe pas. Aucune dépendance installée."}; python .\main.py',
        ".gitignore": "# Byte-compiled / optimized / DLL files\n__pycache__/\n*.py[cod]\n*$py.class\n\n# Virtual environment\nvenv/\n\n# IDE files\n.vscode/\n.idea/\n\n# OS generated files\n.DS_Store\nThumbs.db",
        "README.md": f"# {pn}\n\nDescription de votre projet.\n\n## Installation\n\n1. Clonez ce dépôt\n2. Exécutez `go.ps1` pour créer l'environnement virtuel et installer les dépendances\n\n## Utilisation\n\n1. Activez l'environnement virtuel\n2. Exécutez `python main.py`",
        "requirements.txt": ""
    }
    for n, c in files.items():
        (p / n).write_text(c)
    subprocess.run([sys.executable, "-m", "venv", "venv"], cwd=p)
    if git:
        subprocess.run(["git", "init"], cwd=p)
    print(f"Projet '{pn}' créé avec succès.\n\nActions post-création :\n1. Ajoutez vos dépendances au 'requirements.txt' et exécutez 'go.ps1' pour installer les dépendances.\n2. Commencez à coder votre projet dans main.py!\n")
    input("Appuyez sur Entrée pour quitter...")

if __name__ == "__main__":
    main()