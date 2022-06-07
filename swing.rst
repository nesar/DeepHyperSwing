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

Then, check the allocated node using squeue

.. code-block:: consoule
    $ ssh gpu4

Then, to access Deephyper run the following commands:

.. code-block:: consoule

    $ module load conda/2021-09-22
    $ conda activate base

Finally, to verify the installation do:

.. code-block:: console

    $ python
    >>> import deephyper
    >>> deephyper.__version__
    '0.3.0'

.. _thetagpu-conda-environment:

Conda environment
=================

This installation procedure shows you how to create your own Conda virtual environment and install DeepHyper in it.

.. admonition:: Storage/File Systems
    :class: dropdown, important

    It is important to run the following commands from the appropriate storage space because some features of DeepHyper can generate a consequante quantity of data such as model checkpointing. The storage spaces available at the ALCF are:

    - ``/lus/grand/projects/``
    - ``/lus/eagle/projects/``
    - ``/lus/theta-fs0/projects/``

    For more details refer to `ALCF Documentation <https://www.alcf.anl.gov/support-center/theta/theta-file-systems>`_.

After logging in Theta, locate yourself on one of the ThetaGPU service node (``thetagpusnX``) and move to your project folder (replace ``PROJECTNAME`` by your own project name):

.. code-block:: console

    $ ssh thetagpusn1
    $ cd /lus/theta-fs0/projects/PROJECTNAME

Then create the ``dhgpu`` environment:

.. code-block:: console

    $ module load conda/2021-09-22
    $ conda create -p dhgpu --clone base
    $ conda activate dhgpu/

Finally install DeepHyper in the previously created ``dhgpu`` environment:

.. code-block:: console

    $ pip install pip --upgrade
    $ # DeepHyper + Analytics Tools (Parsing logs, Plots, Notebooks)
    $ pip install deephyper["analytics"]


Developer installation
======================

Follow the :ref:`thetagpu-conda-environment` installation and replace ``pip install deephyper[analytics]`` by:

.. code-block:: console

    $ git clone https://github.com/deephyper/deephyper.git
    $ cd deephyper/ && git checkout develop
    $ pip install -e ".[dev,analytics]"


Internet Access
===============

If the node you are on does not have outbound network connectivity, set the following to access the proxy host:

.. code-block:: console

    $ export http_proxy=http://proxy.tmi.alcf.anl.gov:3128
    $ export https_proxy=http://proxy.tmi.alcf.anl.gov:3128
