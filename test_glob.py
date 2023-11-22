import glob

csv_file_list = glob.glob('temp/' + '*.csv')
print(f'[12/13] csv_file_list : {csv_file_list}')   
# [os.remove(f) for f in glob.glob(temp_dir + '/' + '*.csv')]