import logging
import os

def setup_logging():
    """Configures the logging for the application."""
    log_file = os.path.join(os.path.dirname(__file__), '..', '..', 'pharmacy.log')

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()  # Also log to console
        ]
    )
