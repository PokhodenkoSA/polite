# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

### Added

- Added Directory.list_files method to list the files in a directory if it
  exists
- Added DirectoryMap.copy_all and DirectoryMap.safe_copy_all to copy all files
  in the source directory to the target directory.
- Directory objects now returns their path when printed.
  
### Changed

- Made Logger.configure_logger require the configuration dictionary as an
  input.
  
### Fixed

- Ensured that the target directory exists when calling ReadYAML.write().

## [0.9.0] - 2017-01-04

### Added

- Initial import of dtocean-gui from SETIS.

