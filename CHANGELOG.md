# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [0.10.0] - 2019-03-04

### Added

- Add gitignore.
- Add change log.
- Add Database.execute_transaction method which will commit a query immediately
  without returning results.
- Add Sequencer.refresh_interfaces and Hub.refresh_interface to replace
  interfaces in Hubs. Useful if interfaces have gone stale after saving.
- Add create_pool_subset method to DataStorage class. Given a pool and 
  datastate, this creates a new pool and datastate containing just the variables
  in the datastate.
- Added create_merged_state method to the Loader class. By default, this
  generates a merged pseudo state from a given simulation unless the simulation
  already has one stored.
- Added compatibility for loading pandas data from version prior to 0.20 when
  using version 0.20 or greater.
- Interfaces which do not import properly can now be allowed to skip if
  the warn_import flag is set in Socket.discover_interfaces or Sequencer.
- Added conda requirements file for developers that doesn't include any DTOcean
  packages (requirements-conda-dev.txt).
- Added test module, which contains SPT interface example, which as been added
  to the README.
  
### Changed

- For pipelines, changed labelling of inputs for one interface that appear in a
  previous interface to say "overwritten" rather than "unavailable".
- In DataStorage._convert_box_to_data will catch errors and pass with a warning
  when unpickling, if the warn_unpickle flag is True.
- In DataStorage._convert_data_to_box will catch errors and pass with a warning
  when saving, if the warn_save flag is True.
- In DataStorage._make_data allow data not in the data catalogue to pass with a
  warning if the warn_missing flag is True.
- Modify add_datastate in the Controller class so that it can take Data objects
  as the variable values, if the use_objects flag is set to True.
- Updated API for pandas.read_excel
- Moved the add_datastate method from the Controller to the Loader class.
  
### Fixed
  
- Removed unnecessary psycopg2 import
- Fixed bug in FileInterface.check_path
- Ensure SerialBox is replaced if encountering unknown data identifier when
  deserializing a data pool.
- Fixed bug for Hub.get_next_scheduled when no interfaces are scheduled. Now
  returns None in this case.

## [0.9.1] - 2017-01-04

### Added

- Initial import of aneris from SETIS.
