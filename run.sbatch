#!/bin/bash
#SBATCH --job-name=cs886-project
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=2
#SBATCH --mem=10G
#SBATCH --time=05:00:00
#SBATCH --output=./output/slurm-%j.output

set -e
source /opt/anaconda3/bin/activate cs886
python -u main.py