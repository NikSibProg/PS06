import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Инициализация браузера
driver = webdriver.Chrome()

# URL для парсинга
url = "https://www.divan.ru/sankt-peterburg/category/kresla"
driver.get(url)

# Ожидание загрузки карточек товаров
WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-testid="product-card"]')))

# Список для хранения данных
parsed_data = []

# Находим карточки с товарами
armchairs = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="product-card"]')

# Перебираем карточки
for armchair in armchairs:
    try:
        # Название кресла
        title_element = armchair.find_element(By.CSS_SELECTOR, 'span[itemprop="name"]')
        title = title_element.text if title_element else "Не указано"

        # Текущая цена
        current_price_element = armchair.find_elements(By.CSS_SELECTOR, 'span[data-testid="price"]')
        current_price = current_price_element[1].text.replace('руб.', '').strip() if len(current_price_element) > 0 else "Не указано"

        # Старая цена
        old_price = current_price_element[2].text.replace('руб.', '').strip() if len(current_price_element) > 1 else "Не указано"

        # Ссылка на товар
        link_element = armchair.find_element(By.CSS_SELECTOR, 'a.ui-GPFV8')
        link = "https://www.divan.ru" + link_element.get_attribute('href') if link_element else "Не указано"

        # Вычисляем скидку
        discount = "0%"
        if old_price != "Не указано" and current_price != "Не указано":
            old_price = int(old_price.replace(" ", ""))
            current_price = int(current_price.replace(" ", ""))
            discount = f"{round((old_price - current_price) / old_price * 100)}%"

        # Добавляем данные в список
        parsed_data.append([title, current_price, discount, link])
        print(f"Добавлено: {title}, {current_price}, {discount}, {link}")
    except Exception as e:
        print(f"Ошибка при парсинге карточки: {e}")
        continue

# Закрываем браузер
driver.quit()

# Сохраняем данные в CSV
with open("divanru.csv", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Название кресла', 'Цена', 'Скидка %', 'Ссылка на кресло'])
    writer.writerows(parsed_data)

print("Данные успешно сохранены в divanru.csv")
