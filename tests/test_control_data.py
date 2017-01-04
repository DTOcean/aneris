# -*- coding: utf-8 -*-
"""py.test tests on control.data module

.. moduleauthor:: Mathew Topper <mathew.topper@tecnalia.com>
"""

import pytest

import os
import sys
import shutil
import pickle

from aneris.boundary.data import SerialBox
from aneris.control.data import DataValidation, DataStorage
from aneris.entity.data import DataCatalog, DataPool, DataState, Data
from aneris.utilities.files import mkdir_p
from polite.paths import user_data_dir, module_dir

import data_plugins as data
import user_plugins as user_data

def test_discover_plugins():

    super_cls='DataDefinition'

    validation = DataValidation()

    # Discover the available classes and load the instances
    cls_map = validation._discover_plugins(data, super_cls)

    assert 'testDefinition' in cls_map.keys()

#def test_update_data_catalog_from_definitions():
#
#    '''Test retrieving all variables from data catalog definition files'''
#
#    # Test using files in AppData
#    test_app_dir = "yaml"
#    test_file_dir = "user_data"
#    test_file_name = "test.yaml"
#
#    app_path = user_data_dir("aneris", "DTOcean")
#    data_path = os.path.join(app_path, test_app_dir)
#    mkdir_p(data_path)
#    current_module = sys.modules[__name__]
#    test_yaml_file = os.path.join(module_dir(current_module),
#                                  test_file_dir,
#                                  test_file_name)
#    dst_path = os.path.join(data_path, test_file_name)
#    shutil.copyfile(test_yaml_file, dst_path)
#
#    catalog = DataCatalog()
#    validation = DataValidation()
#    catalog = validation.update_data_catalog_from_definitions(catalog,
#                                                              user_data)
#    all_vars = catalog.get_variable_identifiers()
#
#    shutil.rmtree(data_path)
#
#    assert 'my:test:variable2' in all_vars

def test_get_valid_variables():

    '''Test comparing variables in the interfaces to the data catalog'''

    all_vars = ['my:test:variable', 'site:wave:dir']

    catalog = DataCatalog()
    validation = DataValidation(meta_cls=data.MyMetaData)
    validation.update_data_catalog_from_definitions(catalog, data)

    valid_vars = validation.get_valid_variables(catalog, all_vars)

    assert 'my:test:variable' in valid_vars
    
def test_create_new_datastate():
    
    catalog = DataCatalog()
    validation = DataValidation(meta_cls=data.MyMetaData)
    validation.update_data_catalog_from_definitions(catalog, data)
    data_store = DataStorage(data)
    state = data_store.create_new_datastate("test")
    
    assert isinstance(state, DataState)  
    assert state.get_level() == "test"

def test_create_new_data():

    catalog = DataCatalog()
    validation = DataValidation(meta_cls=data.MyMetaData)
    validation.update_data_catalog_from_definitions(catalog, data)
    data_store = DataStorage(data)
    pool = DataPool()
    state = data_store.create_new_datastate("test")

    # Get the meta data from the catalog
    metadata = catalog.get_metadata("Technology:Common:DeviceType")
    
    data_store.create_new_data(pool, state, catalog, "Tidal", metadata)
    new_data_value = data_store.get_data_value(pool,
                                               state,
                                               "Technology:Common:DeviceType")

    assert new_data_value == "Tidal"
    
def test_create_new_none_data():

    catalog = DataCatalog()
    validation = DataValidation(meta_cls=data.MyMetaData)
    validation.update_data_catalog_from_definitions(catalog, data)
    data_store = DataStorage(data)
    pool = DataPool()
    state = data_store.create_new_datastate("test")

    # Get the meta data from the catalog
    metadata = catalog.get_metadata("Technology:Common:DeviceType")
    
    data_store.create_new_data(pool, state, catalog, None, metadata)
                                             
    with pytest.raises(ValueError):

        data_store.get_data_value(pool,
                                  state,
                                  "Technology:Common:DeviceType")
    
    assert len(pool) == 0
                                  
