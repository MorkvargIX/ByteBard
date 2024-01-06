Install all requirements packages.
```bash
pip install requirements
```

For using form you must configure smtp server. Provide appropriate data in vars:
```python
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'some_mail@gmail.com'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

Update var in blog/views/post_share.
```python
def post_share(request, post_id):
    # Code
    send_mail(subject, message, 'some_mail@gmail.com', [cd['to']])
    # Code
```

Also, you should delete next var. This variable displays a message to the console, without sending it to the server.
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```