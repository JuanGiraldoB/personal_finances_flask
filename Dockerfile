FROM python:alpine
ENV PYTHONBUFFERED 1
ENV FLASK_APP=project
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_DEBUG=1
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

EXPOSE 5000
CMD ["flask", "run"]