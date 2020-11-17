FROM python:3.7-alpine
ADD . /code
WORKDIR /code
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r modules/core/requirements.txt
EXPOSE 5000
# CMD [ "python", "services/app_main.py" ]