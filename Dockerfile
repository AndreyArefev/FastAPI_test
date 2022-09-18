FROM python

WORKDIR /FastAPI_test

COPY ./requirements.txt /FastAPI_test/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /FastAPI_test/requirements.txt

COPY ./app /FastAPI_test/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

