from prometheus_client import Counter, Histogram, Gauge

# Counters
HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "route", "status"]
)

INGEST_ROWS_TOTAL = Counter(
    "ingest_rows_total",
    "Total rows ingested per symbol",
    ["symbol"]
)

INGEST_BATCHES_TOTAL = Counter(
    "ingest_batches_total",
    "Total ingest batches processed"
)

# Histograms
HTTP_REQUEST_LATENCY = Histogram(
    "http_request_latency_seconds",
    "HTTP request latency in seconds",
    ["method", "route"]
)

INGEST_PROCESSING_SECONDS = Histogram(
    "ingest_processing_seconds",
    "Time spent processing ingest batches"
)

# Gauges
STORE_POINTS = Gauge(
    "store_points",
    "Current points stored per symbol",
    ["symbol"]
)

STORE_SYMBOLS_TOTAL = Gauge(
    "store_symbols_total",
    "Total symbols currently tracked"
)
