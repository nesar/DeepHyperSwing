#!/bin/bash
#SBATCH -A dasrepo_g
#SBATCH --job-name=ackley
#SBATCH -C gpu
#SBATCH -q regular
#SBATCH -t 1:00:00
#SBATCH --nodes=128
#SBATCH --gres=gpu:4

# User Configuration
INIT_SCRIPT=$PWD/activate-dhenv.sh

SLURM_JOBSIZE=128
RANKS_PER_NODE=4

# Initialization of environment
source $INIT_SCRIPT

srun -n $(( $SLURM_JOBSIZE * $RANKS_PER_NODE )) -N $SLURM_JOBSIZE python evaluator_mpi.py

echo "Complete"
