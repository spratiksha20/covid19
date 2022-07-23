#!/bin/bash
rm -rf Data/*
echo "Data cleared from Data Folder."
cd Scripts/
ipython DataFetch.py
echo " "
echo "Executed DataFetch. Data folder populated."
ipython DataPreprocess.py
echo "Executed DataPreprocess."
ipython DataProc.py
echo "Executed Data Processing. Files ready for analysis."
cd ..