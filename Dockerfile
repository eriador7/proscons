# Übernommen Basis
# Eigenentwicklung Anpassungen

FROM python:slim

RUN useradd proscons

WORKDIR /home/proscons

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY proscons proscons
COPY data.sql data.sql
COPY boot.sh boot.sh
RUN chmod +x boot.sh

ENV FLASK_APP proscons

RUN chown -R proscons:proscons ./
#RUN venv/bin/pip install ./proscons
USER proscons

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
