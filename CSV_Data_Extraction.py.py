# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
import pandas as pd
from pathlib import Path



# Defining CSV Names (Input)

EnergyTimeCSVName = 'test1.csv'
DetectorPositionCSVName = 'test2.csv'
DetectorPairingCSVName = 'test3.csv'


BaseLocation = str(Path("C:/Users/chris/Documents/Medical_Physics_Group_Study/Lab_CSVs"))
EnergyTimeCSV = BaseLocation + "\\" + EnergyTimeCSVName
DetectorPositionCSV = BaseLocation + "\\" + DetectorPositionCSVName
DetectorPairingCSV = BaseLocation + "\\" + DetectorPairingCSVName



EnergyTimeDF = pd.read_csv(EnergyTimeCSV, sep=';')
DetectorPositionDF = pd.read_csv(DetectorPositionCSV, sep=';')
DetectorPairingDF = pd.read_csv(DetectorPairingCSV, sep=';')