FROM ubuntu:jammy

RUN mkdir /app
RUN apt update && apt upgrade -y
RUN apt install -y python3 python3-pip curl netcat
RUN apt-get update && apt-get upgrade
RUN apt-get install git -y
RUN apt-get update -y && apt-get install -y gcc

ADD requirements2.txt /app

RUN python3 -m pip install -r /app/requirements2.txt
RUN pip install git+https://github.com/cene555/ru-clip.git
RUN pip install uvicorn
ADD run.sh main.py e_places2.csv n_places2.csv v_places2.csv y_places2.csv latents2.pt latents3.pt fixes.json ml_module.py main.py /app
RUN chmod +x /app/run.sh
CMD PYTHONPATH=/app /app/run.sh