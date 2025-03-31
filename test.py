import multiprocessing

max_threads = multiprocessing.cpu_count() * 2  # или *4, если нагрузка I/O-шная
print(f"Рекомендуемое количество потоков: {max_threads}")
