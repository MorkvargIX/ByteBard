FROM python

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

RUN pip install --upgrade pip

RUN pip uninstall channels --yes && pip uninstall daphne --yes && python -m pip install -U channels["daphne"]

COPY . . 

EXPOSE 8000

WORKDIR /app/mysite

