# Start on Windows
## Download python
Check if you have a python. Type `python` in the command line. There should be such a output
```commandline
>python
Python 3.8.0 (tags/v3.8.0:fa919fd, Oct 14 2019, 19:21:23) [MSC v.1916 32 bit (Intel)] on win32
Type "help", "copyright", "credits" or "license" for more information.
```
If you have a some Error download python for windows 
https://www.python.org/downloads/windows/
## Download Link Shorter
By the same rule as above download git bash
https://git-scm.com/download/win

Clone repository
```commandline
>git clone https://github.com/levovit/Link_Shorter_Async.git
>cd Link_Shorter_Async
```
Create and activate a virtual environment
```commandline
>python -m venv venv
>venv\Scripts\activate
```
Install the required modules
```commandline
$ pip install -r requirements.txt
```

## Database
Download PostgreSQL
https://www.postgresql.org/download/windows/

run shell
```commandline
>cd C:\Program Files\PostgreSQL\<Your version>\bin
>psql
```
Create database 
```commandline
postgres=# CREATE DATABASE link_shorter_db;
```
Create table links
```commandline
>cd <Link Shorter repository path>
>psql -d link_shorter_local -f init.sql -U postgres
```
## Run
`-c` -local config file

`--host` - Host to listen

`--port` - Port to accept connection

`--db` - Path to database

`--debug` - Autoreload code on change

```commandline
>python entry.py -c local.yaml --db "postgresql://user:passwords@localhost:5432/link_shorter_db"
```
