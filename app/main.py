import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from app.study_plan import study_api
from app import settings # Import the settings
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
    # print(f"Configuring OTLP exporter for endpoint: {otlp_endpoint}")
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
            
    # print(f"DEBUG: OTLP Exporter Headers: {headers}")
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

# Configure CORS from settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.ALLOWED_METHODS,
    allow_headers=settings.ALLOWED_HEADERS,
)

# Instrument FastAPI app
FastAPIInstrumentor.instrument_app(app)

# Include routers
app.include_router(study_api.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
