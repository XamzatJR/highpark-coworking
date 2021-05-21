FROM python:3.9

RUN apt update && apt upgrade -y && pip3 install pipenv

COPY . .

RUN pip3 install -r requirements.txt

RUN chmod +x fastapirun.sh

CMD /bin/sh fastapirun.sh

EXPOSE 8000