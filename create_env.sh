#!/bin/bash

python3 -m venv .venv
source .venv/bin/activate

pip install --upgrade pip

pip install numpy pandas scipy spotpy
pip install git+https://github.com/amacd31/gr4j.git
pip install git+https://github.com/hydrologie/hsamiplus.git
