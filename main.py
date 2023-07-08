from datetime import datetime

from browser.createbrowser import CreatBrowser
from save_result import SaveResult
from src.plu_parse import PluParser
from src.source_parse import SourceParse

from src.temp import *


def main():
    # Ограничитель на кол-во страниц. Если поставить 0 то без ограничений
    count_page = 1

    browser_core = CreatBrowser()

    print(f'Парсер запущен. Получаю данные')

    # data_good = SourceParse(browser_core.driver, count_page).start_pars()
    data_good = data_list

    # data_good = data_good[:18]

    print(f'Собрал {len(data_good)} plu')

    ower_good_data = PluParser(browser_core.driver, data_good).start_pars()

    # ower_good_data = ower_list
    # print()

    file_name = f'{datetime.now().strftime("%H_%M_%S")}'

    SaveResult(ower_good_data).save_file(file_name)


if __name__ == '__main__':
    main()

    print(f'Работу закончил')
