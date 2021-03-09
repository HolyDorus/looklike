from multiprocessing import cpu_count


def max_workers():
    # Formula: Physical CPU cores * 2 + 1
    return cpu_count() + 1


bind = 'localhost:5000'
max_requests = 1000
worker_class = 'sync'
workers = max_workers()
