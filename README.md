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
- pyenv

### Install and Build
1. Create and activate a python virtual environment
```
$ python3 -m venv dosuke_env
$ source dosuke_env/bin/activate 
```
2. Install this app and packages
```
$ git clone https://github.com/bbladr/dosuke_generator.git dosuke_generator
$ cd dosuke_generator
pip install -r requirements.txt
```
3. Migrate
```
$ python3 manage.py makemigrations
$ python3 manage.py migrate
```
4. Import default settings and sample data
```
$ python3 manage.py loaddata config_seed
$ python3 manage.py loaddata sample
```
5. Build a server
```
$ python3 manage.py runserver
```

Access to [http://localhost:8000/](http://localhost:8000/)
