import asyncio
from playwright.async_api import async_playwright
from datetime import datetime

# Глобальная переменная для пути к файлу
file_path = ""

# Функция для мокирования ответа сервера с указанным путем к файлу
async def fulfill_route(route):
    with open(file_path, "r") as file:
        content = file.read()
        await route.fulfill(status=200, body=content)

async def main():
    global file_path  # Объявляем переменную как глобальную, чтобы использовать внутри функции

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Список тестов и путей к данным для них
        tests = [
            {"name": "test1", "path": "responses/test1.json"},
            {"name": "test2", "path": "responses/test2.json"},
            {"name": "test3", "path": "responses/test3.json"},
            {"name": "test4", "path": "responses/test4.json"},
            {"name": "test5", "path": "responses/test5.json"},
            {"name": "test6", "path": "responses/test6.json"},
            {"name": "test7", "path": "responses/test7.json"},
            {"name": "test8", "path": "responses/test8.json"},
            {"name": "test9", "path": "responses/test9.json"},
            {"name": "test10", "path": "responses/test10.json"},
            {"name": "test11", "path": "responses/test11.json"}, 
            {"name": "test12", "path": "responses/test12.json"},
            {"name": "test13", "path": "responses/test13.json"},
            {"name": "test14", "path": "responses/test14.json"},
            {"name": "test15", "path": "responses/test15.json"},
            {"name": "test16", "path": "responses/test16.json"}
        ]
        
        # Перебираем каждый тест
        for test in tests:
            now_day = datetime.now().strftime('%Y.%m.%d_%H.%M.%S')
            
            # Устанавливаем путь к файлу для текущего теста
            file_path = test["path"]
            
            # Мокируем ответ сервера для текущего теста
            await page.route(
                "**/web/1/charity/ecoImpact/init",
                lambda route: fulfill_route(route)
            )
            
            # Переходим на страницу
            await page.goto('https://www.avito.ru/avito-care/eco-impact')
            
            # Ожидаем появления элемента счётчика
            await page.wait_for_selector('#app > div > div:nth-child(3) > div > div > div > div > div:nth-child(3) > div > div.desktop-impact-items-F7T6E')
            
            # Получаем элемент счётчика
            element = await page.query_selector('#app > div > div:nth-child(3) > div > div > div > div > div:nth-child(3) > div > div.desktop-impact-items-F7T6E')
            
            # Создаём скриншот элемента счётчика
            if element:
                await element.screenshot(path=f'output/screen_{test["name"]}_' + now_day + '.png')
                print(f"Создан скриншот для {test['name']}")
            else:
                print(f"Не удалось создать скриншот для {test['name']}. Элемент не найден.")
        
        await browser.close()

asyncio.run(main())