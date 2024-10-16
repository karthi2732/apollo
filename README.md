# apollo
apollo repo contains utility scripts and application for assisting and supporting stanlysis

uses virtual-env setup for installing and maintaining its dependencies

## Usage
 - Create table with the following query in local mysql database.

```
CREATE TABLE `gstk` (
  `search_id` varchar(255) NOT NULL,
  `exchange` varchar(255) NOT NULL,
  `code` varchar(255) NOT NULL,
  `tradable` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`search_id`),
  UNIQUE KEY `unique_code_idx` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

```
CREATE TABLE `gstk_day_stat` (
  `search_id` VARCHAR(255) NOT NULL,
  `open_price` DECIMAL(11,2) DEFAULT 0,
  `live_price` DECIMAL(11,2) DEFAULT 0,
  `day_change` DECIMAL(11,3) DEFAULT 0,
  `day_change_perc` DECIMAL(11,2) DEFAULT 0,
  PRIMARY KEY (`search_id`),
) ENGINE=INNODB DEFAULT CHARSET=utf8;
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


