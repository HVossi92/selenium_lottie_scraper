from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.wait import WebDriverWait
import requests

PATH = "/Applications/chromedriver"
download_dir = "/Users/h.vosskamp/Documents/Private/Hagen/2021_22_WiSe/Master_Thesis/Webscraping/Lottie_Jsons/"


def scrape_pages(num_pages):
    for page_number in range(num_pages):
        page_number = page_number + 46
        driver = webdriver.Chrome(PATH)
        print(f"{page_number} Scrape 'https://lottiefiles.com/featured?page={page_number}'")
        driver.get(f"https://lottiefiles.com/featured?page={page_number}")

        try:
            WebDriverWait(driver, 10).until(presence_of_element_located((By.CLASS_NAME, 'lottieanimation')))
            print("Page is ready!")
            elements = driver.find_elements(By.CLASS_NAME, 'lottieanimation')
            for element in elements:
                print(f"{element} / {len(elements)} ond {page_number}")
                get_json_and_write_to_disk(element)
        except TimeoutException:
            print("Loading took too much time!")
        driver.quit()


def get_json_and_write_to_disk(element):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    url = element.get_attribute("src")
    request = requests.get(url, headers=headers)
    last_slash = url.rfind('/')
    file_name = url[last_slash + 1:-4]
    print(element.get_attribute("src"))
    with open(download_dir + file_name + '.json', 'wb') as f:
        f.write(request.content)


if __name__ == '__main__':
    scrape_pages(98)
    print("Done")
