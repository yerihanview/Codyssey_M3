import time

def measure_mac_time(pattern, filter_, repeat=10):

    elapsed_times = []

    for _ in range(10):
        start = time.perf_counter()
        mac(pattern, filter_, repeat)
        end = time.perf_counter()

        elapsed = (end - start)*1000
        elapsed_times.append(elapsed)

    avg_time = sum(elapsed_times)/repeat


