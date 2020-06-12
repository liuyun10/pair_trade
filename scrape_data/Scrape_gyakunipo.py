from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from util import fileutil as file_util
import pandas as pd
import os ,setting

url = 'https://www.traders.co.jp/margin/backwardation/backwardation.asp'

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)

def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

def output(table):
    output_rows = []
    for table_row in table.findAll('tr'):
        columns = table_row.findAll('td')
        output_row = []
        for column in columns:
            _text = column.text.replace('\n', '').replace('\t', '').replace('\r', '').replace(' ', '')
            output_row.append(_text)

        output_rows.append(output_row)
    # print(output_rows)
    df = pd.DataFrame(output_rows)
    file_util.write_csv_without_index_header(df, os.path.join(setting.get_master_dir(), 'gyakunipo_data.csv'))

def main():
    # print('Gyakunipo data start!')
    html= BeautifulSoup(simple_get(url), 'html.parser')
    table = html.find('table', attrs={'width':'600px', 'bordercolor':'#AAB5BB'})
    output(table)
    print('Gyakunipo data suceesfully !')

if __name__ == '__main__':
    main()
