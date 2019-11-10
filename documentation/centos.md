# Start on CentOS
## Download python

```bash
$ sudo yum install -y https://centos7.iuscommunity.org/ius-release.rpm
$ sudo yum update
$ sudo yum install -y python37u python37u-libs python37u-devel python37u-pip
```

## Download Link Shorter
```bash
$ yum install git
```
Clone repository
```bash
$ git clone https://github.com/levovit/Link_Shorter_Async.git
$ cd Link_Shorter_Async
```
Create and activate a virtual environment
```bash
$ yum install python-pip.noarch 
$ pip install virtualenv
$ virtualenv --no-site-packages -p python3 program
$ source /web/venv/program/bin/activate
```
Install the required modules
```bash
$ pip install -r requirements.txt
```

## Database
Download PostgreSQL
```bash
$ sudo yum update
$ sudo yum install postgresql-server postgresql-contrib
$ sudo postgresql-setup initdb
$ sudo systemctl start postgresql
$ sudo systemctl enable postgresql
```
If you have problem with that command use link

https://www.postgresql.org/download/linux/redhat/

run shell
```bash
$ sudo passwd postgres
$ sudo su - postgres
$ psql -d template1 -c "ALTER USER postgres WITH PASSWORD '<your-password>';"
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
