LOAD_SCRIPT=$PWD/load_modules.sh
source $LOAD_SCRIPT

conda create -p dh_test --clone base
conda activate dh_test

#INSTALL LATEST RELEASE VERSION 
pip install deephyper==0.4.0
pip install tensorflow

#DOWNLOAD AND INSTALL DEEPHYPER

#git clone https://github.com/deephyper/deephyper.git
#cd deephyper/ && git checkout develop
#pip install -e ".[dev,analytics]"