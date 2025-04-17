import os
from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

# Setup OpenTelemetry

# Define resource with service name
resource = Resource.create({"service.name": "study-agent-backend"})

# Set tracer provider
tracer_provider = TracerProvider(resource=resource)
trace.set_tracer_provider(tracer_provider)

# Configure OTLP exporter from environment variables
otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
otlp_headers = os.getenv("OTEL_EXPORTER_OTLP_HEADERS")

if otlp_endpoint:
    print(f"Configuring OTLP exporter for endpoint: {otlp_endpoint}")
    # Parse headers if they exist (e.g., "key1=value1,key2=value2")
    headers = {}
    if otlp_headers:
        try:
            # Split only on the first '=' for each header pair
            headers = dict(item.split("=", 1) for item in otlp_headers.split(","))
        except ValueError:
            print(
                "Warning: Could not parse OTEL_EXPORTER_OTLP_HEADERS. Ensure format is key1=value1,key2=value2"
            )
            
    print(f"DEBUG: OTLP Exporter Headers: {headers}")
    otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint, headers=headers)
    processor = BatchSpanProcessor(otlp_exporter)
    tracer_provider.add_span_processor(processor)
else:
    print(
        "Warning: OTEL_EXPORTER_OTLP_ENDPOINT not set. Falling back to ConsoleSpanExporter."
    )
    processor = BatchSpanProcessor(ConsoleSpanExporter())
    tracer_provider.add_span_processor(processor)


app = FastAPI()

# Instrument FastAPI app
FastAPIInstrumentor.instrument_app(app)


@app.get("/health")
def health_check():
    return {"status": "ok"}
