import logging
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('crawler')

from datetime import datetime
def strToDatetime(dateStr):
  strs = dateStr.split('-')
  if len(strs) != 3:
    return None
  return datetime(int(strs[0]),int(strs[1]),int(strs[2]))

