FROM python:3.9-slim

WORKDIR /app

COPY app/requirements.txt /app/requirements.txt

#RUN apt-get update && \
#    apt-get install -y --no-install-recommends python3.9-pip && \
#RUN pip3 install --no-cache-dir --upgrade -r /app/requirements.txt

RUN pip3 install --no-cache-dir fastapi
RUN pip3 install --no-cache-dir uvicorn
RUN pip3 install --no-cache-dir sentry_sdk
RUN pip3 install --no-cache-dir passlib[bcrypt]
RUN pip3 install --no-cache-dir python-jose[cryptography]
RUN pip3 install --no-cache-dir SQLAlchemy[aiomysql]
RUN pip3 install --no-cache-dir pydantic[dotenv]
RUN pip3 install --no-cache-dir email-validator
RUN pip3 install --no-cache-dir jinja2
RUN pip3 install --no-cache-dir python-multipart

COPY app/ /app/
COPY cfg/ /cfg/

CMD ["uvicorn", "main:app_fastapi", "--host", "0.0.0.0", "--port", "80", "--reload"]
