# Trabajos de grado #

El proyecto permite gestionar la información referente al proceso completo de trabajos de grado de pregrado, maestría y posgrado de la Escuela de Ingeniería Eléctrica y Electrónica de la Universidad del Valle.

Se definió la arquitectura como multitenant para expandir el software no solo para una escuela, sino para muchas más.

---
## Configuración

1. Se debe configurar el archivo `secrets.json` mediante las variables:
    - SECRET_KEY: String que representa la llave secreta de la aplicación.
    - DEBUG: Booleano (True o False) que representa si la aplicación está en modo desarrollo o no.
    - DATABASE_DEFAULT: Diccionario con la configuración de la base de datos principal de la aplicación, resaltando que el engine debe ser obligatoriamente `django_tenants.postgresql_backend`.
    - DOMINIOS_PROPIOS: Listado de los dominios permitidos para acceder a la aplicación, no es necesario si `DEBUG = True`.

2. Se debe configurar el archivo  `config.json` mediante las variables:
    - ESCUELAS_PARA_CREAR: Lista de listas, donde cada lista interior debe contener tres (3) strings, el primero debe ser el nombre del esquema asociado a la escuela, el segundo el nombre que tendrá la escuela, el tercero las siglas de la escuela (e.g. EISC), y el cuarto es el subdominio asociado a la escuela.

---
## Instrucciones

1. Ejecutar el siguiente comando para instalar todas las dependencias del proyecto (se requiere internet).
    -   `pip install -r requirements/base.pip`
2. Ejecutar los siguientes comandos para actualizar la base de datos con las tablas requeridas.
    -   `python manage.py makemigrations`
    -   `python manage.py migrate_schemas`
    -   `python manage.py crear_escuelas`
    -   `python manage.py tenant_command configurar_permisos --schema=eiee`
3. Ejecutar el siguiente comando para iniciar el servidor (manteniendo la terminal abierta).
    -   `python manage.py runserver`
4. Abrir en el navegador web la siguiente url para acceder a la aplicación.
    -   `eiee.localhost:XXXX`, XXXX: puerto en el que ejecutará la aplicación.
