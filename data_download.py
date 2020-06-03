import os, setting, lhafile
import urllib.request
from datetime import datetime
from time import strftime

#url = 'http://www.edatalab.sakura.ne.jp/data2020/D200527.LZH'

def open_lha(target_file_path, target_date):
    # Create Lhafile instance from filename
    f = lhafile.Lhafile(target_file_path)

    # Print each file informaion in archive file.
    file_name = ''
    for info in f.infolist():
        # print(info.filename)
        file_name = info.filename

    save_file = os.path.join(setting.get_download_stock_file_dir(), target_date + '.csv')
    open(save_file, "wb").write(f.read(file_name))
    f = None
    try:
        os.remove(target_file_path)
    except:
        print('---ERROR---Cannot delete the target LHA file:' + target_file_path)

def download_target_file(target_date):
    print('target_date:' + target_date)

    download_web_site_url = 'http://www.edatalab.sakura.ne.jp/'
    download_web_site_url = download_web_site_url + "data" + target_date[0:4] + "/D" + target_date[2:] + ".LZH"
    print('download_web_site_url:' + download_web_site_url)

    download_file_name = os.path.join(setting.get_download_stock_file_dir(), target_date + '.LZH')
    try:
        urllib.request.urlretrieve(download_web_site_url, "{0}".format(download_file_name))
        print('Downloaded Target Data in the following URL:' + download_web_site_url)
    except :
        print('---ERROR---Not Found Target Data in the following URL:' + download_web_site_url)
        return

    open_lha(download_file_name, target_date)

if __name__ == '__main__':

    start_time = datetime.now()

    today = datetime.now()

    weekno = today.today().weekday()
    if weekno < 5:
        print
        "Weekday"
    else:
        print
        "Weekend"

    print('Download Stock Data Start ' + today.strftime("%Y-%m-%d %H:%M:%S"))
   