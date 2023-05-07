#!/bin/bas
# ambiente virtual para instalar coisas
python3 -m venv .
# entrar no ambiente virtual
source bin/activate
# pip sempre desatualizado por alguma razao
pip install --upgrade pip
# instalar pacotes
pip install opencv-python numpy
python3 colors.py
