Install all requirements packages.
```bash
pip install requirements
```
The app is using a PostgreSQL database. If you want to utilize the database and SMTP, please create a **.config** file 
and update the path reference in the settings.
```python
conf.read('/ByteBard/.config')
```
Please create the config file following the INI standard.
```text
[database]
NAME = *name*
USER = *user*
PASSWORD = *password*

[email]
...
```

Also, you should delete next var. This variable displays a message to the console, without sending it to the server.
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```
