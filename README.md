# proJay

# ![ThematrixreloadedNeoGIF](https://github.com/user-attachments/assets/4df80063-238e-4ce2-9468-13a55bb323f8)

Un script simple pour configurer rapidement une structure de projet Python.

## 🥱 Qu'est-ce que c'est ?

Ce script crée automatiquement :

- Un dossier de projet avec un fichier `main.py`
- Un dépôt Git (optionnel)
- Un environnement virtuel Python (optionnel)
- Des fichiers utiles (`.gitignore`, `go.ps1`, `README.md`)

## 📦 Comment l'utiliser ?

1. **Exécutez le script :**

   - Mode interactif

    Double clique sur go.py, ou :
     ```bash
     python go.py
     ```

   - Avec des options en ligne de commande
     ```bash
     python go.py [nom_du_projet] --init-git --create-venv
     ```

2. **Installez les dépendances** (si nécessaires) :

   ```powershell
   .\go.ps1
   ```

3. **Démarrez le développement** :

   - Modifiez `main.py` pour votre projet
   - Exécutez le script :
     ```bash
     python main.py
     ```
