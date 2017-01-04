#!/usr/bin/env python

"""Utility module with functions to provide paths to application files.

.. module:: paths
   :platform: Windows
   :synopsis: Provides application paths

.. moduleauthor:: Mathew Topper <mathew.topper@tecnalia.com>

"""

# Built-in modules
import os
import sys
import shutil
import inspect

# Local imports
from .appdirs import user_data_dir, site_data_dir

class Directory(object):

    '''Work with a stored directory location'''

    def __init__(self, dir_path):

        self._dir_path = dir_path

        return

    def get_path(self, file_name=None):

        result = self._dir_path
        
        if file_name is not None:
            
            result = os.path.join(result, file_name)

        return result
        
    def isdir(self):
        
        return os.path.isdir(self._dir_path)
        
    def isfile(self, file_name):
        
        test_path = self.get_path(file_name)
            
        return os.path.isfile(test_path)
        
    def makedir(self):

        '''Make a directory if it does not already exist.
        '''

        if not self.isdir():
            os.makedirs(self.get_path())

        return

    
class ObjDirectory(Directory):

    '''Directory of the calling object.'''

    def __init__(self, module_name,
                       *paths):

        mod_handle = sys.modules[module_name]
        dir_path = module_dir(mod_handle)
        
        dir_path = os.path.join(dir_path, *paths)
        
        super(ObjDirectory, self).__init__(dir_path)
        
        return


class UserDataDirectory(Directory):

    '''Directory based on the user data directory for the given package.'''

    def __init__(self, package,
                       company,
                       *paths):

        dir_path = user_data_dir(package, company, roaming=True)
        dir_path = os.path.join(dir_path, *paths)
            
        super(UserDataDirectory, self).__init__(dir_path)

        return
        
        
class SiteDataDirectory(Directory):

    '''Directory based on the site data directory for the given package.'''

    def __init__(self, package,
                       company,
                       *paths):

        dir_path = site_data_dir(package, company)
        dir_path = os.path.join(dir_path, *paths)
            
        super(SiteDataDirectory, self).__init__(dir_path)

        return

        
class DirectoryMap(object):

    '''Class for moving files from one directory to another.

    Attributes:
        target_dir (polite.paths.Directory)
        source_dir (polite.paths.Directory)
        last_copy_path (str): Location of last copied configuration file.
          Defaults to None.

    '''

    def __init__(self, target_dir,
                       source_dir):

        self.target_dir = target_dir
        self.source_dir = source_dir
        self.last_copy_path = None

        return

    def target_exists(self, file_name=None):

        '''Test to see if a given target file or directory exists

        Args:
            file_name (str, optional): The name of a target file to
              check.

        Returns:
            bool: True if path exists.

        '''
        
        if file_name is not None:
            
            result = self.target_dir.isfile(file_name)
            
        else:
            
            result = self.target_dir.isdir()

        return result

    def copy_file(self, src_name,
                        dst_name=None,
                        overwrite=False,
                        new_ext='.new'):

        '''Copy a file from the source to target directory.

        Args:
            cfile_name (str): File name of the file to copy. It is
              assumed that this exists within the source directory.
            overwrite (bool, optional): Copy the files to target
              directory even if it already exists. Default to False.
            new_dir (str, optional): If target file exists and overwrite
              is False copy the file appending this extension. Defaults to
              ".new".

        '''
        
        if self.source_dir is None:
            
            errStr = "No source directory is given."
            raise ValueError(errStr)
            
        if dst_name is None:
            file_name = src_name
        else:
            file_name = dst_name

        # Build the destination path
        dst_file_path = self.target_dir.get_path(file_name)

        if self.target_exists(file_name) and not overwrite:
                       
            dst_file_path = dst_file_path + new_ext

        # Get the source path
        src_file_path = self.source_dir.get_path(src_name)

        # Prepare the destination directory
        self.target_dir.makedir()

        # Copy the file
        shutil.copy(src_file_path, dst_file_path)

        # Punch out the dst_file_path to logging
#        sys.stdout.write(dst_file_path)

        # Store the location of the copy directory
        self.last_copy_path = dst_file_path

        return

    def safe_copy_file(self, src_name, dst_name=None):

        '''Copy the file to the target directory if it does not
        exist already.

        Args:
            file_name (str): File name of the file to copy. It is
              assumed that this exists within the source directory.

        '''
        
        if dst_name is None:
            file_name = src_name
        else:
            file_name = dst_name

        # Test for existance otherwise copy the file to the user data
        # directory
        if not self.target_exists(file_name):

            self.copy_file(src_name, dst_name)

        return


def object_path(obj):

    '''Return the path of the class object.

    Args:
      object (obj): Class object.

    Returns:
        str: Absolute path to class source file.
    '''

    path = inspect.getabsfile(obj.__class__)

    return path

def object_dir(obj):

    '''Return the directory path containing the class object.

    Args:
      object (obj): Class object.

    Returns:
        str: Absolute path to directory containing class source file.
    '''

    obj_path = object_path(obj)
    obj_dir = os.path.dirname(obj_path)

    return obj_dir

def class_path(cls):

    '''Return the path of the class attribute.

    Args:
      class (cls): Class.

    Returns:
        str: Absolute path to class source file.
    '''

    path = inspect.getabsfile(cls)

    return path

def class_dir(cls):

    '''Return the directory path containing the class attribute.

    Args:
      class (cls): Class.

    Returns:
        str: Absolute path to directory containing class source file.
    '''

    cls_path = class_path(cls)
    cls_dir = os.path.dirname(cls_path)

    return cls_dir

def module_path(module):

    '''Return the path of the modules "__file__" attribute.

    Args:
      module (module): Module object.

    Returns:
        str: Absolute path to "module.__file__".

    '''

    module_path = os.path.realpath(module.__file__)

    return module_path

def module_dir(module):

    '''Returns path to the directory containing the given module.

    Args:
      module (module): Module object.

    Returns:
        str: Absolute path to directory containing module.

    '''

    mod_path = module_path(module)
    dirname = os.path.dirname(mod_path)

    return os.path.abspath(dirname)


