import argparse
import asyncio
import aiohttp
import aiofiles
from time import time
from multiprocessing import Pool, cpu_count
from threading import Thread

def download_image(url):
    async def download(url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    f = await aiofiles.open(url.split('/')[-1], mode='wb')
                    await f.write(await response.read())
                    await f.close()
    start_time = time()
    asyncio.run(download(url))
    print(f"Downloaded {url} in {time() - start_time:.2f} seconds")

def download_images_sequential(urls):
    for url in urls:
        download_image(url)

def download_images_threading(urls):
    threads = [Thread(target=download_image, args=(url,)) for url in urls]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

def download_images_multiprocessing(urls):
    with Pool(cpu_count()) as p:
        p.map(download_image, urls)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download images from URLs.')
    parser.add_argument('urls', metavar='URL', type=str, nargs='+',
                        help='a URL to download an image from')
    args = parser.parse_args()
    
    start_time = time()
    download_images_sequential(args.urls)
    print(f"\nSequential execution time: {time() - start_time:.2f} seconds")
    
    start_time = time()
    download_images_threading(args.urls)
    print(f"\nThreading execution time: {time() - start_time:.2f} seconds")
    
    start_time = time()
    download_images_multiprocessing(args.urls)
    print(f"\nMultiprocessing execution time: {time() - start_time:.2f} seconds")
