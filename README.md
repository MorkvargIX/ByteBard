Install all requirements packages.
```bash
pip install requirements
```
Run this command to create *martor* static directory
```bash
./manage.py collectstatic
```
The app is using a PostgreSQL database. If you want to utilize the database and SMTP, please create a **.config** file 
and update the path reference in the settings.
```python
conf.read('/ByteBard/.config')
```
Please create the config file following the INI standard. Don't forget register on [Imgur Oauth2](https://api.imgur.com/oauth2)
```text
[server]
SECRET_KEY = your_key

[database]
NAME = db_name
USER = db_user
PASSWORD = db_password

[email]
...
```
Do migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
Also, you should delete next var. This variable displays a message to the console, without sending it to the server.
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```
---
To use django-social-share edit templates in your **.venv** file. For example my path is: 
/ByteBard/.venv/lib/python3.12/site-packages/django_social_share/templates/django_social_share/templatetags/
post_to_twitter.html. 
