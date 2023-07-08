from datetime import datetime

from browser.createbrowser import CreatBrowser
from save_result import SaveResult
from src.plu_parse import PluParser
from src.source_parse import SourceParse
from src._no_source_parse_plu import SourceParsePlu

from src.temp import *

from sql.bot_connector import BotDB

from src.temp_collect import temp_collect


def main():
    url_ = ['https://profiplitka.ru/plitka/altacera/']

    collec_count_page = 0

    browser_core = CreatBrowser()

    for url in temp_collect:
    # for url in url_:


        print(f'Парсер запущен. Получаю данные')

        # data_good = SourceParse(browser_core.driver, collec_count_page).start_pars(url)

        #
        #
        # print(f'Собрал {len(data_good)} коллекций на обработку')
        #
        # collection_data = PluParser(browser_core.driver, data_good, BotDB).start_pars()
        collection_data = coll_data

        print(f'Обработоал {len(collection_data)} коллекций')

        file_name = f'{datetime.now().strftime("%H_%M_%S")}'

        SaveResult(collection_data).save_file(file_name)


        print()


if __name__ == '__main__':
    main()

    print(f'Работу закончил')
