import structlog
from structlog.dev import ConsoleRenderer

structlog.configure(
    processors=[
        *filter(
            lambda processor: not isinstance(processor, ConsoleRenderer),
            structlog.get_config()["processors"].copy(),
        ),
        ConsoleRenderer(sort_keys=False),
    ]
)
log = structlog.get_logger()
