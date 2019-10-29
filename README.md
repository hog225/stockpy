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
    
    
# Bitnami Wordpress 연동
## Python 3.6 install on Ubuntu 16.04
    # environment: Amazone light sail/ ubuntu 16.04 LTS/ bitnami amp 
    sudo add-apt-repository ppa:jonathonf/python-3.6
    sudo apt-get update
    sudo apt-get install python3.6
    sudo apt-get install python3.6-venv

## DB Setting
    + 워드프레스 MYSQL 은 워드프레스 폴더에 있음
    + apt-get install mysql-client
    + 접속 : mysql --socket=[파일 패스]/wordpress-5.2.4-0/mysql/tmp/mysql.sock
    + mysql root password : mysqladmin -p -u root password [비밀번호] --socket=/home/yghong/wordpress-5.2.4-0/mysql/tmp/mysql.sock
    + PATH 설정 : export PATH=$PATH:/home/[PATH]/wordpress-5.2.4-0/mysql/bin/ - ~/.profile에 저장
    + sudo apt-get install python3.6-dev <= 이거 설치 해야 python mysqlclient 설치됨 
    
## Apache Setting
    Version: Apache/2.4.37 (Unix)
    sudo apt-get install libapache2-mod-wsgi-py3
    sudo vim /etc/apache2/ports.conf -> Listen 8000 추가
    sudo vim /etc/apache2/sites-enabled/000-default.conf -> 아래처럼 입력
    <VirtualHost *:8000>

        ServerAdmin master@localhost
        DocumentRoot /var/www/html
        # Collectstatic 해야함 media도 필요하면 추가
        Alias /static/ /home/yghong/stockpy/stockpy/stockpy/static/  

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        <Directory /home/yghong/stockpy/stockpy/stockpy/static>
                Require all granted
        </Directory>

        <Directory /home/yghong/stockpy/stockpy/stockpy/stockpy/> # wsgi.py 가 있어야함
                <Files wsgi.py>
                        Require all granted
                </Files>
        </Directory>
        # python-path: manage.py 가 있어야함, python-home: spvenv(가상환경 폴더 지정)
        WSGIDaemonProcess stockpy python-path=/home/yghong/stockpy/stockpy/stockpy python-home=/home/yghong/stockpy/stockpy/spvenv
        WSGIProcessGroup stockpy
        WSGIScriptAlias / /home/yghong/stockpy/stockpy/stockpy/stockpy/wsgi.py

    </VirtualHost>
    python manage.py collectstatic (코드상에 {% static "path"%} 이렇게 안할시 에러 발생위험)
    sudo service apache2 restart -> Django 서버가 실행됨 

