# -*- coding: utf-8 -*-
"""py.test tests on main.py

.. moduleauthor:: Mathew Topper <mathew.topper@tecnalia.com>
"""

import os
import shutil
import configobj

import pytest

from polite.paths import Directory, ObjDirectory, DirectoryMap
from polite.configuration import Config, Logger, ReadINI, ReadYAML

# Using a py.test fixture to reduce boilerplate and test times.
@pytest.fixture(scope="module")
def directory():
    '''Share a ObjDirectory object'''
    
    objdir = ObjDirectory(__name__, "..", "examples", "config")

    return objdir

def test_user_config_exists(tmpdir, directory):

    '''Test if the user_config_exists function returns false'''

    # Make a local directory
    locd = tmpdir.mkdir("config")

    configdir = Directory(str(locd))

    logger = Logger(configdir)

    assert configdir.isfile(logger.config_file_name) == False

def test_copy_logger_config(tmpdir, directory):
    
    '''Test if logger configuration is copied'''
    
    # Make a local directory
    locd = tmpdir.mkdir("config")

    configdir = Directory(str(locd))
    logger = Logger(configdir)
    
    with pytest.raises(ValueError):

        # Copy the logging file
        logger.copy_config()

def test_configure_logger(tmpdir, directory):

    '''Test if logger configuration can be loaded'''

    # Make a local directory
    locd = tmpdir.mkdir("config")
    locp = locd.join("logging.yaml")

    configdir = Directory(str(locd))

    logger = Logger(configdir)

    # Copy the logging file
    src_file_path = directory.get_path("logging.yaml")
    shutil.copy(src_file_path, str(locp))

    # Attempt to configure the logger
    logger.configure_logger()
    
def test_call_logger(tmpdir, directory):

    '''Test if logger can be called'''

    # Make a local directory
    locd = tmpdir.mkdir("config")
    locp = locd.join("logging.yaml")

    configdir = Directory(str(locd))

    logger = Logger(configdir)
    
    # Copy the logging file
    src_file_path = directory.get_path("logging.yaml")
    shutil.copy(src_file_path, str(locp))
    
    logger('my_logger')

def test_copy_ini_config(tmpdir, directory):

    '''Test if the configuration file is correctly copied.'''

    # Make a local directory
    locd = tmpdir.mkdir("config")

    # Create Logger object and change path to user data dir to tmp
    configdir = Directory(str(locd))

    ini_reader = ReadINI(configdir)
    
    with pytest.raises(ValueError):

        # Copy the logging file
        ini_reader.copy_config()

    
def test_config_exists(tmpdir, directory):

    '''Test that the configuration file is read correctly'''

    # Make a local directory
    locd = tmpdir.mkdir("config")
    locp = locd.join("configuration.ini")

    # Create object
    configdir = Directory(str(locd))
    ini_reader = ReadINI(configdir)

    # Copy config and check for existance
    src_file_path = directory.get_path("configuration.ini")
    shutil.copy(src_file_path, str(locp))

    test = ini_reader.config_exists()

    assert test
    
def test_get_config(tmpdir, directory):

    '''Test that the configuration file is read correctly'''

    # Make a local directory
    locd = tmpdir.mkdir("config")
    locp = locd.join("configuration.ini")

    # Create object
    configdir = Directory(str(locd))
    ini_reader = ReadINI(configdir)

    # Copy the config file
    src_file_path = directory.get_path("configuration.ini")
    shutil.copy(src_file_path, str(locp))

    # Read the config file
    config = ini_reader.get_config()

    assert isinstance(config, configobj.ConfigObj)
    assert set(config.keys()) == set(['Spreadsheet'])
    assert set(config['Spreadsheet'].keys()) == set(['high', 'low'])
    
def test_read_yaml(tmpdir, directory):

    '''Test if the configuration file is correctly copied.'''

    # Make a local directory
    locd = tmpdir.mkdir("config")
    locp = locd.join("logging.yaml")

    # Create Logger object 
    configdir = Directory(str(locd))
    yaml_reader = ReadYAML(configdir, "logging.yaml")

    # Copy the config file
    src_file_path = directory.get_path("logging.yaml")
    shutil.copy(src_file_path, str(locp))
    
    yaml_dict = yaml_reader.read()
    
    assert "loggers" in yaml_dict
    
def test_write_yaml(tmpdir, directory):

    '''Test if the configuration file is correctly copied.'''

    # Make a local directory
    locd = tmpdir.mkdir("config")

    # Create Logger object and change path to user data dir to tmp
    configdir = Directory(str(locd))

    yaml_reader = ReadYAML(configdir, "logging.yaml")
    
    test_list = ["curly", "larry", "moe"]
    yaml_reader.write(test_list)
    
    assert os.path.basename(str(locd.listdir()[0])) == "logging.yaml"


