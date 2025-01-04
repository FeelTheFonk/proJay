import sys
import subprocess
from pathlib import Path

def main():
    args = sys.argv[1:]
    pn = args[0] if args else input("Enter the project name: ").strip()
    git = '--init-git' in args if args else input("Initialize a Git repository? (y/N): ").lower().startswith('y')
    p = Path(pn)
    p.mkdir(parents=True, exist_ok=True)

    is_windows = sys.platform.startswith('win')
    script_name = 'go.ps1' if is_windows else 'go.sh'

    files = {
        "main.py": 'def main():\n    print("Hello, World!")\n\nif __name__ == "__main__":\n    main()\n',
        script_name: (
            r'.\venv\Scripts\activate; python -m pip install --upgrade pip; '
            r'if(Test-Path requirements.txt){pip install -r requirements.txt}else{Write-Host "requirements.txt not found. No dependencies installed."}; '
            r'python .\main.py' if is_windows else
            '#!/bin/bash\nsource venv/bin/activate\npip install --upgrade pip\n'
            'if [ -f requirements.txt ]; then\n    pip install -r requirements.txt\nelse\n    echo "requirements.txt not found. No dependencies installed."\nfi\n'
            'python main.py\n'
        ),
        ".gitignore": "__pycache__/\n*.py[cod]\n*$py.class\nvenv/\n.vscode/\n.idea/\n.DS_Store\nThumbs.db",
        "README.md": f"# {pn}\n\nDescription of your project.\n\n## Installation\n\n1. Clone this repository\n2. Run `{script_name}` to create the virtual environment and install dependencies\n\n## Usage\n\n1. Activate the virtual environment\n2. Run `python main.py`",
        "requirements.txt": ""
    }

    for n, c in files.items():
        f = p / n
        f.write_text(c)
        if n == 'go.sh':
            f.chmod(0o755)

    (p / ".github/workflows").mkdir(parents=True, exist_ok=True)
    (p / ".github/dependabot.yml").write_text(
        "version: 2\nupdates:\n  - package-ecosystem: pip\n    directory: \"/\"\n    schedule:\n      interval: daily\n  - package-ecosystem: github-actions\n    directory: \"/\"\n    schedule:\n      interval: daily"
    )
    (p / ".github/workflows/ci.yml").write_text(
        "name: CI\n\non:\n  push:\n  pull_request:\n\njobs:\n  build-and-test:\n    runs-on: windows-latest\n\n    steps:\n      - uses: actions/checkout@v3\n      - uses: actions/setup-python@v4\n        with:\n          python-version: \"3.12\"\n      - name: Install dependencies\n        run: |\n          python -m pip install --upgrade pip\n          pip install -r requirements.txt\n      - name: Run tests\n        run: pytest"
    )

    subprocess.run([sys.executable, "-m", "venv", "venv"], cwd=p)
    if git:
        subprocess.run(["git", "init"], cwd=p)
    print(f"Project '{pn}' created successfully.\nAdd dependencies to 'requirements.txt' and run '{script_name}' to install them.\n")
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()