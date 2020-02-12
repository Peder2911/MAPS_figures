import functools
from matplotlib import pyplot as plt
import logging

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

def blitTo(path):
    def dec(func):
        @functools.wraps(func)
        def inner(*args,**kwargs):
            plt.clf()
            func(*args,**kwargs)
            plt.savefig(path)
            logger.info(f"Saved plot to {path}")
        return inner
    return dec
