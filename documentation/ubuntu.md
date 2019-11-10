# Start on Ubuntu
## Download python
Check if you have a python. Type `python` in the command line. There should be such a output
```bash
$ python
Python 3.7.4 (default, Sep 12 2019, 01:19:52)
[GCC 7.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```
If you have a some Error download python for Linux 
```bash
$ sudo apt-get update
$ sudo apt install python3.7
```
If you have problem with that command use link

https://www.python.org/downloads/source/

## Download Link Shorter
By the same rule as above download git bash
```bash
$ sudo apt install git
```
If you have problem with that command use link

https://git-scm.com/download/linux

Clone repository
```bash
$ git clone https://github.com/levovit/Link_Shorter_Async.git
$ cd Link_Shorter_Async
```
Create and activate a virtual environment
```bash
$ virtual venv —python=python3.7
$ source venv\Scripts\activate
```
Install the required modules
```bash
$ pip install -r requirements.txt
```

## Database
Download PostgreSQL
```bash
$ sudo apt-get install wget ca-certificates
$ wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
$ sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
$ sudo apt-get install postgresql postgresql-contrib
```
If you have problem with that command use link

https://www.postgresql.org/download/linux/ubuntu/

run shell
```bash
$ sudo su - postgres
$ psql
```
Create database 
```bash
postgres=# CREATE DATABASE link_shorter_db;
```
Create table links
```bash
$ cd <Link Shorter repository path>
$ psql -d link_shorter_local -f init.sql -U postgres
```
## Run
`-c` -local config file

`--host` - Host to listen

`--port` - Port to accept connection

`--db` - Path to database

`--debug` - Autoreload code on change

```bash
$ python entry.py -c local.yaml --db "postgresql://user:password@localhost:5432/link_shorter_db"
```
