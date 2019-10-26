# Environment
    Ubuntu 18.04.3 LTS, python 3.6.8, Django
    Make virtualenv : python3 -m venv spvenv, python3.6 -m venv spvenv
    Run Virtualenv : . activeVenv.sh (source spvenv/bin/activate)
    insall Package : pip install -r requirements.txt
    make config.cfg and edit
    APP DB:
        - python manage.py makemigrations stocks
    DB Commit: python manage.py migrate
    APP DB Init: python manage.py loaddata stocks_db_init.json

    install python3.6 on Ubuntu 16.04 LTS
        sudo add-apt-repository ppa:jonathonf/python-3.6
        sudo apt-get update
        sudo apt-get install python3.6
        sudo apt-get install python3.6-venv

    
    
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

    Wordpress bitnami version
    + apt-get install mysql-client
    + 접속 : mysql --socket=/home/yghong/wordpress-5.2.4-0/mysql/tmp/mysql.sock
    + export PATH=$PATH:[파일이 있는 패스]/mysql/bin
    
# Integration MariaDB
    - pip install mysqlclient, configparser
    - Edit config.cfg (settings.py/DATABASE)
    
# Jquery/bootstrap 
    - getStatic.sh 실행시켜 설치 
    - crispy forms install requirments.txt에 포함 -> setting.py 변경
    - Jquery WEB site에서 Jquery 다운 
    - https://getbootstrap.com 에서 Compiled CSS and JS 다운 
    - stocks/static/ccs: ccs 파일 이동 
    - stocks/static/js: js 파일 이동
## Bootstrap theme 적용
    - 사용한 theme : startbootstrap-bare-gh-pages  
    - stocks/static/stocks: 원하는 theme 다운로드 후 index 만 빼고 모든 파일 이동
    - index.html 을 base.html로 사용  
    - 
 # ta-lib 
    1. wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz / 참고로 git 에서 가져온건 안됨 ..
    2. cd ta-lib/
       ./configure --prefix=/usr
       make
    3. sudo make install
    4. 가상환경 Enable 
    5. pip install TA-Lib     
    
    