def test_remove_data_from_state():

    catalog = DataCatalog()
    validation = DataValidation(meta_cls=data.MyMetaData)
    validation.update_data_catalog_from_definitions(catalog, data)
    data_store = DataStorage(data)
    pool = DataPool()
    state = data_store.create_new_datastate("test")

    # Get the meta data from the catalog
    metadata = catalog.get_metadata("Technology:Common:DeviceType")
    
    data_store.create_new_data(pool, state, catalog, "Tidal", metadata)
    new_data_value = data_store.get_data_value(pool,
                                               state,
                                               "Technology:Common:DeviceType")

    assert new_data_value == "Tidal"
    
    data_store.remove_data_from_state(pool,
                                      state,
                                      "Technology:Common:DeviceType")
                                         
    assert data_store.has_data(state, "Technology:Common:DeviceType") == False
    assert state.has_index("Technology:Common:DeviceType") == False
    assert len(pool) == 0
    
def test_remove_none_data_from_state():

    catalog = DataCatalog()
    validation = DataValidation(meta_cls=data.MyMetaData)
    validation.update_data_catalog_from_definitions(catalog, data)
    data_store = DataStorage(data)
    pool = DataPool()
    state = data_store.create_new_datastate("test")

    # Get the meta data from the catalog
    metadata = catalog.get_metadata("Technology:Common:DeviceType")
    
    data_store.create_new_data(pool, state, catalog, None, metadata)
                                     
    assert data_store.has_data(state, "Technology:Common:DeviceType") == False
    assert state.has_index("Technology:Common:DeviceType") == True
    assert len(pool) == 0

    data_store.remove_data_from_state(pool,
                                      state,
                                      "Technology:Common:DeviceType")
                                         
    assert data_store.has_data(state, "Technology:Common:DeviceType") == False
    assert state.has_index("Technology:Common:DeviceType") == False
    assert len(pool) == 0
    
def test_copy_datastate():
    
    catalog = DataCatalog()
    validation = DataValidation(meta_cls=data.MyMetaData)
    validation.update_data_catalog_from_definitions(catalog, data)
    data_store = DataStorage(data)
    pool = DataPool()
    state = data_store.create_new_datastate("test")

    # Get the meta data from the catalog
    metadata = catalog.get_metadata("Technology:Common:DeviceType")
    
    data_store.create_new_data(pool, state, catalog, "Tidal", metadata)
    data_value = data_store.get_data_value(pool,
                                           state,
                                           "Technology:Common:DeviceType")
    data_index = state.get_index("Technology:Common:DeviceType")

    assert data_value == "Tidal"
    assert len(pool) == 1
    assert pool._links[data_index] == 1
    
    new_state = data_store.copy_datastate(pool, state)
    new_data_value = data_store.get_data_value(pool,
                                               new_state,
                                               "Technology:Common:DeviceType")
    
    assert isinstance(new_state, DataState)
    assert new_state is not state
    assert new_state.get_level() == "test"                                         
    assert new_data_value == "Tidal"
    assert len(pool) == 1
    assert pool._links[data_index] == 2
    
def test_serialise_data(tmpdir):

    catalog = DataCatalog()
    validation = DataValidation(meta_cls=data.MyMetaData)
    validation.update_data_catalog_from_definitions(catalog, data)
    data_store = DataStorage(data)
    pool = DataPool()
    state = DataState("test")
    data_store.discover_structures(data)
    
    metadata = catalog.get_metadata("Technology:Common:DeviceType")
    data_store.create_new_data(pool, state, catalog, "Tidal", metadata)
    
    data_index = state.get_index("Technology:Common:DeviceType")

    data_store.serialise_data(pool,
                              [data_index],
                              str(tmpdir))
                                     
    data_box = pool.get(data_index)

    assert isinstance(data_box, SerialBox)

    data_path = data_box.load_dict["file_path"]

    assert os.path.isfile(data_path)
    
def test_deserialise_data(tmpdir):

    catalog = DataCatalog()
    validation = DataValidation(meta_cls=data.MyMetaData)
    validation.update_data_catalog_from_definitions(catalog, data)
    data_store = DataStorage(data)
    pool = DataPool()
    state = DataState("test")
    data_store.discover_structures(data)
    
    metadata = catalog.get_metadata("Technology:Common:DeviceType")
    data_store.create_new_data(pool, state, catalog, "Tidal", metadata)
    
    data_index = state.get_index("Technology:Common:DeviceType")
    new_data = pool.get(data_index)
    
    data_store.serialise_data(pool,
                              [data_index],
                              str(tmpdir))
                              
    data_store.deserialise_data(catalog, pool, [data_index])
    new_data = pool.get(data_index)

    assert isinstance(new_data, Data)
    assert new_data._data == "Tidal"
    
