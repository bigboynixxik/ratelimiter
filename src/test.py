import asyncio
import time
from datetime import datetime

from main import SlidingWindowRateLimiter


async def mock_api_request(req_id: int) -> dict:
    """Мок-функция, имитирующая ответ от внешнего API"""
    await asyncio.sleep(0.05)
    return {"status": 200, "data": f"Обработан {req_id}"}


async def worker(req_id: int, limiter: SlidingWindowRateLimiter):
    """Задача, отправляющая запрос через лимитер"""
    async with limiter:
        current_time = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        response = await mock_api_request(req_id)
        print(
            f"[{current_time}] Запрос {req_id:03d} отправлен | Ответ: {response['status']}")


async def main():
    print("Старт теста: 100 запросов (Лимит: 10 запросов в 1 секунду)\n")

    limiter = SlidingWindowRateLimiter(requests_limit=10, time_window=1.0)
    start_time = time.perf_counter()

    tasks = [worker(i, limiter) for i in range(1, 101)]
    await asyncio.gather(*tasks)

    end_time = time.perf_counter()
    print("\nТест успешно завершен.")
    print(f"Общее время выполнения: {end_time - start_time:.2f} секунд")


if __name__ == "__main__":
    asyncio.run(main())
