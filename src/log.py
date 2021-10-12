import logging


def setup_logging(log_file_name=None, log_level='INFO'):
    logging.basicConfig(level=log_level.upper())

    root = logging.getLogger()
    root.setLevel(log_level.upper())

    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    if log_file_name:
        root.addHandler(logging.FileHandler(log_file_name))

    formatter = logging.Formatter('[%(asctime)s] - %(levelname)s - %(module)s - %(message)s', '%m-%d %H:%M:%S')

    for h in root.handlers:
        h.setFormatter(formatter)
        h.setLevel(log_level.upper())

    # ch = logging.StreamHandler()
    # ch.setLevel(logging.DEBUG)
