import time

ticks1 = time.time()
time1 = time.localtime(ticks1)
time.sleep(3)
ticks2 = time.time()
time2 = time.localtime(ticks2)

print("Ticks1: "+str(ticks1)+"\tTime1: "+time.asctime(time1))
print("Ticks2: "+str(ticks2)+"\tTime2: "+time.asctime(time2))

ltTicks = ticks1 < ticks2
ltTime = time1 < time2

print("Ticks1 < Ticks2: "+str(ltTicks))
print("Time1 < Time2: "+str(ltTime))
