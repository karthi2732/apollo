# apollo
apollo repo contains utility scripts and application for assisting and supporting stanlysis

uses virtual-env setup for installing and maintaining its dependencies

## Usage
 - Create table with the following query in local mysql database.

```
CREATE TABLE `gst_details` (
  `search_id` varchar(255) NOT NULL,
  `exchange` varchar(255) NOT NULL,
  `code` varchar(255) NOT NULL,
  `tradable` tinyint(1) DEFAULT '0',
  `g_contract_id` varchar(255) DEFAULT NULL,
  `isin` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`search_id`),
  UNIQUE KEY `unique_code_idx` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

  - Use the following commands to setup env for the scripts

  ```
  # If Virtual Env is not installed

  pip install virtualenv;
  ```
  ```
  # Creating Virtual Env for Script
  # This can be excluded from VCS

  python3 -m venv .venv;
  ```
  ```
  # Activating Virtual Env

  source ./.venv/bin/activate;
  ```
  ```
  # Deactivating Virtual Env

  deactivate;
  ```
  - Other util Commands on `venv`

  ```
  # Get Latest Dependencies and its version in Virtual Env

  pip3 freeze > requirements.txt;
  ```

  ```
  # Install Packages in Virtual Env

  pip3 install -r requirements.txt;
  ```
  - Project Usage Commands
  ```
  # To run archer script that keeps probing server and notifies upon crossing thresholds

  python3 archer.py
  ```


