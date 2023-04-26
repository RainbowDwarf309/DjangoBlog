Python 3.10.0 +

### Создание и настройка пользователя\базы 
    sudo -u postgres psql

    psql postgres or sudo -i -u postgres
    
    CREATE DATABASE blog;
    create user user_name_blog with password 'password';
    alter role user_name_blog set client_encoding to 'utf8';
    alter role user_name_blog set default_transaction_isolation to 'read committed';
    alter role user_name_blog set timezone to 'UTC';
    ALTER USER user_name_blog CREATEDB;

    pip3 install -r blog/requirements/config
    Где config необходимый конфиг.