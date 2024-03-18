FROM python:3.12.2

# Set the working directory in the container
WORKDIR /app

COPY . .

RUN pip install check50
RUN pip install style50
RUN pip install submit50

ENTRYPOINT ["./check.sh"]

