FROM python:3.9

RUN apt update && apt upgrade -y && pip3 install pipenv

COPY . .

RUN pip3 install poetry

RUN poetry install --no-dev

RUN chmod +x fastapirun.sh

CMD /bin/sh fastapirun.sh

EXPOSE 8000