FROM python:3.11

# Set the working directory in the container
WORKDIR /app

COPY ./check.sh /app/check.sh

RUN pip install check50
RUN pip install style50
RUN pip install submit50

ENTRYPOINT ["./check.sh"]

