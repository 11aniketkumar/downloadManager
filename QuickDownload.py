import requests
from pathlib import Path
from tqdm import tqdm


print('=======================Python Downloader=====================')

url = input('Please enter the url of the download: ')
q = input('Do you want to download the file from beginning(y/n): ')
if q=='y' or q=='Y':
  filename = 'data.bin'
  print('By default this program will download all data in a file data.bin, please change the extension according to the file later on.')
  f = open(filename, 'w+')
  f.close()
elif q=='n' or q=='N':
  print('Please keep this program and the incomplete_downloaded file in the same directory.')
  filename  = input('Please enter the complete name of the incomplete_download file along with its extension: ')
else:
  p = input('invalid input, Program terminating. Press any key to exit.')
print('This program uses a chunk size of 25mb while writing on a SSD so as to reduce disk writes, this method prolongs the disk life also by saving battery life, enter \'y\' below to continue with this setting. But HDD are not afected by disk writes, in case of HDD this program uses a chunk size of 100KB. So if you are using a HDD please enter \'n\'.')
n = input('Are you downloading this file on SSD:')
if n=='y' or n=='Y':
  write_chunk_size = 26214400
elif n=='n' or n=='N':
  write_chunk_size = 1024000
else:
  p = input('invalid input, Program terminating. Press any key to exit.')
  exit()



print('Note: While downloading file at once, this program does not show any download progress bar.')
n = input('Do you want to download complete file at once(y/n): ')

last_byte= Path(filename).stat().st_size

if n=='y' or n=='Y':
  resume_header = ({'Range': 'bytes={}-'.format(last_byte)})
  r = requests.get(url, stream=True, headers=resume_header)
  with open(filename,'ab') as f:
    for chunk in r.iter_content(chunk_size=write_chunk_size):
      f.write(chunk)
      print('+25mb downloaded')

elif n=='n' or n=='N':
  size = int(input('How many GB do you want to download right now(GB): '))
  size_bytes = int(1073741824 * size)
  p = last_byte+size_bytes
  resume_header = ({'Range': 'bytes={}-{}'.format(last_byte, p)})
  r = requests.get(url, stream=True, headers=resume_header)
  with open(filename,'ab') as f:
      for chunk in tqdm(iterable = r.iter_content(chunk_size=write_chunk_size), total = size_bytes/write_chunk_size, unit = 'MB', desc='Downloading: '):
        f.write(chunk)

else:
  p = input('invalid input, Program terminating. Press any key to exit.')
  exit()

n = input('File downloaded successfully, please change the extension of the file as per your data. Press enter to exit...')
#This is dangerous especially for ssd pc's, opening and writing 1kb again and again is worse, all browsers are literally destroying the SSD's, it's better to install 25mb and write everything at once.
# 26214400     25mb
# 104857600    100mb
# 1073741824   1 GB
