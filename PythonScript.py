import requests
import os
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse


def is_valid (url):
    # Check if url is valid
    parsed = urlparse(url)
    # netloc is domain name, scheme is protocol
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_images(url):
    #Return all images URL's on a single url
    soup = bs(requests.get(url).content, 'html.parser')
    urls = []
    for img in soup.find_all('img'):
        print("Extracting images...")
        img_url = img.attrs.get('src')
        if not img_url:
            #go to next image URL
            continue
        img_url= urljoin(url, img_url) #make URL absolute
        print(img_url)
        if is_valid(img_url):
            urls.append(img_url)
            print(urls)
        return urls

def download(url,pathname):
    #Download a file given a URL and puts it in the folder pathname
    if not os.path.isdir(pathname): #if path doesn't exist, make path dir
        os.makedirs(pathname)
    # download the body of response by chunk
    response = requests.get(url, stream = True)
    # get the file name
    filename = os.path.join(pathname, url.split('/')[-1])
    progress = response.iter_content(1024)
    with open(filename,'wb') as f:
        for data in progress:
            f.write(data)
            print("Image added to folder")

def main(url, pathname):
    #get all images
    # calling get_all_images function from above
    imgs = get_all_images(url)
    for img in imgs:
        # for each image iterated, download it
        # calling download function from above
        download(img, pathname)

main("insert_url_here","select_or_create_folder")
