"""Main entry point for Ralph application."""

import threading
import time
import signal
import sys

import uvicorn

from src.api import app
from src.config import Config
from src.logging_config import configure_logging, get_logger


class RalphApplication:
    """Main application orchestrator."""

    def __init__(self, config: Config):
        self.config = config
        self.logger = get_logger(__name__)
        self._shutdown_event = threading.Event()
        self._server_thread: threading.Thread | None = None

    def _run_server(self) -> None:
        """Run FastAPI server in background thread."""
        config = uvicorn.Config(
            app=app,
            host=self.config.host,
            port=self.config.port,
            log_level=self.config.log_level.lower(),
        )
        server = uvicorn.Server(config)
        server.run()

    def start_api_server(self) -> None:
        """Start the FastAPI server in a background thread."""
        self.logger.info(
            "starting_api_server",
            host=self.config.host,
            port=self.config.port,
        )
        self._server_thread = threading.Thread(
            target=self._run_server,
            daemon=True,
            name="api-server",
        )
        self._server_thread.start()

    def run_console(self) -> None:
        """Run the console application loop."""
        self.logger.info("ralph_console_started")
        print("\n" + "=" * 50)
        print("  Ralph Trading Infrastructure")
        print("  API running at http://{}:{}".format(
            self.config.host, self.config.port
        ))
        print("  Press Ctrl+C to exit")
        print("=" * 50 + "\n")

        while not self._shutdown_event.is_set():
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                break

    def shutdown(self) -> None:
        """Graceful shutdown."""
        self.logger.info("shutting_down")
        self._shutdown_event.set()


def main() -> None:
    """Main entry point."""
    config = Config.from_env()
    configure_logging(config.log_level)
    
    logger = get_logger(__name__)
    logger.info("ralph_starting", version="0.1.0")

    application = RalphApplication(config)

    def signal_handler(signum: int, frame) -> None:
        logger.info("signal_received", signal=signum)
        application.shutdown()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start API server in background
    application.start_api_server()
    
    # Give server time to start
    time.sleep(1)
    
    # Run console loop
    application.run_console()


if __name__ == "__main__":
    main()
