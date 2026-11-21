#!/bin/bash
#SBATCH --job-name=cs886-project
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=2
#SBATCH --mem=10G
#SBATCH --time=00:15:00
#SBATCH --output=slurm-%j.output

#SBATCH --mail-user=xaliferi@uwaterloo.ca
#SBATCH --mail-type=ALL

set -e
source /opt/anaconda3/bin/activate cs886
python -u quickstart.py