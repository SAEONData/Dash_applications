FROM python:3.9

WORKDIR /srv
COPY app.py index.py requirements.txt ./
COPY apps apps/
COPY assets assets/
RUN pip install -r requirements.txt

CMD ["gunicorn", "index:server", "--bind=0.0.0.0:8050", "--workers=4"]
