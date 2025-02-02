import aiohttp
import asyncio
import ssl

# URL сайта для проверки
URL = "https://lms.kantiana.ru/lib/ajax/service-nologin.php"

# Заголовки запроса
HEADERS = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",

    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://lms.kantiana.ru/"
}

# Параметры запроса
PARAMS = {
    "info": "core_output_load_template_with_dependencies",
    "cachekey": "1737355256",

}

# Настройка SSL для игнорирования ошибок сертификата
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


# Асинхронная функция для отправки запроса
async def send_request(session):
    try:
        async with session.get(URL, headers=HEADERS, params=PARAMS, ssl=ssl_context) as response:
            status = response.status
            body = await response.text()
            print(f"Response: {status}\nBody: {body[:200]}...")
    except Exception as e:
        print(f"Request failed: {e}")


# Асинхронная функция для запуска теста с заданным числом запросов
async def perform_test(concurrent_requests):
    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session) for _ in range(concurrent_requests)]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    # Укажите число одновременных запросов
    concurrent_requests = 10

    # Запуск теста
    asyncio.run(perform_test(concurrent_requests))
