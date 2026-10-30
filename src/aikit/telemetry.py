# src/aikit/telemetry.py   (uv add opentelemetry-sdk opentelemetry-exporter-otlp)
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

provider = TracerProvider(resource=Resource.create({"service.name": "policy-assistant"}))
provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("aikit")


def traced_chat(llm, messages, system=None, *, prompt_name: str, prompt_version: int, **kw):
    with tracer.start_as_current_span("chat") as span:
        span.set_attribute("gen_ai.operation.name", "chat")
        span.set_attribute("gen_ai.provider.name", llm.provider)
        span.set_attribute("gen_ai.request.model", llm.model)
        span.set_attribute("aikit.prompt.name", prompt_name)
        span.set_attribute("aikit.prompt.version", prompt_version)
        r = llm.chat(messages, system=system, **kw)
        span.set_attribute("gen_ai.usage.input_tokens", r.input_tokens or 0)
        span.set_attribute("gen_ai.usage.output_tokens", r.output_tokens or 0)
        span.set_attribute("gen_ai.response.finish_reasons", [r.stop_reason or ""])
        return r
