from prometheus_client import Counter, Histogram

# Define your custom metrics
LIVENESS_CHECK = Counter('flask_app_liveness_check_total', 'Total liveness checks performed')
CALLBACK_COUNT = Counter('flask_app_callback_count_total', 'Total callback requests received')
SUCCESSFUL_MISSION_COUNT = Counter('flask_app_successful_mission_count_total', 'Total successful missions executed')

REQUEST_COUNTER = Counter('flask_app_requests_total', 'Total number of requests received')
REQUEST_LATENCY = Histogram('flask_app_request_latency_seconds', 'Request latency in seconds')


# Decorator to measure request latency
def record_request_data(f):
    def decorated_function(*args, **kwargs):
        with REQUEST_LATENCY.time():
            REQUEST_COUNTER.inc()
            return f(*args, **kwargs)

    return decorated_function


# Function to increase liveness check metric
def increase_liveness_check():
    LIVENESS_CHECK.inc()


# Function to increase callback count metric
def increase_callback_count():
    CALLBACK_COUNT.inc()


# Function to increase successful mission count metric
def increase_successful_mission_count():
    SUCCESSFUL_MISSION_COUNT.inc()