def test_serialise_data_root(tmpdir):

    catalog = DataCatalog()
    validation = DataValidation(meta_cls=data.MyMetaData)
    validation.update_data_catalog_from_definitions(catalog, data)
    data_store = DataStorage(data)
    pool = DataPool()
    state = DataState("test")
    data_store.discover_structures(data)
    
    metadata = catalog.get_metadata("Technology:Common:DeviceType")
    data_store.create_new_data(pool, state, catalog, "Tidal", metadata)
    
    data_index = state.get_index("Technology:Common:DeviceType")

    data_store.serialise_data(pool,
                              [data_index],
                              str(tmpdir),
                              root_dir=str(tmpdir))
                                     
    data_box = pool.get(data_index)

    assert isinstance(data_box, SerialBox)

    data_path = os.path.join(str(tmpdir), data_box.load_dict["file_path"])

    assert os.path.isfile(data_path)
    
def test_deserialise_data_root(tmpdir):

    catalog = DataCatalog()
    validation = DataValidation(meta_cls=data.MyMetaData)
    validation.update_data_catalog_from_definitions(catalog, data)
    data_store = DataStorage(data)
    pool = DataPool()
    state = DataState("test")
    data_store.discover_structures(data)
    
    metadata = catalog.get_metadata("Technology:Common:DeviceType")
    data_store.create_new_data(pool, state, catalog, "Tidal", metadata)
    
    data_index = state.get_index("Technology:Common:DeviceType")
    new_data = pool.get(data_index)
    
    data_store.serialise_data(pool,
                              [data_index],
                              str(tmpdir),
                              root_dir=str(tmpdir))
                              
    data_store.deserialise_data(catalog,
                                pool,
                                [data_index],
                                root_dir=str(tmpdir))
    new_data = pool.get(data_index)

    assert isinstance(new_data, Data)
    assert new_data._data == "Tidal"
    
def test_serialise_pool(tmpdir):

    catalog = DataCatalog()
    validation = DataValidation(meta_cls=data.MyMetaData)
    validation.update_data_catalog_from_definitions(catalog, data)
    data_store = DataStorage(data)
    pool = DataPool()
    state = DataState("test")
    data_store.discover_structures(data)
    
    metadata = catalog.get_metadata("Technology:Common:DeviceType")
    data_store.create_new_data(pool, state, catalog, "Tidal", metadata)
    
    data_index = state.get_index("Technology:Common:DeviceType")

    data_store.serialise_pool(pool,
                              str(tmpdir))
                                     
    data_box = pool.get(data_index)

    assert isinstance(data_box, SerialBox)

    data_path = data_box.load_dict["file_path"]

    assert os.path.isfile(data_path)
    
def test_deserialise_pool(tmpdir):

    catalog = DataCatalog()
    validation = DataValidation(meta_cls=data.MyMetaData)
    validation.update_data_catalog_from_definitions(catalog, data)
    data_store = DataStorage(data)
    pool = DataPool()
    state = DataState("test")
    data_store.discover_structures(data)
    
    metadata = catalog.get_metadata("Technology:Common:DeviceType")
    data_store.create_new_data(pool, state, catalog, "Tidal", metadata)
    
    data_index = state.get_index("Technology:Common:DeviceType")
    new_data = pool.get(data_index)
    
    data_store.serialise_pool(pool,
                              str(tmpdir))
                              
    data_store.deserialise_pool(catalog, pool)
    new_data = pool.get(data_index)

    assert isinstance(new_data, Data)
    assert new_data._data == "Tidal"
    
def test_serialise_pool_root(tmpdir):

    catalog = DataCatalog()
    validation = DataValidation(meta_cls=data.MyMetaData)
    validation.update_data_catalog_from_definitions(catalog, data)
    data_store = DataStorage(data)
    pool = DataPool()
    state = DataState("test")
    data_store.discover_structures(data)
    
    metadata = catalog.get_metadata("Technology:Common:DeviceType")
    data_store.create_new_data(pool, state, catalog, "Tidal", metadata)
    
    data_index = state.get_index("Technology:Common:DeviceType")

    data_store.serialise_pool(pool,
                              str(tmpdir),
                              root_dir=str(tmpdir))
                                     
    data_box = pool.get(data_index)

    assert isinstance(data_box, SerialBox)

    data_path = os.path.join(str(tmpdir), data_box.load_dict["file_path"])

    assert os.path.isfile(data_path)
    
