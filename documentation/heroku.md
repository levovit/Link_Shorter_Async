# Deploy to Heroku
First you need to download git and clone repository
## Download git
#### On Windows
https://git-scm.com/download/win
#### On Ubuntu
```bash
$ sudo apt install git
```
If you have problem with that command use link

https://git-scm.com/download/linux
#### On CentOS
```bash
$ yum install git
```

## Git
Clone Repository
```bash
$ git clone https://github.com/levovit/Link_Shorter_Async.git
$ cd Link_Shorter_Async
```
Create new Repository

https://github.com/new

Add new origin and push into you repository
```bash
$ git remote add origin git@github.com:username/new_repo
$ git push -u origin master
```

## Heroku
Create new app with Heroku 
https://dashboard.heroku.com/new-app

Go to the deploy page.
choose Deployment method `GitHub`
Turn Automatic deploys.
And deploy branch `master`


Now you can see your app on
`https://<Your-app-name>.herokuapp.com/`