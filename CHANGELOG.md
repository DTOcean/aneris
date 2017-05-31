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
  
### Changed

- Changed labelling of inputs in an interface in a pipeline that appear in a
  previous interface to say "overwritten" rather than "unavailable".
  
### Fixed
  
- Removed unnecessary psycopg2 import
- Fixed bug in FileInterface.check_path

## [0.9.1] - 2017-01-04

### Added

- Initial import of aneris from SETIS.
