# Backend Inventario Mantenimiento

Instalar Python 3.11.2

python -m venv venv

./venv/Scripts/activate

python -m pip install -r requirements.txt

esta para mysql o postgress, en el archivo Settings.py revisar la conexión a base de datos deseada y nombrar en el gestor de base de datos la base de datos igual que el django.

python manage.py migrate

python manage.py runserver
