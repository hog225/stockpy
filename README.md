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
    DB BackUp : mysql [dbname] -u [username] -p[password] -N -e 'show tables like "bak\_%"' | xargs mysqldump [dbname] -u [username] -p[password] > [dump_file] 
    DB Restore : mysql -u [사용자 계정] -p [패스워드] [복원할 DB] < [백업된 DB].sql
    
# Integration MariaDB
    - pip install mysqlclient, configparser
    - Edit config.cfg (settings.py/DATABASE)
    
# Jquery/bootstrap 
    - getStatic.sh 실행시켜 설치 
    - crispy forms install requirments.txt에 포함 -> setting.py 변경
    - Jquery WEB site에서 Jquery 다운 
    - https://getbootstrap.com 에서 Compiled CSS and JS 다운 
    - stocks/static 에다 css, js 파일 이동