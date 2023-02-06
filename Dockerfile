FROM python:3.10-alpine
ENV PYTHONUNBUFFERED 1

WORKDIR /src

COPY ./src /src

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip3 install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh src/entrypoint.sh
RUN sed -i 's/\r$//g' src/entrypoint.sh
RUN chmod +x src/entrypoint.sh

# export python path variable
ENV PYTHONPATH "${PYTHONPATH}:/src"

ENTRYPOINT ["sh", "src/entrypoint.sh"]