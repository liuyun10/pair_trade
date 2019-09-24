import shutil,os

def clean_target_dir(data_dir, report_dir):

    result_dir = os.path.join(data_dir, report_dir)
    if os.path.exists(result_dir):
        print('Cleaning the target dir:'+report_dir)
        shutil.rmtree(result_dir)

    os.makedirs(result_dir)