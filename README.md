<!--
Template designed for scientific articles workflow written in LaTeX with simulations and figure generation in Python.

Template author: Álvaro Salazar Cuadros
https://github.com/alvaroslzar
-->


# Aveiro journal club 2026

This repository contains the TEX source and Python scripts for the presentation given at the [journal club](https://gravitation.web.ua.pt/node/5700) on September 16, 2026 at University of Aveiro.
See [here](/ASC_Aveiro_journal_club.pdf) the PDF with the slides.

Speaker: Álvaro Salazar Cuadros

Authors: Shin’ichi Nojiri, Sergei D. Odintsov, Diego Sáez-Chillón Gómez, Álvaro Salazar Cuadros.

Paper: Horizon singularity, energy conditions and shadows in time-dependent and spherically symmetric spacetime [arXiv:2608.15740 [gr-qc]](https://arxiv.org/abs/2608.15740).


## Setup

### First time (one-time only)

Create a virtual environment and install the dependencies (macOS/Linux):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
```

### Every time after

Build the project by running the following script in the root directory:

```bash
python3 scripts/build.py
```


## Citation

The use of this work in scientific publications must be properly acknowledged.
Please cite the following:

**BibTeX**
```
@article{Nojiri:2026tjn,
    author = "Nojiri, Shin'ichi and Odintsov, Sergei D. and S{\'a}ez-Chill{\'o}n G{\'o}mez, Diego and Cuadros, {\'A}lvaro Salazar",
    title = "{Horizon singularity, energy conditions and shadows in time-dependent and spherically symmetric spacetime}",
    eprint = "2608.15740",
    archivePrefix = "arXiv",
    primaryClass = "gr-qc",
    reportNumber = "KEK-TH-2861, KEK-Cosmo-0429",
    month = "8",
    year = "2026"
}
```

## License

This work is licensed under a Creative Commons Attribution 4.0 International License ([CC BY 4.0](/LICENSE)).