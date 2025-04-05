from flask import Flask, render_template, jsonify
import logging
from routes.favorites import favorites_bp
from routes.media import media_bp
from routes.api import api_bp
from routes.main import main_bp
import os
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Only enable OpenTelemetry if OTEL_ENABLED environment variable is set
if os.getenv('OTEL_ENABLED'):
    # OpenTelemetry imports
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.instrumentation.flask import FlaskInstrumentor
    from opentelemetry.instrumentation.requests import RequestsInstrumentor
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

    # Define your service
    resource = Resource.create({
        "service.name": "entertainment-website",
        "service.version": "1.0.0",
        "deployment.environment": "development"
    })

    tracer = TracerProvider(resource=resource)
    otlp_endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4318")
    
    try:
        otlp_exporter = OTLPSpanExporter(
            endpoint=f"{otlp_endpoint}/v1/traces"
        )
        tracer.add_span_processor(BatchSpanProcessor(otlp_exporter))
        trace.set_tracer_provider(tracer)
        FlaskInstrumentor().instrument_app(app)
        RequestsInstrumentor().instrument()
        logger.info("OpenTelemetry initialized successfully")
    except Exception as e:
        logger.warning(f"Failed to initialize OpenTelemetry: {str(e)}")

# Register blueprints
app.register_blueprint(favorites_bp)
app.register_blueprint(media_bp)
app.register_blueprint(api_bp)
app.register_blueprint(main_bp)

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'service': 'entertainment-website',
        'timestamp': datetime.now().isoformat()
    })

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
