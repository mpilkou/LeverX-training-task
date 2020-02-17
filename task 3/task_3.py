from threading import Thread, Lock
from concurrent.futures import ThreadPoolExecutor


def function(arg):
    a = 0
    for _ in range(arg):
        a += 1
    return a


def main():
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        future = executor.submit(function, 5000000)
        future.result()

        print("----------------------", future.result())

main()
