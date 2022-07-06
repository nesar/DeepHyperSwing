Swing (Argonne LCRC)
**********************

`Swing <https://www.lcrc.anl.gov/systems/resources/swing/>`_  is part of the Argonne Laboratory Computing Resource Center (LCRC), consisting of 6 public compute nodes with 8x NVIDIA A100 GPUS-per-node. See the `documentation <https://www.lcrc.anl.gov/for-users/using-lcrc/running-jobs/running-jobs-on-swing/>`_ for a detailed information on how to run jobs on Swing. 

.. _swing-module-installation:

Set-up to connect to Swing. 
========================

Open ~/.ssh/config file on your home computer. 

Dedicate a port for Swing (XXXX in this case). This port number will be required later.
Use your USERNAME and location of the SSH_KEY. The ssh key has to be saved on the LCRC `webpage <https://accounts.lcrc.anl.gov/>`_. 

.. code-block:: console

	$ Host swing
	$   HostName swing.lcrc.anl.gov
	$   User USERNAME
	$   IdentityFile ~/.ssh/SSH_KEY
	$   LocalForward XXXX localhost:XXXX
	$   ForwardX11Trusted yes

The setup only needs to be done once. For more details on using LCRC systems, check the documentation https://www.lcrc.anl.gov/for-users/getting-started/ssh/


DeepHyper Installation
========================

First, log in into Swing.

.. code-block:: console

    $ ssh swing

After logging in Swing, connect to a GPU node:

.. code-block:: console

    $ salloc -p gpu -N 1 --gres=gpu:1 -t 1:00:00

Then, check the allocated node using ``squeue``. Say, the node allocated is gpu4. Next, log in to the allocated node.

.. code-block:: consoule
    
    $ ssh gpu4

Copy and Paste the files ``dh_install.sh``, ``load_modules.sh`` and ``launch_notebook.sh`` on your folder on Swing, and then run the script.

.. code-block:: consoule
    
    $ source dh_install.sh
    
This script loads the necessary modules on required to use GPUs (GCC, CUDA, MPI), and creates a new conda environment, and installs the latest release version of DeepHyper (0.4.0) in the newly created environment. 



Running the installed DeepHyper
========================

Once DeepHyper is installed, one can use the deephyper after loading the modules and activating the conda environment. The ``gpuX`` corresponds to the allocated node (check via ``squeue``). 

.. code-block:: console

    $ salloc -p gpu -N 1 --gres=gpu:1 -t 1:00:00  
    $ ssh gpuX
    $ source load_modules.sh
   
Finally, to verify the installation do:

.. code-block:: console

    $ python
    >>> import deephyper
    >>> deephyper.__version__
    '0.4.0'
    
 
 
Using Jupyter notebook on Swing
========================

The follwing 2 steps have to be followed to run jupyter kernel on Swing GPU. The following procedue only works for a single node job (one can use all the 8 GPUs in the node, depending on the allocation).  

1. Start the remote Jupyter kernel without interface.

	* Open the first terminal and run the usual commands to log-in to an allocated node. 

	.. code-block:: console

	   $ ssh swing
	   $ salloc -p gpu -N 1 --gres=gpu:1 -t 1:00:00
	   $ ssh gpuX

	* Run the Jupyter kernel after ssh-ing into the GPU node. 

	.. code-block:: console

	   $ source launch_notebook.sh

	This initiates a JupyterLab kernel without an iterface. Copy the notebook URL generated from the Jupyter kernel. 

2. Forward the remote port to the local port. 

	* Open the second terminal for porting the display to our workstation. 

	.. code-block:: console

	   $ ssh -L XXXX:localhost:XXXX swing
	   $ ssh -L XXXX:localhost:XXXX gpuX

	* The URL can be pasted on your browser. Any notebook can be opened with the JupyterLab, with access to Swing GPUs for executions. 
 
