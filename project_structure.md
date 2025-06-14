# VocoBell Project Structure

This is the recommended structure for deployment:

vocobell/
│
├── venv/ # Virtual environment (gitignored)
├── instance/ # Flask instance folder
│ └── vocobell.db # SQLite database (gitignored)
│
├── website/ # Your Flask app code
│ ├── __init__.py
| ├── auth.py
│ ├── models.py
│ ├── user.py
│ ├── templates/
│ └── static/
│
├── requirements.txt # Python dependencies
├── install.sh # Full deployment install script
├── deploy.sh # Deployment restart/update script (optional)
├── main.py # Flask entrypoint
└── .gitignore # Git ignore rules