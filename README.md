# Senior Project

![](app/static/favicon.png/)

# Table of Contents
- [About](#about)
- [Requirements](#requirements)
- [Downloading repo](#downloading-repo)
- [Setup](#setup)
  * [Python Packages](#python-packages)
  * [.env](#env)
  * [Database](#database)
    + [MySQL](#mysql)
- [Local run](#local-run)
- [Deploy with Apache](#deploy-with-apache)
- [Overview](#overview-)
- [Scripts](#scripts)
- [Developers List](#developers-list)

# About
This inventory management system will modernize the way ACR Solar keeps track of the parts within their inventory and keep members of the company aware of potentially problematically low stock. This software will allow ACR employees to track items, change stock to reflect the parts used for a job, and know when to order additional parts due to low stock.


# Requirements
- Python
  - Used version 3.10 and .bat scripts in `/scripts/` folder mostly are `python manage.py XXX` where python is `py -3.10` for Windows and `python3.10` for Mac/Linux like systems.
    - for mac/linux system running the script can work with `./` in front (ex: `./XXXX.bat`)
    - might need to give it execute permission with `chmod +x *.bat` which gives all .bat files execute mode
    - can get Python 3.10 here: https://www.python.org/downloads/release/python-3100/
      - make sure to select to add to PATH
      - can change installation path by using custom installation and changing Customize install location to `C:\Python310` and select `Precompile standard library`
      - disable pathj length limit if prompted
  - other versions of python may work but would need to change scripts (mostly base.bat in scripts folder).
  - test to see what you installed python correctly though `py -3.10 --version` on windows and `python3.10 --version` on Mac/Linux like systems.
- Apache 2.4
  - Apache with mod_wsgi was used for deploying on Windows and gunicorn was used for heroku's linux server
  - can get Apache 2.4 lounge here: https://www.apachelounge.com/download/
  - download, extract files, copy `Apache24` folder and move it into C drive
- Visual C++ Redistributable Visual Studio 2015-2022. vc_redistx64 and x86 are listed here: https://www.apachelounge.com/download/
  - make sure to select `C++ build tools` when prompting workloads to install
- VS Code (optional as can use different source-code editor but this downloading repo is made easy with VS Code)
- Preferably some database tool like MySQL Workbench
 
# Downloading repo
Go to https://gitlab.com/JohnGeronimo1/senior-project
1. Click on Clone dropdown button
2. Choose the cloning option that best suits your environement ( For the following steps we advice the option VS Code (HTTPS) )
3. This will open up VS Code automaically
4. In VS Code, Click Open when the prompt "Allow an Extension to open this URL?" pops up
5. Go to the place where you would want the repository saved then click on Select Repository Location
6. In VS Code, click Open when the prompt on the lower right hand side prompt "Would you like to open the cloned repository, or add it to the current workspace?" opens up
7. Now your downloaded repository will show up in VS Code ready to use. 
8. Continue to the setup part of this readme

# Setup
## Python Packages
- run `requirements.bat` in /scripts/ folder to install all the python packages
- Notes
  - If error on mod_wsgi, make sure you have Apache. Can also reference their [git](https://github.com/GrahamDumpleton/mod_wsgi/#readme) or [PyPi](https://pypi.org/project/mod-wsgi/)
  - If error on mysqlclient: try to run `brew install mysql`
  - If error on pg_config, try running `brew install postgresql`
  - If I missed dependency, install it with `[py -3.10 or python3.10] -m pip install PACKAGE` & put it in requirements.txt

## .env
- copy and paste .envexample file in the same place and rename it to .env if you haven't done so
  - choose a secret key and replace the value for SECRET_KEY in "XXX"
  - list all hosts for the DEPLOY_ALLOWED_HOST variable in string
    - "*" means all and is not recommended
  - fill out database section
    - DEV_DB_XX is for development and PRO_DB_XX is for production
    - NAME is name of Database
    - USER is username of Database user
    - PASS is password of Database user
    - HOST is the ip/url of the Database
    - PORT is port of the Database
- If you want to use GitLab pipeline make sure to go to project settings -> Variables and create a variable for each variable in .env along with it's value. 
  - Note: don't include the "" when typing value.
  - Example: key:SECRET_KEY and VALUE:12345

## Database
Some form of database is required. Currently configured towards MySQL engine.
If you want to change database to something besides MySQL (ex: Postgress):
1. add relevant packages to requirements.txt
2. update 'ENGINE' in DATABASE variable in both `production_settings.py` and `development_settings.py` (located in appsetup/settings/)
3. run `requirements.bat`
For more info: read https://docs.djangoproject.com/en/4.0/ref/settings/#databases

Once your database is setup, make sure you have a new schema/name for database and your .env is setup.
Now prepare your database by running migrate.bat in /scripts/ twice
- Run `migrate.bat` for the first time and it will create all tables in your database
- Run `migrate.bat` once again to prefill some initial data.

Create a superuser which is like a tip-top admin that has all permissions so you have an initial account.
- run `createsuperuser.bat` in scripts

### MySQL
Can create and run your own mysql server or connect to one.

One way to create your own server, is to download MySQL Workbench
- open workbench.
- Add connection. Can create on own ip.
- Open connection if not already open.
- Go to schemas tab.
- Create new Schema, name it whatever.
- Click apply, apply
  - may need to increase screen size to see option

optional to create another account to use for django.
- go to Administration tab -> Users and Priviliegs -> Add Account
- Can change login information for that user "Login" tab
- Can change query and connection limit in "Accounts limit"
- Then click Apply

Update the settings files to your MySQL Info.


# Local run
run `runserver.bat` in scripts folder
- creates local website at your ipv4 and port (currently using 8000)
  - http://your_local_ip:port
- creates public website at your public ip and port
  - http://your_public_ip:port
- can currently login with username = Admin, password = Admin
- can also view admin page at http://your_public_ip:port/admin with superuser
- NOTE:
  - might need to allow portwarding for others to access at your ip


# Deploy with Apache
- open terminal and navigate to your C drive then into cd into `Apache24` that you moved into C drive
- run `bin\httpd.exe -k install`
- commands:
  - start service with `httpd.exe -k start`
  - stop service with `httpd.exe -k stop`
  - restart servicec with `httpd.exe -k restart`
- install Microsoft C++ Build Tools
- install mod_wsgi after install Apache (`py -3.10 -m pip install mod_wsgi==4.9.1`)
- edit `httpd.conf.template`
  - update IP and PORT for `ServerName` (the \<IP\>:PORT part)
  - run `mod_wsgi-express module-config` and replace variables with what was generaded in `httpd.conf.template` (should be LoadFile, LoadModule, and WSGIPythonHome)
  - further edit `httpd.conf.template` to make sure it has correct paths
- copy content of `httpd.conf.template` and paste at the bottom of the file `httpd.conf` in `C:\Apache24\conf`
- run `collectstatic.bat`
- now read to start service
- Note:
  - may need to allow port forwarding
  - may need to change firewall to allow others to access
    - For windows:
      - navigate to Windows Defender Firewall -> Advanced settings
      - click inbound rule -> new rule
      - select Port -> next -> select Specific local port -> change to your PORT (ex: 80) -> next -> select Allow the connection -> next -> select which ones you want (Domain, Private, and/or Public) -> Next -> give it a name and description -> Finish
    - if no static files are being served use the Cling version (`application = Cling(get_wsgi_application())`) in `appsetup/wsgi.py`


# Overview
- urls.py 
  - contains a list of url patterns whete it ties a url (ex : /about/ ) with a view of a page (method from views.py)
  - can have dynamic / variables in url with patterns captured in <> (ex: \<int:pk\>)
- views.py
  - holds methods that build a page
  - uses context data (a dictonary) to pass variables into template / frontend
- models.py creates data tables and can then update/sync database
  - python manage.py makemigrations creates a migration which is what changed
  - python manage.py migrate implements those migrtions created
  - if error of table already exists, then 
    - comment out new tables
    - run `makemigrations.bat`
    - run `fakemigrate.bat`
    - uncomment and new tables and it should be fixed so rerun with make & migrate
- templates
  - this is more of front end
  - `collectstatic.bat` in scripts folder looks for static files and puts them in one folder
  - `app/templates/app` is where the html pages go for app
  - use `layout.html` as a base that other html files can extend (use the same style)
    - HTML pages in this case pages with:
      - {% extends "app/layout.html" %}
      - {% block content %}
    - pages end with "{% endblock %}"
  - can reference static files in HTML like so : "{% static 'app/content/style2.css' %}"
  - `app/templates/app/errors` is where custom errors pages go
- `Procfile` is there to make it compaitable to heroku's linux server
- `manage.py` is the main python file that will be started with various inputs

Notes:
- in case url for "Starting development server at http://XXX" causes errors, try using url in "public access at http://xxx" one or vice versa
- make sure debug is false in settings when deploying (production_settings.py has it off)
- when running locally you can change a .py file and saving can make it restart run
- if no static files are being served use the Cling version (`application = Cling(get_wsgi_application())`) in `appsetup/wsgi.py`

# Scripts
Some useful scripts in /scripts/
- `base.bat` is to find python version. Other scripts use this
- `collectstatic.bat` collects all static files and puts into one place
- `createsuperuser.bat` creates a superuser "admin" that has all permissions
- `fakemigrate.bat` is like a migrate but doesn't do anything. Used to trick database into thinking a migrate happened. (useful for errors like table already exists so instead of creating a new table with migrate.bat you trick it into thinking it created a table)
- `loaddata.bat` is if you have some data you want to load into database you can specifcy a fixture file (read more here: https://docs.djangoproject.com/en/4.0/howto/initial-data/)
- `loadinit.bat` is like loaddata.bat but uses initdata.json
- `makemigrations.bat` creates a file for what changed in database
- `migrate.bat` implments those changes from makemigrations.bat to database
- `requirements.bat` installs python packages
- `runserver.bat` runs a local server
- `showmigrations.bat` shows all migrations (ones your database implemented and ones you created with makemigrations.bat)
- `test.bat` runs all tests


# Developers List
- James Olesen
- John Geronimo
- Leena Sharma
- Kyle Hazell
- Emmanual Lemeshov
- Juan E Portillo
- Reshma Palakkadan
- Thomas Rich

