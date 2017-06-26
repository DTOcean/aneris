# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

### Added

- Add gitignore.
- Add change log.
- Add Database.execute_transaction method which will commit a query immediately
  without returning results.
- Add Sequencer.refresh_interfaces and Hub.refresh_interface to replace
  interfaces in Hubs. Useful if interfaces have gone stale after saving.
  
### Changed

- Changed labelling of inputs in an interface in a pipeline that appear in a
  previous interface to say "overwritten" rather than "unavailable".
- In DataStorage._convert_box_to_data catch TypeErrors and pass with a warning
  when unpickling, if the warn_unpickle flag is True.
- In DataStorage._make_data allow data not in the data catelogue to pass with a
  warning if the warn_missing flag is True.
  
### Fixed
  
- Removed unnecessary psycopg2 import
- Fixed bug in FileInterface.check_path

## [0.9.1] - 2017-01-04

### Added

- Initial import of aneris from SETIS.
