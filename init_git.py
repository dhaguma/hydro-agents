import subprocess
from pathlib import Path

GITIGNORE_CONTENT = """
# -----------------------------
# Python
# -----------------------------
__pycache__/
*.pyc
*.pyo
*.pyd
*.pkl
*.egg-info/
.venv/
.env/
.envrc
*.log

# uv environment + lock artifacts
.uv/
uv.lock.backup

# -----------------------------
# VS Code
# -----------------------------
.vscode/
!.vscode/agents/

# -----------------------------
# Hydrology Data (large files)
# -----------------------------
data/raw/
data/processed/era5/
data/processed/streamflow/

# Keep outputs but ignore large intermediates
data/outputs/calibration/*.csv
data/outputs/calibration/*.sqlite
data/outputs/calibration/*.db

# Forecast ensembles (can be huge)
data/outputs/forecasts/*_ensemble.csv

# Parameter files are small and useful
!data/outputs/parameters/*.json

# -----------------------------
# SPOTPY temporary files
# -----------------------------
*.csv
*.sqlite
*.db
spotpy_*

# -----------------------------
# OS / Editor junk
# -----------------------------
.DS_Store
Thumbs.db
"""

def init_git_repo(base=None):
    base_path = Path(base or ".").resolve()
    base_path.mkdir(parents=True, exist_ok=True)

    print(f"\n📁 Initializing Git repository in: {base_path.resolve()}\n")

    # Step 1 — Initialize repo only if not already initialized
    git_dir = base_path / ".git"
    if not git_dir.exists():
        subprocess.run(["git", "init", base], check=True)
        print("✔️  Git repository initialized")
    else:
        print("ℹ️  Git repository already exists — skipping init")

    # Step 2 — Create .gitignore inside repo
    gitignore_path = base_path / ".gitignore"
    gitignore_path.write_text(GITIGNORE_CONTENT.strip() + "\n")
    print(f"✔️  .gitignore created at {gitignore_path}")

    # Step 3 — Stage changes
    subprocess.run(["git", "-C", base, "add", ".gitignore"], check=True)

    # Step 4 — Commit only if there is something to commit
    result = subprocess.run(
        ["git", "-C", base, "status", "--porcelain"],
        capture_output=True,
        text=True
    )

    if result.stdout.strip():
        subprocess.run(
            ["git", "-C", base, "commit", "-m", "Initialize repository with hydrology-optimized .gitignore"],
            check=True
        )
        print("✔️  Initial commit created")
    else:
        print("ℹ️  Nothing to commit — working tree clean")

    print("\n🎉 Git repository is ready!\n")


if __name__ == "__main__":
    init_git_repo()
