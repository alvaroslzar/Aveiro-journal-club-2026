#!/usr/bin/env python
"""Build script: Generate images and build PDF."""

import subprocess
import sys
import time
from pathlib import Path
import os

def run_cmd(cmd, desc, quiet=False, announce=True):
    """Run shell command and report status."""
    if announce:
        print(f"Running: {desc}")
    try:
        subprocess.run(cmd, check=True,
                      stdout=subprocess.DEVNULL if quiet else None,
                      stderr=subprocess.DEVNULL if quiet else None)
        if announce:
            print(f"✓ {desc} completed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"✗ {desc} failed: {e}")
        return False

def install_deps(requirements_path):
    """Install dependencies from requirements.txt if not already installed."""
    try:
        import numpy  # noqa: F401
        import matplotlib  # noqa: F401
    except ImportError:
        print("Installing dependencies from requirements.txt...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r",
                        str(requirements_path)], check=True)
        print("✓ Dependencies installed")


def main():
    start = time.time()
    base = Path(__file__).parent

    install_deps(base / "requirements.txt")

    gen_script = base / "src" / "generate_images.py"
    if not gen_script.exists():
        print(f"Error: {gen_script} not found"); sys.exit(1)
    if not run_cmd([sys.executable, str(gen_script)], "Image generation"):
        sys.exit(1)

    latex_dir = base / "latex"
    main_tex = latex_dir / "main.tex"
    if not main_tex.exists():
        print(f"Error: {main_tex} not found"); sys.exit(1)

    os.chdir(latex_dir)
    print("Running: Build PDF")
    for cmd in [
        ["pdflatex", "-interaction=nonstopmode", "-synctex=1", "main.tex"],
        ["bibtex", "main"],
        ["pdflatex", "-interaction=nonstopmode", "-synctex=1", "main.tex"],
        ["pdflatex", "-interaction=nonstopmode", "-synctex=1", "main.tex"],
    ]:
        if not run_cmd(cmd, "Build PDF", quiet=True, announce=False):
            sys.exit(1)
    print("✓ Build PDF completed")

    for ext in ['.aux', '.log', '.out', '.toc', '.lot', '.lof', '.fls', '.blg', '.fdb_latexmk']:
        (latex_dir / f"main{ext}").unlink(missing_ok=True)

    elapsed = time.time() - start
    print(f"\nBuilt project successfully in {elapsed:.2f} s.")

if __name__ == "__main__":
    main()
