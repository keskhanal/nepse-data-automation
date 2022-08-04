FROM python:3.9

WORKDIR /automation

RUN python -m pip install --upgrade pip

COPY ./requirements.txt /automation/requirements.txt

RUN pip install -r requirements.txt

COPY . /automation

CMD ["python", "main.py"]