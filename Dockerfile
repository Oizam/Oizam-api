FROM python:3.8.13

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

COPY ./main.py /code/main.py

RUN pip install -r /code/requirements.txt

COPY ./ /code/

ENTRYPOINT [ "python" ]

CMD [ "main.py" ]