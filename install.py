import platform
import requests
import zipfile
import os

if __name__ == "__main__": 
  driver_folder = 'driver'
  if not os.path.exists(driver_folder):
    system = platform.system()
    if system == 'Darwin':
      link = 'https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_mac64.zip'
    elif system == 'Linux':
      link = 'https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_linux64.zip'
    elif system == 'Windows':
      link = 'https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_win32.zip'
    else:
      print("This system is not supported(can do from source): '{0}'".format(system))
      exit(1)
    
    filename = 'driver.zip'
    r = requests.get(link)
    open(filename, 'wb').write(r.content)
    
    with zipfile.ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall(driver_folder)
    os.remove(filename)

  