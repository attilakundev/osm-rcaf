FROM python:3.11.3-slim-bullseye
COPY . /usr/share/osm-rcaf/src/
WORKDIR /usr/share/osm-rcaf/
RUN pip install --no-cache-dir -r src/requirements.txt
CMD [ "uvicorn", "src.webserver:app", "--host", "0.0.0.0", "--port", "80" ]