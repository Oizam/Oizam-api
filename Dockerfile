FROM python:3.8.13

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

COPY ./main.py /code/main.py

RUN pip install -r /code/requirements.txt

COPY ./App /code/App

ENTRYPOINT [ "python" ]

CMD [ "main.py" ]