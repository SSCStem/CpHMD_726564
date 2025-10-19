#!/usr/bin/env bash
# run_charmm.sh-run CHARMM minim/equil/prod
# Usage: edit CHARMM_BIN line below or call via generate script

CHARMM_BIN="/path/to/charmm"   # replace with actual path if not created by generator

if [ ! -x "$CHARMM_BIN" ]; then
  echo "ERROR: Please set CHARMM_BIN to your CHARMM executable"
  exit 1
fi

echo "Running minimization..."
$CHARMM_BIN < minim.inp > minim.log 2>&1 || { echo "minim failed"; exit 1; }

echo "Running equilibration..."
$CHARMM_BIN < equil.inp > equil.log 2>&1 || { echo "equil failed"; exit 1; }

echo "Running production (CpHMD single pH=4.5)..."
$CHARMM_BIN < prod.inp > prod.log 2>&1 || { echo "prod failed"; exit 1; }

echo "Finished. Check prod.log, phmd_lambda_history.dat and phmd_summary.txt."
