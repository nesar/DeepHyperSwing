module load PrgEnv-nvidia cray-mpich craype-accel-nvidia80 python
module load cudatoolkit/12.2
module load cudnn/8.9.3_cuda12
conda activate dh_env_2024
export MPICH_GPU_SUPPORT_ENABLED=1 
