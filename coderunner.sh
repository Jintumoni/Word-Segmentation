#!bin/bash

dir=$PWD
filename=$1

mkdir -p $dir/venv/

# make a virtual environment
python3 -m venv $dir/venv/

# activate the virtual environment
source $dir/venv/bin/activate

# upgrade version of pip
python3 -m pip install --upgrade pip 1>/dev/null

# install all the dependencies
pip3 install opencv-python numpy 1>/dev/null

# run the python script
python3 main.py $filename

# deactivate the virtual environment
deactivate
