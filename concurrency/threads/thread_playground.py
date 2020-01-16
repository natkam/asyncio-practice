import concurrent
import threading
import time
from concurrent.futures import ThreadPoolExecutor

thread_local = threading.local()


def get_thread_value(value):
    if not hasattr(thread_local, "value"):
        print(f"setting value: {value}")
        thread_local.value = value
    time.sleep(2)
    print(thread_local.value)


def example_1():
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=4) as executor:
        ## this would operate on a single thread!
        # for _ in range(10):
        #     get_thread_value()
        #     print(thread_local.value)

        executor.map(get_thread_value, list(range(10)))
    print(f"Took {time.perf_counter() - start} to execute.")


def wait(name):
    print(f"Thread {name}: start waiting...")
    time.sleep(2)
    print(f"Thread {name}: finished waiting")


def example_2():
    t = threading.Thread(target=wait, args=("one",))  # daemon=True => has to be join()-ed
    print("BEFORE START")
    t.start()
    print("WAITING")
    # t.join()
    print("MAIN EXIT")


def example_3():
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(wait, range(3))


if __name__ == "__main__":
    example_3()