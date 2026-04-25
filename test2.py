from hyperswarm import HyperswarmInterface
import time


hs = HyperswarmInterface()
n = int(input("num"))
print(hs.create("elmeutopic"))

time.sleep(4)

if n == 1:
    print(hs.send("hello world!"))

if n == 2:
    print(hs.recv())
    print(hs.send("I <3 club mate"))

if n == 1:
    time.sleep(2)
    print(hs.nrecv())
    print(hs.nrecv())
    



