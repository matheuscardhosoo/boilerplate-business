FROM python:3.10

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

ARG PORT=8000

ENV PORT=$PORT
ENV LOG_LEVEL="INFO"
ENV CONFIG_PATH="containers/system_configuration.yaml"
ENV ENV="test"
ENV SERVICE_NAME="boilerplate-business"

EXPOSE $PORT

ENTRYPOINT gunicorn -w 3 -k uvicorn.workers.UvicornWorker --timeout 7000 --preload --capture-output --bind "0.0.0.0:$PORT" --chdir src main:app