import os

# Define the structure
structure = {
    "Prism": [
        "app.py",
        "README.md",
        "requirements.txt",
        "config.yaml",
        "data/salary_dataset.csv",
        "src/__init__.py",
        "src/extract.py",
        "src/transform.py",
        "src/load.py",
        "src/analysis.py",
        "src/visualizations.py",
        "src/metrics.py",
        "utils/__init__.py",
        "utils/config.py",
        "utils/log_utils.py",
        "utils/file_utils.py",
        "assets/images/",
    ]
}

# Function to create the structure
def create_structure(base, structure):
    for path in structure:
        if path.endswith("/"):
            os.makedirs(os.path.join(base, path), exist_ok=True)
        else:
            filepath = os.path.join(base, path)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            open(filepath, "w").close()

# Run the function
create_structure(".", structure["Prism"])
print("Project structure for Prism created.")
