from functools import wraps
from flask import Flask
from prometheus_client import Counter, start_http_server, Histogram, Gauge
from prometheus_flask_exporter import PrometheusMetrics
import time
import requests
import threading

app = Flask(__name__)
g = Gauge('my_progress_requests', 'Description of gauge')# to count succsessfull requests
metrics = PrometheusMetrics(app, group_by='endpoint')
# Create a metric to track time spent and requests made.
url = 'https://487f-193-169-71-150.ngrok-free.app/callback'


def send_request():
    for i in range(0, 20):
        print(i)
        time.sleep(2)
        response = requests.post(url=url, data=str(i))
        if response.status_code == 200:
            g.inc()
            g.time()


@app.route("/callback", methods=['POST'])
@metrics.counter('webhook_requests_total', 'Total number of webhook requests received') #Counters go up, and reset when the process restarts.
@metrics.histogram('request_latency_seconds', 'Description of histogram')        # @Histograms track the size and number of events in buckets. This allows for aggregatable calculation of quantiles.
def counter_callback():
    print("Callback")
    return "<p> callback has got  </p>"


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == '__main__':
    # Start Prometheus HTTP server for metrics
    # start_http_server(8000)
    # Start the Flask application
    thread = threading.Thread(target=send_request)
    thread.start()
    # Start sending requests
    app.run(host='0.0.0.0', port='5000')