# Environment
    Ubuntu 18.04.3 LTS, python 3.6.8, Django
    Make virtualenv : python3 -m virtualenv spvenv
    Run Virtualenv : . activeVenv.sh
    insall Package : pip install -r requirements.txt
    
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
    