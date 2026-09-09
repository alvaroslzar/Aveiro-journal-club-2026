import os
import numpy as np
from matplotlib import pyplot as plt


script_dir = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.abspath(os.path.join(script_dir, "..", "latex", "figures"))

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Generate plot
# plot_filename = 'name.pdf'
# savepath = os.path.abspath(os.path.join(OUTPUT_DIR, plot_filename))
# plt.savefig(savepath)