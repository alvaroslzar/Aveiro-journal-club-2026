<!--
Template designed for scientific articles workflow written in LaTeX with simulations and figure generation in Python.

Template author: Álvaro Salazar Cuadros
https://github.com/alvaroslzar
-->


# Draft title

This is the repo for the project `Draft title`

Authors: `author_name_1`, `author_name_2`, etc.


## Setup

### First time (one-time only)

Create a virtual environment and install the dependencies (macOS/Linux):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
bash scripts/setup-nb-filter.sh
```

### Every time after

Build the project by running the following script in the root directory:

```bash
python3 scripts/build.py
```


## File tree

To see the file tree, move to the root of the project and run
```bash
tree -A -I "*.pdf|*.bbl|*.synctex.gz"
```

Then, paste the output here
```bash
.
├── LICENSE
├── README.md
├── build.py
├── latex
│   ├── figures
│   ├── main.tex
│   └── references.bib
├── requirements.txt
└── src
    └── generate_images.py
```