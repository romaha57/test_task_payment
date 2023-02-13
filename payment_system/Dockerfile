FROM python

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

RUN pip install --upgrade pip

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/

EXPOSE 8000

CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "loaddata", "user.json"]
CMD ["python", "manage.py", "loaddata", "item.json"]
CMD ["python", "manage.py", "loaddata", "order.json"]
CMD ["python", "manage.py", "loaddata", "tax.json"]
CMD ["python", "manage.py", "loaddata", "discount.json"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
