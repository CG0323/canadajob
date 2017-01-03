import logging

logger = logging.getLogger("scraper")
handler1 = logging.FileHandler("/home/ec2-user/scraperdebug.log")  
formatter1 = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler1.setFormatter(formatter)
handler1.setLevel(logging.DEBUG)
logger.addHandler(handler1)
handler2 = logging.FileHandler("/home/ec2-user/scraperinfo.log")  
formatter2 = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler2.setFormatter(formatter)
handler2.setLevel(logging.INFO)
logger.addHandler(handler2)


def get_logger():
    return logger