from datetime import datetime
import time
x = time.time()
print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(x)))

print(str(datetime.now()))