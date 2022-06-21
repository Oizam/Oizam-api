FROM python:3.8.13

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

COPY ./main.py /code/main.py

COPY ./app /code/app

RUN pip install -r /code/requirements.txt

ENTRYPOINT [ "python" ]

CMD [ "main.py" ]