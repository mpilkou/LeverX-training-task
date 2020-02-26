from threading import Thread, Lock
from concurrent.futures import ThreadPoolExecutor
import typing


a = 0

def function1(arg : int, lock : typing.TypeVar('Lock')) -> int:
    tmp = 0

    for _ in range(arg):
        tmp += 1

    with lock:
        global a
        a += tmp


def function2(arg : int) -> int:
    a = 0
    for _ in range(arg):
        a += 1
    return a

def main() -> None:
    
    # using previos solution
    threads = []
    lock = Lock()
    for _ in range(5):
        thread = Thread(target=function1, args=(1000000,lock))
        thread.start()
        threads.append(thread)

    [t.join() for t in threads]
    print("----------------------", a)  # ???


    # using thread pool
    with ThreadPoolExecutor(max_workers=5) as executor:
        future = executor.submit(function2, 5000000)
        future.result()

        print("----------------------", future.result())


main()
