Swing (Argonne LCRC)
**********************

`Swing <https://www.lcrc.anl.gov/systems/resources/swing/>`_  is part of the Argonne Laboratory Computing Resource Center (LCRC), consisting of 6 public compute nodes with 8x NVIDIA A100 GPUS-per-node. See the `documentation <https://www.lcrc.anl.gov/for-users/using-lcrc/running-jobs/running-jobs-on-swing/>`_ of Swing for a detailed information on how to run jobs on Swing. 

.. _swing-module-installation:

Already installed module
========================

This installation procedure shows you how to access the installed DeepHyper module on Swing. 

After logging in Swing, connect to a GPU node:

.. code-block:: console

    $ salloc -p gpu -N 1 --gres=gpu:1 -t 1:00:00

Then, check the allocated node using ``squeue``. Say, the node allocated is gpu4. Next, log in to the allocated node.

.. code-block:: consoule
    
    $ ssh gpu4

Then, load the following modules:

.. code-block:: consoule

    $ module load gcc/9.2.0-r4tyw54 cuda/11.0.2-4szlv2t
    $ module load openmpi/4.1.0-cuda11.0.2-tyz7hlj
    $ module load cuda/11.2.1 cudnn/8.1.1.33


Conda environment
=================

This installation procedure shows you how to create your own Conda virtual environment.

 Create condo environment and install necessary packages

.. code-block:: console

	$ conda create -p env_dh --clone base
	$ conda activate env_dh
    
    
Developer installation
======================

Finally install DeepHyper in the previously created ``env_dh`` environment:

.. code-block:: console
    
    $ git clone https://github.com/deephyper/deephyper.git
    $ cd deephyper/ && git checkout develop
    $ pip install -e ".[dev,analytics]"


Finally, to verify the installation do:

.. code-block:: console

    $ python
    >>> import deephyper
    >>> deephyper.__version__
    '0.3.0'
