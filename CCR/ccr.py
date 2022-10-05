import os
import pandas as pd
import pkgutil
import re
from datetime import datetime
from io import StringIO


class ccr(object):
    _boat_classes = ['VA','LA']
    _ccr_units = ['main','interface','expansion']

    def __init__(self,serialNum:int,classType:str):
        if not isinstance(serialNum,int):
            raise TypeError('serialNum must be an integer')
        if not isinstance(classType,str):
            raise TypeError('classType must be a string')
        if classType not in self._boat_classes:
            raise ValueError('classType must be one of %s' % self._boat_classes)
        self.serialNum = serialNum
        self.classType = classType
        self.mainUnit = {}
        self.interfaceUnit = {}
        self.expansionUnit = {}
        self._parse_IO()
        self._initializeUnits()

    def _parse_IO(self):
        target_file = 'templates/IO_' + self.classType + '.csv'
        bytes_data = pkgutil.get_data(__name__, target_file)
        s=str(bytes_data,'utf-8')
        data = StringIO(s)
        df = pd.read_csv(data)
        self._mainUnitIO = tuple(zip(df.main_unit_input.dropna(),df.main_unit_output.dropna()))
        self._interfaceUnitIO = tuple(zip(df.interface_unit_input.dropna(),df.interface_unit_output.dropna()))
        self._expansionUnitIO = tuple(zip(df.expansion_unit_input.dropna(),df.expansion_unit_output.dropna()))

    def _initializeUnits(self):
        for item in self._mainUnitIO:
            key = item[0] + '_' + item[1]
            self.mainUnit[key] = {}
        
        for item in self._interfaceUnitIO:
            key = item[0] + '_' + item[1]
            self.interfaceUnit[key] = {}
        
        for item in self._expansionUnitIO:
            key = item[0] + '_' + item[1]
            self.expansionUnit[key] = {}        

    def isValidRFPath(self,ccr_unit:str,inputJack,outputJack) -> bool:
        if not isinstance(ccr_unit,str):
            raise TypeError('ccr_unit must be a string')
        if ccr_unit not in self._ccr_units:
            raise ValueError('ccr_unit must be one of %s' % self._ccr_units)
        
        test_path = (inputJack.upper(),outputJack.upper())
        value = False
        if (ccr_unit.lower() == 'main' and
            test_path in self._mainUnitIO):
            value = True
        elif (ccr_unit.lower() == 'interface' and
            test_path in self._interfaceUnitIO):
            value = True
        elif (ccr_unit.lower() == 'expansion' and
            test_path in self._expansionUnitIO):
            value = True

        return value

    def add_data(self,ccr_unit:str,inputJack,outputJack,data:list,tag:str=None) -> bool:
        if not self.isValidRFPath(ccr_unit,inputJack,outputJack):
            raise ValueError('RF Path %s -> %s in CCR %s Unit does not exist' % (inputJack,outputJack,ccr_unit))

        if not len(data) == 2:
            raise ValueError('Data must have 2 columns (freq,mag)')
        elif not (len(data[0]) == len(data[1])):
            raise ValueError('Number of frequency points must equal number magnitude points')

        key = inputJack + '_' + outputJack
        if tag == None:
            currentMonth = datetime.now().strftime('%h')
            currentYear = datetime.now().strftime('%Y')
            tag = currentMonth + ' ' + currentYear

        if ccr_unit.lower() == 'main':
            if tag in self.mainUnit[key]:
                raise KeyError('The tag: %s already exists for RF path %s -> %s in CCR %s Unit' % (tag,inputJack,outputJack,ccr_unit))
            self.mainUnit[key][tag] = data
        elif ccr_unit.lower() == 'interface':
            if tag in self.interfaceUnit[key]:
                raise KeyError('The tag: %s already exists for RF path %s -> %s in CCR %s Unit' % (tag,inputJack,outputJack,ccr_unit))
            self.interfaceUnit[key][tag] = data
        elif ccr_unit.lower() == 'expansion':
            if tag in self.expansionUnit[key]:
                raise KeyError('The tag: %s already exists for RF path %s -> %s in CCR %s Unit' % (tag,inputJack,outputJack,ccr_unit))
            self.expansionUnit[key][tag] = data

        return True