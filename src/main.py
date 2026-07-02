import asyncio
import time
from collections import deque


class SlidingWindowRateLimiter:
    """
    Асинхронный Rate Limiter на основе алгоритма "Скользящее окно".
    Гарантирует, что за указанное временное окно будет выполнено не более заданного числа запросов.
    """

    def __init__(self, requests_limit: int, time_window: float):
        self.limit = requests_limit
        self.window = time_window
        self.history = deque()
        self._lock = asyncio.Lock()

    async def __aenter__(self):
        """Срабатывает при входе в блок 'async with'"""
        while True:
            async with self._lock:
                now = time.perf_counter()

                while self.history and now - self.history[0] >= self.window:
                    self.history.popleft()

                print(self.history)
                if len(self.history) < self.limit:
                    self.history.append(now)
                    return self

                sleep_time = self.window - (now - self.history[0])

            if sleep_time > 0:
                await asyncio.sleep(sleep_time)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Срабатывает при выходе из блока 'async with'"""
        pass
