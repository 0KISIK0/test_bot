from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options

def get_books_name():
    chrome_option = Options()
    chrome_option.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_option)
    driver.get("http://selenium1py.pythonanywhere.com/ru/")

    login(driver)

    basket_button = driver.find_element(By.XPATH, '//*[@id="default"]/header/div[1]/div/div[2]/span/a')
    basket_button.click()

    books_list = driver.find_elements(By.CSS_SELECTOR,".basket-items .row .col-sm-4 >h3")
    result_list = []
    for book in books_list:
        result_list.append(book.text)

    driver.quit()
    return result_list


def login(driver):

    login = driver.find_element(By.ID, "login_link")
    login.click()

    login_email = driver.find_element(By.ID, "id_login-username")
    login_email.send_keys("rrterter@gmail.com")

    login_pass = driver.find_element(By.ID, "id_login-password")
    login_pass.send_keys("qwe123123qwe")

    button = driver.find_element(By.NAME, "login_submit")
    button.click()


def add_book(name):
    chrome_option = Options()
    chrome_option.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_option)
    try:
        driver.get("http://selenium1py.pythonanywhere.com/ru/")

        login(driver)

        inpt = driver.find_element(By.ID, "id_q")
        inpt.send_keys(name)

        submit_inpt = driver.find_element(By.CSS_SELECTOR, ".navbar-form.navbar-right > input")
        submit_inpt.click()
        
        add_to_basket = driver.find_element(By.CSS_SELECTOR, ".btn.btn-primary.btn-block")
        add_to_basket.click()
        return True
    except:
        return False
    finally: driver.quit()



def find_number_gdz(message:str)->list:
    """_summary_

    Args:
        message (str): Текстовое сообщение которое разделится на номер и предмет.
        number (int or str): Номер задания который нужно найти.
        subject (str): Название предмета который ищем

    Returns:
        list: 
            1.Если все успешно возвращает список с сылками на картинки.
            2.Если не правильно введен номер возвращает список с фразой Неправильно введен номер.
            3.Если не правильно введен предеме возвращает список с фразой Неправильно введен предмет.
    """
    try:
        subject,number = message.split(" ")
    except ValueError:
        return ["Извините я не могу обратотать такой ввод. Попробуйсте еще раз, Алгебра 93"]
    number = str(number)
    subject = subject.lower()
    subject_link = ""
    if subject == "русский":
        subject_link = "russkii_yazik/barhudarov-8"
        number = number + "-nom"
    elif subject == "алгебра":
        subject_link = "algebra/kolyagin-tkacheva"
        number = number + "-nom"
    elif subject == "геометрия":
        subject_link = "geometria/atanasyan-8"
        number = number + "-task"
    elif subject == "английский":
        subject_link = "english/kuzovlev-sb8"
        number = number + "-s"
    else:
        return ["Не правильно введино название предмета."]
    link = f"https://gdz.ru/class-8/{subject_link}/{number}/"
    chrome_option = Options()
    chrome_option.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_option)
    try:
        driver.implicitly_wait(5)
        driver.get(link)
        imges = driver.find_elements(By.CSS_SELECTOR, ".with-overtask > img")
        links = []
        for element in imges:
            src = element.get_attribute("src")
            links.append(src)
        if not links:
            return ["Не удалось найти номер."]
        else:
            return links
    except:
        return ["Не удалось найти номер."]
    finally: driver.quit()

if __name__ == "__main__":
    print(find_number_gdz(34,"sgfxcf"))