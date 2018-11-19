import os

fo = open("test.txt", "w")
str = '148\tstat.funshion.net\t294\t4.1846774567742\t1.59391195052098\t0.1781\t1\t1\n'
for i in range(1, 45004):
    fo.write(str)

fo.close()