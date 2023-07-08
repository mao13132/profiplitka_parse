import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from datetime import datetime


class SourceParsePlu:
    def __init__(self, driver, count_page, collect, BotDB):
        self.driver = driver
        self.source_name = 'profiplitka'
        self.links_post = []
        self.count_page = count_page
        self.collect = collect
        self.url = f'https://profiplitka.ru/plitka/{collect}/elements/'
        self.BotDB = BotDB

    def load_page(self, url):
        try:
            self.driver.get(url)
            return True
        except Exception as es:
            print(f'Ошибка при заходе на стартовую страницу "{es}"')
            return False

    def __check_load_page(self):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'favorites__row')]")))
            return True
        except:
            return False

    def loop_load_page(self):
        count = 0
        count_ower = 10

        while True:

            count += 1

            if count >= count_ower:
                print(f'Не смог открыть {self.source_name}')
                return False

            start_page = self.load_page(self.url)

            if not start_page:
                continue

            check_page = self.__check_load_page()

            if not check_page:
                self.driver.refresh()
                continue

            print(f'Успешно зашёл на {self.source_name}')

            return True

    def get_all_post(self):
        try:
            rows_post = self.driver.find_elements(by=By.XPATH,
                                                  value=f"//*[@id='products']"
                                                        f"//*[contains(@class, 'favorites__row')]/div")


        except Exception as es:
            print(f'Ошибка при получение постов"{es}"')
            return False

        return rows_post

    def click_paginator(self):
        try:
            next_paginator = self.driver.find_elements(by=By.XPATH,
                                                       value=f"//*[contains(@class, 'page-n')]"
                                                             f"//a[contains(@class, 'active')]/following-sibling::a")


        except Exception as es:
            print(f'Ошибка при переключение страницы "{es}"')
            return False

        if next_paginator == []:
            return False

        try:
            next_paginator[0].click()
        except Exception as es:
            print(f'Ошибка при кликен на пагинатор "{es}"')
            return False

        return True

    def get_link(self, row):
        try:
            link_post = row.find_element(by=By.XPATH, value=f".//a[contains(@class, 'link')]") \
                .get_attribute('href')
        except:
            link_post = ''

        return link_post

    def get_name(self, row):
        try:
            name_post = row.find_element(by=By.XPATH, value=f".//a[contains(@class, 'link')]").text
        except:
            name_post = ''

        return name_post


    def get_coutry(self, row):
        try:
            har_ = row.find_element(by=By.XPATH, value=f".//p[contains(@class, 'info')]").text
        except:
            return '', ''

        try:
            coutry = har_.split()[-1]
        except:
            coutry = ''
        try:
            artikl = har_.split()[1]
        except:
            artikl = ''




        return coutry, artikl



    def itter_rows_post(self, rows_post):

        for row in rows_post:
            status = True

            link = self.get_link(row)
            name = self.get_name(row)
            coutry, artikl = self.get_coutry(row)

            good_itter = {}

            good_itter['link'] = link
            good_itter['name'] = name
            good_itter['coutry'] = coutry
            good_itter['artikl'] = artikl
            good_itter['collection'] = self.collect

            chech_double = self.BotDB.exist_plu(artikl, self.collect)
            if chech_double != []:
                status = False
                print(f'Найден дубль')

            if status:
                self.BotDB.add_plu(link, name, artikl, self.collect)

            self.links_post.append(good_itter)

        return True

    def step_one_parse(self):

        _count_page = 0

        while True:

            rows_post = self.get_all_post()

            if rows_post == [] or rows_post is None:
                return False

            response = self.itter_rows_post(rows_post)

            _count_page += 1

            if _count_page >= self.count_page and self.count_page != 0:
                print(f'Сработал ограничитель в {self.count_page} страниц')
                return True

            print(f'Обработал {_count_page} PLU')

            click_paginator = self.click_paginator()

            if not click_paginator:
                return True


    def start_pars_plu(self):

        result_start_page = self.loop_load_page()

        if not result_start_page:
            return False

        response_one_step = self.step_one_parse()

        return self.links_post
