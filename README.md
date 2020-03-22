# dosuke_generator

## このアプリについて
音楽サークルのバンド練習スケジュールを自動で組むアプリケーション

### 要件
- 練習スタジオの使える時間に対して、複数のバンドに平等な練習時間が割り振られるような練習スケジュールを考えたい
- セッションタイム（みんなで演奏する時間）も考慮したい
- 所属歴による優遇やスタジオまでの距離が遠い人は昼間にするなどを考慮したい

## How to Start (for Mac)
### Require
- git
- python3
- pip3

### Install and Build
1. Install this app
```
$ git clone https://github.com/bbladr/dosuke_generator.git dosuke_generator
$ cd dosuke_generator
```
2. Create and activate a python virtual environment
```
$ python3 -m venv dosuke_env
$ source dosuke_env/bin/activate 
```
3. Install packages
```
$ pip3 install -r requirements.txt
$ LDFLAGS=-L/usr/local/opt/openssl/lib pip install mysqlclient # https://github.com/PyMySQL/mysqlclient-python/issues/131
```
4. Create admin user
```
$ python3 manage.py createsuperuser
> username
> email (allow null)
> password * 2
```
5. Migrate
```
$ sh create_db_and_dosuke_config_table_with_default_records.sh
$ python3 manage.py makemigrations
$ python3 manage.py migrate
```
6. Import default settings and sample data
```
$ python3 manage.py loaddata sample
```
5. Build a server
```
$ python3 manage.py runserver
```

Access to [http://localhost:8000/](http://localhost:8000/)
