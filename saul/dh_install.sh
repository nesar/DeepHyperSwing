# https://docs.nersc.gov/development/languages/python/using-python-perlmutter/#building-cuda-aware-mpi4py

module load PrgEnv-nvidia cudatoolkit python
module load cudnn/8.2.0
conda create -n dh python=3.9 -y
conda activate dh
conda install gxx_linux-64 gcc_linux-64
MPICC="cc -target-accel=nvidia80 -shared" CC=nvc CFLAGS="-noswitcherror" pip install --force --no-cache-dir --no-binary=mpi4py mpi4py
pip install deephyper==0.4.0
pip install tensorflow

pip install kiwisolver
pip install cycler
