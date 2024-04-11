FROM python:3.11.1-slim-buster

WORKDIR /frontend

COPY requirements.txt /frontend/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /frontend/requirements.txt

COPY ./pages /frontend/pages
COPY ./.streamlit /frontend/.streamlit
COPY main.py /frontend/main.py

ENTRYPOINT ["streamlit", "run", "main.py"]
