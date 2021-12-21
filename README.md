# Как запустить проект :
- Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/MotorShoW/api_final_yatube
cd api_final_yatube
```
- Cоздать и активировать виртуальное окружение:
```
python -m venv env
source venv/Scripts/Activate (для Windows)
```
- Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
- Выполнить миграции:
```
python manage.py migrate
```
- Запустить проект:
```
python manage.py runserver
```
