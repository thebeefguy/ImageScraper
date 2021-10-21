from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import time

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

wd = webdriver.Chrome(options=chrome_options)

def fetch_image_urls(query:str, max_links_to_fetch:int, wd:webdriver = wd, sleep_between_interactions:int = 1):

  def scroll_to_end(wd):
    wd.execute_script("window.scrollTo(0, document.body.scollHeight);")
    time.sleep(sleep_between_interactions)

  search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"

  wd.get(search_url.format(q=query))

  image_urls = set()
  image_count = 0
  results_start = 0

  while image_count < max_links_to_fetch:

    scroll_to_end(wd)

    thumbnail_results = wd.find_elements_by_css_selector('img.Q4LuWd')
    number_results = len(thumbnail_results)

    print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")

    for img in thumbnail_results[results_start:number_results]:

      try:
        img.click()
        time.sleep(sleep_between_interactions)
      except Exception:
        continue

      actual_images = wd.find_elements_by_css_selector('img.n3VNCb')
      for actual_image in actual_images:
        if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
          image_urls.add(actual_image.get_attribute('src'))

      image_count = len(image_urls)

      if len(image_urls) >= max_links_to_fetch:
        print(f"Found: {len(image_urls)} image links, done!")
        break

    else:
      print("Found:", len(image_urls), "image links, looking for more ...")
      time.sleep(30)
      return
      load_more_button = wd.find_element_by_css_selector(".mye4qd")
      if load_more_button:
        wd.execute_script("document.querySelector('.mye4qd').click();")

    results_start = len(thumbnail_results)

  return image_urls

query = input("Search term: ")
max_links_to_fetch = int(input("Number of images to get: "))

res = fetch_image_urls(query, max_links_to_fetch, sleep_between_interactions = 0.5)

for elem in res:
  print(elem)