# miscanchas
### Para instalar repositorio:###


En un entorno linux, desde la terminal:

    sudo apt-get install python
    sudo apt-get install git
    sudo apt-get install virtualenv
    sudo apt-get install pip
    pip install python-dateutil
    virtualenv miscanchasenv (crear entorno virtual)
    source miscanchasenv/bin/activate (activar entorno virtual)
    git clone https://github.com/ignacioribes/miscanchas.git

    Instalar y configurar PostgreSQL: ver en https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04 con los settings definidos en miscanchas/miscanchas/settings.py
    cd miscanchas
    pip install -r requirements.txt
    python manage.py migrate (crea la base de datos)
    python manage.py createsuperuser (crea superusuario para la db, para entrar por /admin)
    python manage.py runserver
    
Crear DB en Postgres

    psql
    CREATE DATABASE miscanchas;
    CREATE USER admin_miscanchas WITH PASSWORD 'miscanchas_0517';
    GRANT ALL PRIVILEGES ON DATABASE miscanchas TO admin_miscanchas;

Fix error Pillow en Mac OS (local install):

    ARCHFLAGS=-Wno-error=unused-command-line-argument-hard-error-in-future pip install pillow

Actualizacion de DB:

    python manage.py makemigrations (crea migracion)
    python manage.py migrate

Actualizar Statics:

    python manage.py collectstatic (buildea de statics-temp a statics)

Local/production URLs on: 
    
    reserva⎽calendar.html (line 49)
    models.py (line 269)

MP test:
    
    https://www.mercadopago.com.ar/developers/es/guides/payments/web-payment-checkout/test-integration/

Comisión, se define en models.py en la linea 18, ejemplo:

    COMISION = 0.06

Comsion, en el frontend se define en base.html en la linea 39, ejemplo:

    var comision = 0.06;