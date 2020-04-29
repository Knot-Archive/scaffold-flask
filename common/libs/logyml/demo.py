import logging

from .logging import setup_logging

setup_logging()
logger = logging.getLogger("Common")
logger.info("info")
logger.warning("warning")
logger.debug("debug")
logger.error("error")
logger.fatal("fatal")
