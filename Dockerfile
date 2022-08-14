FROM python:3.9

WORKDIR /wordcollect-app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./ ./

CMD ["python","./app.py"]