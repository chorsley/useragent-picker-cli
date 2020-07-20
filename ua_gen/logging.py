from loguru import logger
import sys

logger.remove()
logger.add(sys.stderr, format="{message}", level="INFO")