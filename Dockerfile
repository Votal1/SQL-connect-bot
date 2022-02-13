FROM python:3
WORKDIR /
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . /
ENTRYPOINT ["nohup", "python", "main.py"]