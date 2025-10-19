# CpHMD_726564
For Aashni and Om

# Quick notes fr
1. This project assumes your CHARMM executable has the PHMD module enabled - its like pretty much standardized
2. Put your solvated system PDB or generate coordinates/PSF as needed before running.
3. Run:
4.  - `python generate_charmm_inputs.py --pdb my_cleaned.pdb --outdir cphmd_run --charmm_bin /full/path/to/charmm --ph 4.5`
    - `cd cphmd_run`
    -  - `./run_charmm.sh`
5. Outputs of interest:
   - `phmd_lambda_history.dat` (time series of lambda values)
   -  - `phmd_summary.txt`
   - `prod.log`
7. If CHARMM errors at any `phmd` command, copy the error message and share it, inputs are easily adjusted to your CHARMM build's exact syntax.

Important: a single pH simulation yields only the fraction at pH 4.5 — to estimate pKa robustly you normally need multiple pH points or pH-REX  but we alr yapped abt it and its not gonna be an issue apparently. Just text me if u have ?s
