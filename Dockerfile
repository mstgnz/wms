FROM python:3

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . .
RUN python -m pip install pip
RUN pip install -r requirements.txt 

EXPOSE 8000
CMD ["gunicorn", "--bind", ":8000", "worksite.wsgi:application", "--reload"] 	