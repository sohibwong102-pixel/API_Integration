#!/bin/bash

source .venv/bin/activate

if gum spin --spinner monkey --title "\rsabar jing..." -- sleep 5; then

echo -ne "\rPROJECT ACTIVATED😎"

else 
	echo -ne "\rDEPLOY FAILED"
	exit 1
fi

python main.py
