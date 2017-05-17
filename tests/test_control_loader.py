# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 17:28:04 2015

@author: 108630
"""

import pytest

from aneris.control.simulation import Loader
from aneris.control.data import DataStorage

import data_plugins
from data_plugins.definitions import UnitData

@pytest.fixture(scope="module")
def loader():
    
    data_store = DataStorage(data_plugins)
    loader = Loader(data_store)
    
    return loader

def test_init_loader(loader):
    
    assert isinstance(loader, Loader)
    
def test_get_structure(loader):
    
    unitdata = loader.get_structure("UnitData")
    
    assert isinstance(unitdata, UnitData)
