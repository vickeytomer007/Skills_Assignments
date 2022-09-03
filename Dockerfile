FROM python:3.9-slim

WORKDIR /workspace/Skills_Assignments

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT ["python3","main.py"]