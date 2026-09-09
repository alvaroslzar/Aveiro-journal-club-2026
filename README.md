<!--
Template designed for scientific articles workflow written in LaTeX with simulations and figure generation in Python.

Template author: Álvaro Salazar Cuadros
https://github.com/alvaroslzar
-->


# Aveiro journal club 2026

This is the repo for the project `Aveiro-journal-club-2026`

Authors: S. Noriji, S. D. Odintsov, D. Sáez-Chillón Gómez and Á. Salazar Cuadros (speaker).

Contribution: Horizon singularity, energy conditions and shadows in time-dependent and spherically symmetric spacetime [	arXiv:2608.15740 [gr-qc]](https://arxiv.org/abs/2608.15740).


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
├── LICENSE
├── README.md
├── latex
│   ├── figures
│   ├── main.tex
│   └── references.bib
├── requirements.txt
├── scripts
│   ├── build.py
│   └── setup-nb-filter.sh
└── src
    ├── generate_images.py
    ├── paper.mplstyle
    └── ray_tracing_WH.ipynb
```