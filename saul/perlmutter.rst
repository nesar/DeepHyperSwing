
4x NVIDIA A100 GPUs


SSH config: https://docs.nersc.gov/connect/mfa/#ssh-configuration-file-options





Perlmutter (Argonne LCRC)
**********************

Perlmutter, a HPE Cray EX supercomputer at NERSC, is a heterogeneous system with both GPU-accelerated and CPU-only nodes. 


Connect to Perlmutter. 
========================

For SSH configuration, check documentation https://docs.nersc.gov/systems/perlmutter/#connecting-to-perlmutter. One can connect to Perlmutter via terminal.

.. code-block:: console

    $ ssh <username>@perlmutter-p1.nersc.gov


DeepHyper Installation
========================

After logging in Perlmutter, use the `installation script <https://github.com/nesar/DeepHyperSwing/blob/main/saul/dh_install.sh>`_ provided to install DeepHyper and the associated dependencies. Download the file and run ``source dh_install.sh`` on the terminal. 

The script first loads the Perlmutter modules, including cuDNN. 

.. code-block:: console

    $ module load PrgEnv-nvidia cudatoolkit python
    $ module load cudnn/8.2.0

Next, we create a conda environment and install DeepHyper. 

.. code-block:: console

    $ conda create -n dh python=3.9 -y
    $ conda activate dh
    $ conda install gxx_linux-64 gcc_linux-64


The crucial step is to install CUDA aware mpi4py, following the instructions given in the documentation. `[mpi4py] <https://docs.nersc.gov/development/languages/python/using-python-perlmutter/#building-cuda-aware-mpi4py>`_

.. code-block:: console

    $ MPICC="cc -target-accel=nvidia80 -shared" CC=nvc CFLAGS="-noswitcherror" pip install --force --no-cache-dir --no-binary=mpi4py mpi4py

Finally we install deephyper and other packages. 

.. code-block:: console

    $ pip install deephyper==0.4.0
    $ pip install tensorflow
    $ pip install kiwisolver
    $ pip install cycler



Running the installed DeepHyper
========================

Once DeepHyper is installed, one can use the deephyper after loading the modules and activating the conda environment. For the LSTM example for SST data, first copy and Paste the following scripts `load_modules.sh <https://github.com/nesar/DeepHyperSwing/blob/main/saul/load_modules.sh>`_, `common.py <https://github.com/nesar/DeepHyperSwing/blob/main/saul/common.py>`_, `evaluator_mpi.py <https://github.com/nesar/DeepHyperSwing/blob/main/saul/evaluator_mpi.py>`_,  `sst.py <https://github.com/nesar/DeepHyperSwing/blob/main/saul/sst.py>`_ and  `job_submit.sh <https://github.com/nesar/DeepHyperSwing/blob/main/saul/job_submit.sh>`_ on your folder on Perlmutter. 


 
 
Using Jupyter notebook on Perlmutter
========================

NERSC also allows for launching jupyter kernel on Perlmutter. One can visit `jupyer.nersc.gov <https://jupyter.nersc.gov/>`_ and select Exclusive GPU node or a configurable GPU node (up to 4 GPU nodes, with 4 GPUs each). 
 
