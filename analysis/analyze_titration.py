#!/usr/bin/env python3
"""analyze_titration.py
Assumes phmd_lambda_history.dat is whitespace-separated:
time  lambda_res1  lambda_res2 ...
Please just adapt this parser if your CHARMM produces a different layout.
"""
import numpy as np
import os
import sys
import matplotlib.pyplot as plt

fname = 'phmd_lambda_history.dat'
if not os.path.exists(fname):
    print("File not found:", fname)
    sys.exit(1)

data = np.loadtxt(fname)
# first column time, rest are lambda vals
times = data[:,0]
lambdas = data[:,1:]
nsteps, nres = lambdas.shape

fractions = np.mean(lambdas > 0.5, axis=0)  # fraction deprot if lambda ~1 is deprot
for i, frac in enumerate(fractions, 1):
    print(f"Residue {i}: fraction deprotonated = {frac:.3f}")

# "it's for the plot"
plt.figure(figsize=(max(6, nres*0.3),4))
plt.bar(range(1,nres+1), fractions)
plt.xlabel('Titratable residue index (order in titration_list.txt)')
plt.ylabel('Fraction deprotonated (lambda > 0.5)')
plt.tight_layout()
plt.savefig('fraction_deprot.png', dpi=200)
print("Saved fraction_deprot.png")
