# Environment
    Ubuntu 18.04.3 LTS, python 3.6.8, Django
    Make virtualenv : python3 -m venv spvenv
    Run Virtualenv : . activeVenv.sh (source spvenv/bin/activate)
    insall Package : pip install -r requirements.txt
    make config.cfg and edit
    APP DB:
        - python manage.py makemigrations stocks
    DB Commit: python manage.py migrate
    APP DB Init: python manage.py loaddata stocks_db_init.json 
    
    
# Django
    초기시작 : django-admin startproject stockpy
    DB : Maria DB
    python manage.py startapp stocks
    python manage.py migrate # 기본 DB Migrate 
    python manage.py createsuperuser 슈퍼유져 

# Maria DB
    mysql -u root
    use mysql
    
    user add
        create user 'user1'@'localhost or %' identified by 'password'
    grant
        grant all privileges on *.* to 'user1'@'localhost or %' with grant option;
    
    flush privileges;
    
    connect 
        mysql -u user1 -ppassword
      
    create database stock_py  #create database
    
# Integration MariaDB
    - pip install mysqlclient, configparser
    - Edit config.cfg (settings.py/DATABASE)
    