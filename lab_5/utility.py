import time


class Timer:
    def __init__(self, name: str = "Timer") -> None:
        self.timer_name = name
        self.start_time = None

    def __call__(self) -> None:
        if self.start_time is None:
            self.start_time = time.perf_counter()
            print(f"{self.timer_name} started.")
        else:
            elapsed = time.perf_counter() - self.start_time
            print(f"{self.timer_name} finished in {elapsed:.4f} seconds.")
            self.start_time = None
