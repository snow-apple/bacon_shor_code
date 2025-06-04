#!/bin/bash

#SBATCH --partition=scavenge
#SBATCH --time=23:55:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=shwetlana.jha@yale.edu
#SBATCH --array=1-4
#SBATCH --mem-per-cpu=4GB
#SBATCH --job-name=hy_tcnot

# Define parameter ranges
ds=3
de=10
dd=2
ps=0.01
pe=0.2
dp=0.0038
bp=0
ns=500

# Set the Slurm job array ID as a variable
JOB_ARRAY_ID=$SLURM_ARRAY_TASK_ID

# use python
module load miniconda
conda activate bs
#Run the python file with the current parameter values
python mle.py "$ds" "$de" "$dd" "$ps" "$pe" "$dp" "$ns" "$JOB_ARRAY_ID"
