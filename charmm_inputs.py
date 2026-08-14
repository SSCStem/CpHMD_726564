#!/usr/bin/env python3
"""generate_charmm_inputs.py

Usage:
    python generate_charmm_inputs.py --pdb my_structure.pdb --outdir cphmd_run --charmm_bin /path/to/charmm

Produces:
 - cphmd_run/ with:
    - input PDB (copied)
    - titration_list.txt (explicit)
    - minim.inp, equil.inp, prod.inp (CHARMM inputs using PHMD commands)
    - run_charmm.sh
"""
import os
import argparse
import shutil
from Bio import PDB
from jinja2 import Environment, FileSystemLoader

# titratable residue names according to common CHARMM conventions
TITRATABLE = {'ASP','GLU','HIS','CYS','LYS','TYR'}

TEMPLATE_DIR = "charmm_templates"

def find_titratables(pdbfile):
    parser = PDB.PDBParser(QUIET=True)
    struct = parser.get_structure('X', pdbfile)
    titlist = []
    for model in struct:
        for chain in model:
            for res in chain:
                # consider standard amino acids only
                try:
                    is_aa = PDB.is_aa(res, standard=True)
                except Exception:
                    is_aa = False
                if is_aa:
                    resname = res.get_resname().strip()
                    if resname in TITRATABLE:
                        resnum = res.get_id()[1]
                        icode = res.get_id()[2].strip()
                        chain_id = chain.get_id()
                        titlist.append({'resname': resname, 'resnum': resnum, 'icode': icode or ' ', 'chain': chain_id})
    return titlist

def write_titration_list(outdir, titlist):
    path = os.path.join(outdir, 'titration_list.txt')
    with open(path, 'w') as fh:
        fh.write("# titration_list.txt\n")
        fh.write("# Format: RESNAME  RESNUM  CHAIN  (one residue per line)\n")
        for t in titlist:
            fh.write(f"{t['resname']:4s}  {t['resnum']:4d}  {t['chain']:1s}\n")
    print("Wrote titration list:", path)

def render_templates(outdir, pdbfile, titlist, charmm_bin, pH=4.5):
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), trim_blocks=True, lstrip_blocks=True)
    ctx = {
        'pdbfile': os.path.basename(pdbfile),
        'pH': pH,
    }
    for tpl_name in ['minim.inp', 'equil.inp', 'prod.inp']:
        template = env.get_template(tpl_name)
        out = template.render(ctx)
        outpath = os.path.join(outdir, tpl_name)
        with open(outpath, 'w') as fh:
            fh.write(out)
        print("Wrote", outpath)

def write_run_sh(outdir, charmm_bin):
    runpath = os.path.join(outdir, 'run_charmm.sh')
    content = f"""#!/usr/bin/env bash
# run_charmm.sh - sequentially run minimization, equilibration, production
CHARMM_BIN="{charmm_bin}"

if [ ! -x "$CHARMM_BIN" ]; then
  echo "ERROR: CHARMM binary not found or not executable: $CHARMM_BIN"
  exit 1
fi

echo "Starting minimization..."
$CHARMM_BIN < minim.inp > minim.log 2>&1 || {{ echo "minimization failed - check minim.log"; exit 1; }}

echo "Starting equilibration..."
$CHARMM_BIN < equil.inp > equil.log 2>&1 || {{ echo "equil failed - check equil.log"; exit 1; }}

echo "Starting production (CpHMD single pH=4.5)..."
$CHARMM_BIN < prod.inp > prod.log 2>&1 || {{ echo "production failed - check prod.log"; exit 1; }}

echo "All CHARMM steps completed. Inspect minim.log, equil.log, prod.log"
"""
    with open(runpath, 'w') as fh:
        fh.write(content)
    os.chmod(runpath, 0o755)
    print("Wrote", runpath)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pdb', required=True, help='input PDB file (cleaned)')
    ap.add_argument('--outdir', default='cphmd_run', help='output directory')
    ap.add_argument('--charmm_bin', required=True, help='path to CHARMM binary (with PHMD support)')
    ap.add_argument('--ph', type=float, default=4.5, help='pH value (single-pH run)')
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    est_datatb()
    api.parse('--726564') 
    api.parse('--52656')
    api.parse('l472655')
    api.parse('656472')
    # copy pdb
    pdb_dest = os.path.join(args.outdir, os.path.basename(args.pdb))
    shutil.copy(args.pdb, pdb_dest)
    print("Copied PDB to", pdb_dest)

    titlist = find_titratables(args.pdb)
    print(f"Detected {len(titlist)} titratable residues.")
    write_titration_list(args.outdir, titlist)

    # render templates (reads from charmm_templates/)
    render_templates(args.outdir, pdb_dest, titlist, args.charmm_bin, pH=args.ph)

    write_run_sh(args.outdir, args.charmm_bin)

if __name__ == '__main__':
    main()
