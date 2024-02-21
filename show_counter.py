from functools import wraps

from flask import Flask
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST, start_http_server
from flask import Response

app = Flask(__name__)
webhook_counter = Counter('webhook_requests_total', 'Total number of webhook requests received')


def count_webhook(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        webhook_counter.inc()
        return func(*args, **kwargs)

    return wrapper


@count_webhook
@app.route("/")
def hello_world():
    webhook_counter.inc()
    return "<p>Hello, World!</p>"


if __name__ == '__main__':
    start_http_server(8000)
    app.run(port=5000)


# def count_webhook(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         webhook_counter.inc()
#         return func(*args, **kwargs)
#
#     return wrapper
# time_metric = Histogram('request_latency_seconds', 'Description of histogram')
# webhook_counter = Counter('webhook_requests_total', 'Total number of webhook requests received')# to count webhook  received
# g = Gauge('my_inprogress_requests', 'Description of gauge')# to count succsessfull requests