def test_deserialise_pool_root(tmpdir):

    catalog = DataCatalog()
    validation = DataValidation(meta_cls=data.MyMetaData)
    validation.update_data_catalog_from_definitions(catalog, data)
    data_store = DataStorage(data)
    pool = DataPool()
    state = DataState("test")
    data_store.discover_structures(data)
    
    metadata = catalog.get_metadata("Technology:Common:DeviceType")
    data_store.create_new_data(pool, state, catalog, "Tidal", metadata)
    
    data_index = state.get_index("Technology:Common:DeviceType")
    new_data = pool.get(data_index)
    
    data_store.serialise_pool(pool,
                              str(tmpdir),
                              root_dir=str(tmpdir))
                              
    data_store.deserialise_pool(catalog, pool, root_dir=str(tmpdir))
    new_data = pool.get(data_index)

    assert isinstance(new_data, Data)
    assert new_data._data == "Tidal"

def test_save_pool(tmpdir):
    
    "Try pickling a DataPool"

    catalog = DataCatalog()
    validation = DataValidation(meta_cls=data.MyMetaData)
    validation.update_data_catalog_from_definitions(catalog, data)
    data_store = DataStorage(data)
    pool = DataPool()
    state = DataState("test")
    data_store.discover_structures(data)
    
    metadata = catalog.get_metadata("Technology:Common:DeviceType")
    data_store.create_new_data(pool, state, catalog, "Tidal", metadata)
    
    data_index = state.get_index("Technology:Common:DeviceType")

    data_store.serialise_pool(pool,
                              str(tmpdir))
                                     
    data_box = pool.get(data_index)

    assert isinstance(data_box, SerialBox)

    test_path = os.path.join(str(tmpdir), "pool.pkl")
    pickle.dump(pool, open(test_path, "wb"), -1)
    
    assert os.path.isfile(test_path)
    
def test_load_pool(tmpdir):
    
    "Try unpickling a DataPool"

    catalog = DataCatalog()
    validation = DataValidation(meta_cls=data.MyMetaData)
    validation.update_data_catalog_from_definitions(catalog, data)
    data_store = DataStorage(data)
    pool = DataPool()
    state = DataState("test")
    data_store.discover_structures(data)
    
    metadata = catalog.get_metadata("Technology:Common:DeviceType")
    data_store.create_new_data(pool, state, catalog, "Tidal", metadata)
    
    data_index = state.get_index("Technology:Common:DeviceType")
    new_data = pool.get(data_index)
    
    data_store.serialise_pool(pool,
                              str(tmpdir))
    
    test_path = os.path.join(str(tmpdir), "pool.pkl")
    pickle.dump(pool, open(test_path, "wb"), -1)
    
    assert os.path.isfile(test_path)
    
    loaded_pool = pickle.load(open(test_path, "rb"))
                              
    data_store.deserialise_pool(catalog, loaded_pool)
    new_data = loaded_pool.get(data_index)

    assert isinstance(new_data, Data)
    assert new_data._data == "Tidal"
    
def test_load_pool_root(tmpdir):
    
    "Try unpickling a DataPool using a root directory"

    catalog = DataCatalog()
    validation = DataValidation(meta_cls=data.MyMetaData)
    validation.update_data_catalog_from_definitions(catalog, data)
    data_store = DataStorage(data)
    pool = DataPool()
    state = DataState("test")
    data_store.discover_structures(data)
    
    metadata = catalog.get_metadata("Technology:Common:DeviceType")
    data_store.create_new_data(pool, state, catalog, "Tidal", metadata)
    
    data_index = state.get_index("Technology:Common:DeviceType")
    new_data = pool.get(data_index)
    
    data_store.serialise_pool(pool,
                              str(tmpdir),
                              root_dir=str(tmpdir))
    
    test_path = os.path.join(str(tmpdir), "pool.pkl")
    pickle.dump(pool, open(test_path, "wb"), -1)
    
    assert os.path.isfile(test_path)
    
    new_root = os.path.join(str(tmpdir), "test")
#    os.makedirs(new_root)
    move_path = os.path.join(str(tmpdir), "test", "pool.pkl")
    shutil.copytree(str(tmpdir), new_root)
    
    loaded_pool = pickle.load(open(move_path, "rb"))
                              
    data_store.deserialise_pool(catalog, loaded_pool, root_dir=new_root)
    new_data = loaded_pool.get(data_index)

    assert isinstance(new_data, Data)
    assert new_data._data == "Tidal"

