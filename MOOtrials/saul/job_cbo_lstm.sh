#!/bin/bash
#SBATCH -A dasrepo_g
#SBATCH --job-name=cbo_lstm
#SBATCH -C gpu
#SBATCH -q regular
#SBATCH -t 1:00:00
#SBATCH --ntasks-per-node=4
#SBATCH --gpus-per-task=1
#SBATCH --nodes=2
#SBATCH --ntasks=8
#SBATCH --gpus=8


# User Configuration
INIT_SCRIPT=$PWD/activate-dhenv.sh

SLURM_JOBSIZE=2
RANKS_PER_NODE=4

# Initialization of environment
source $INIT_SCRIPT


srun -n $(( $SLURM_JOBSIZE * $RANKS_PER_NODE )) -G $(( $SLURM_JOBSIZE * $RANKS_PER_NODE )) -N $SLURM_JOBSIZE --gpus-per-task 1 --ntasks-per-node 4 python evaluator_mpi.py


echo "Complete"

