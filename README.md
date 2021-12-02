# Sample Project

## Project Setup
```bash
pip install -r requirements.txt
cp sangeet/settings.py.example sangeet/settings.py
python manage.py makemigrations dashboard audit
python manage.py migrate
```

## Create superuser
```bash
python manage.py createsuperuser
```