LOAD_SCRIPT=$PWD/load_modules.sh
source $LOAD_SCRIPT

conda activate dh_test
jupyter lab --no-browser --port=6933
