FROM python:3.7.1

WORKDIR /app

COPY ./ /app

RUN pip3 install --upgrade pip
RUN pip3 install poetry
RUN poetry config virtualenvs.create false && poetry install
RUN chmod +x entrypoint.sh

ENV FLASK_APP=adonai.app

EXPOSE 5000

ENTRYPOINT [ "./entrypoint.sh" ]