#!/bin/bash

export PYTHONPATH=$PYTHONPATH:/lib/python
export PYTHONPATH=$PYTHONPATH:$HOME/lib/python

python /home/steyou14/sentimental/populate_data_from_stream.py
