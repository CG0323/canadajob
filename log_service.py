import logging

logger = logging.getLogger("scraper")
handler = logging.FileHandler("/home/ec2-user/scraper.log")  
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

def get_logger():
    return logger