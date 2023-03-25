#!bin/bash

dir=$PWD
args="$@"

# remove all contents of directory result if it exists
if [ -d $dir/result ] 
then
    rm -r $dir/result/ 
fi

# create a directory "result" to store all the segmented words
mkdir -p $dir/result

# make a virtual environment
mkdir -p $dir/venv/
python3 -m venv $dir/venv/

# activate the virtual environment
source $dir/venv/bin/activate

# upgrade version of pip
python3 -m pip install --upgrade pip 1>/dev/null

# install all the dependencies
pip3 install opencv-python numpy 1>/dev/null

# run the python script
python3 main.py $args

# deactivate the virtual environment
deactivate
