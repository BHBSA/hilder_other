from celery import Celery

app = Celery('tasks', broker='pyamqp://192.168.0.235:5673//')


@app.task
def add(x, y):
    return x + y
