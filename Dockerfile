FROM python:3.11.3-slim-bullseye
COPY . /usr/share/osm-rcaf/src/
WORKDIR /usr/share/osm-rcaf/
RUN pip install --no-cache-dir -r src/configs/requirements.txt
EXPOSE 5000
CMD [ "python", "-m", "src.webserver"]