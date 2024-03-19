FROM python:3.12.2

# Set the working directory in the container
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
COPY ./OpenSans-Regular.ttf /app/OpenSans-Regular.ttf
COPY ./runner.py /app/runner.py
COPY ./check.sh /app/check.sh

RUN pip install check50
RUN pip install style50
RUN pip install submit50

RUN pip install -r requirements.txt

ENTRYPOINT ["./check.sh"]

