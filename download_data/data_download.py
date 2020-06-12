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

    open(setting.get_target_download_csv_file_path(target_date), "wb").write(f.read(file_name))
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

def main(target_date):

    print('Download Stock Data Start ' + strftime("%Y-%m-%d %H:%M:%S"))
    target_date_time = datetime.strptime(target_date, '%Y%m%d')
    weekno = target_date_time.weekday()
    # print('weekno:'+ str(weekno))
    if weekno < 5:
        download_target_file(target_date)
    else:
        print('Skip download date due to today is not weekday. weekno=' + str(weekno))

    # print('Download Stock Data End ' + strftime("%Y-%m-%d %H:%M:%S"))
    # insert_date = target_date_time.strftime("%Y-%m-%d")

if __name__ == '__main__':
    today = datetime.now()
    main('20200603')
    # download_main(today.strftime("%Y%m%d"))