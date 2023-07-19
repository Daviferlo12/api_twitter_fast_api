from datetime import datetime, timedelta
import time

print(datetime.utcnow())
print(datetime(1970, 1, 1) + timedelta(seconds=time.time()))
print(datetime(*time.gmtime()[:6]))


