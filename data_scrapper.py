# scraping images from
# https://festalab.com.br/modelo-de-convite/convite-de-aniversario-infantil

import requests, bs4, os, threading, queue, logging, argparse
from datetime import datetime
from PIL import Image
from io import BytesIO

# queue consumer
def worker(image_links_queue):
    while True and not image_links_queue.empty():
        link, title = image_links_queue.get()
        download_image(link, title)
        image_links_queue.task_done()


# defining func to save img
def download_image(image_url, file_dir):
    response = requests.get(image_url)

    if response.status_code == 200:
        resized_image = formatting_images(BytesIO(response.content))
        directory = os.path.dirname(file_dir)
        
        if not os.path.exists(directory):
            os.makedirs(directory)

        resized_image.save(file_dir + '.jpg')
        
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logging.info(f"{now_time}::Image downloaded successfully.\n {image_url}")
    else:
        logging.error(f"{now_time}::Failed to download the image. Status code: {response.status_code}")


def formatting_images(content, size=(512, 512)):
    if not isinstance(content, BytesIO):
        return
        
    img = Image.open(content)
    img = img.resize(size)
    return img

def print_completion(images_total, image_links_queue):
    percentage = round(100 - (image_links_queue.qsize() / images_total * 100), 2)
    print(f"\n ***COMPLETION***\n   {percentage}%")
    
    if percentage < 100:
        threading.Timer(5, print_completion, args=(images_total, image_links_queue)).start()
        return
    
    logging.info('Script data_scrapper finished')
    print('\nScript data_scrapper finished')


# logging setup
default_url = 'https://festalab.com.br/modelo-de-convite/convite-de-aniversario-infantil'
default_tag = 'img'
default_nthread = 10

arg_parser = argparse.ArgumentParser(prog='DataScrapper',
                    description='Scrape data from a website')

arg_parser.add_argument("-u", "--url", default=default_url, type=str, help="url to scrape")
arg_parser.add_argument("-t", "--tag", default=default_tag, type=str, help="tag to scrape")
arg_parser.add_argument("-n", "--nthread", default=default_nthread, type=int, help="number of threads")

parsed_args = arg_parser.parse_args()
url = parsed_args.url
tag = parsed_args.tag
thread_count = parsed_args.nthread

if tag != 'img':
    print('Only img tag is supported')
    exit()

logging.basicConfig(filename='data_scrapper.log', encoding='utf-8', level=logging.INFO)
logging.info('Starting the script data_scrapper')
print('Starting the script data_scrapper')

# get data
data = requests.get(url).text
image_links_queue = queue.Queue()

# scrap
soup = bs4.BeautifulSoup(data, 'html.parser')
for item in soup.find_all(tag):
  if item.has_attr('data-src') and item.has_attr('title'):
      title = item['title']
      dash_index = title.index('-')
      if dash_index > 0:
          title = title[dash_index + 1:].strip()
      image_links_queue.put((item['data-src'], f'images/{title}'))
   
images_total = image_links_queue.qsize()
print_completion(images_total, image_links_queue)
threads = []

for t in range(0, thread_count):
    thread = threading.Thread(target=worker, args=(image_links_queue,), daemon=True)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()
    
