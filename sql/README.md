# Assessment01

#### To install postgres via homebrew, run the following commands.
1. brew update
2. brew install postgres

#### To start or Stop Postgres:
- pg_ctl -D /usr/local/var/postgres start
- pg_ctl -D /usr/local/var/postgres stop

#### First steps:
1. `python generator.py`(creates the data that postgres db'll consume)
2. `createdb <mydatabasename>`
3. `psql -d <mydatabasename> -a -f init.sql` (creates db tables consuming data created by generator file)

Now you can go to `queries` folder and just run `psql -d <mydatabasename> -a -f <task-file>.sql` in order to query the db. 
  
#### More info:
- postgres (PostgreSQL) 13.0
- python 2.7.15
