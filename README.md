# proJay

# ![ThematrixreloadedNeoGIF](https://github.com/user-attachments/assets/4df80063-238e-4ce2-9468-13a55bb323f8)

A lightweight, universal Python project structure generator that sets up fast.

## 🕶 Features

- Creates a basic Python project structure
- Virtual environment creation
- Optional Git repository initialization
- Generates essential files (`main.py`, `go.sh` or `go.ps1`, `.gitignore`, `README.md`, `requirements.txt`)

## 💊 Quick Start

1. **Run the script** - double-click or:
   ```bash
   python go.py
   ```

## 🔴 Usage

```
python go.py [--init-git] [project_name]
```

Arguments:
- `project_name`: Name of the project to create (optional, will prompt if not provided)
- `--init-git`: Initialize a Git repository

## 📂 Generated Project Structure

- `main.py`: Entry point of the application
- `go.sh` or `go.ps1`: Script to set up the project environment and run the application
- `requirements.txt`: List of project dependencies
- `.gitignore`: Specifies intentionally untracked files to ignore
- `README.md`: Project information and documentation

## 🌐 Development

1. Navigate to your generated project folder.

2. Activate the virtual environment:
   - On **Windows**:
     ```powershell
     venv\Scripts\activate
     ```
   - On **macOS** and **Linux**:
     ```bash
     source venv/bin/activate
     ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

🔵 Happy coding! 🔴

---
