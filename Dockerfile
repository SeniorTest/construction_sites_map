FROM python:3.7

COPY . /app
COPY map /app/map
COPY project_cards /app/project_cards
WORKDIR /app

RUN pip install dash
RUN pip install dash-core-components
RUN pip install dash-html-components
RUN pip install dash-bootstrap-components
RUN pip install folium
RUN python -m pip install gunicorn

# CMD ["gunicorn", "-b", "0.0.0.0:8050", "app:server"]
CMD ["python", "app.py"]