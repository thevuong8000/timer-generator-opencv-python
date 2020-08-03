import sys
from time import sleep

def get_workload_done(done):
    rem = 100 - done
    done = int(done * 30)
    res = '█' * done + '.' * (30 - done)
    return res;


print(get_workload_done(0.75))