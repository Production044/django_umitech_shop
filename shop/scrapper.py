import sys
from concurrent.futures import ThreadPoolExecutor
import requests
from queue import Queue
from bs4 import BeautifulSoup
from django.utils.text import slugify
from pprint import pprint

from shop.models import Category, Color, Image, Product, Size

TIME_OUT = 10


def upload_image_to_local_media(
        img_url: str,
        image_name: str,
        product: Product
):
    with requests.Session() as session:
        img_response = session.get(img_url, timeout=TIME_OUT)

    with open(f'media/images/{image_name}', 'wb') as file:
        file.write(img_response.content)

    Image.objects.create(
        product=product,
        image=f'images/{image_name}',
        base_url=img_url,
    )


def process(html_string: str, url: str):
    umisoup = BeautifulSoup(html_string, "html.parser")
    try:
        title = umisoup.select(".cs-title__product")
        # title = title[0].text.strip()
        price = umisoup.select(".b-product-cost__price")
        # price = price[0].text.replace('\xa0', '').replace('грн', '')
        # old_price = umisoup.select(".b-product-cost__old-price")
        # old_price = old_price[0].text.replace('\xa0', '').replace('грн', '')

        availability_in = umisoup.select(".b-product-data__item")
        # availability_in = availability_in[0].text.strip()

        description = umisoup.select(".b-user-content p")
        # description = '\n'.join([f'<li>{item.text}</li>' for item in description])
        # breakpoint()

        # color = umisoup.select(".b-product-info__cell")
        # find_index = [i.text for i in color]
        # find_color = find_index.index('Колір')
        # color = color[find_color + 1].text
        # color, _ = Color.objects.get_or_create(name=color)

        # brand = umisoup.select(".b-product-info__cell")
        # find_brand_index = [i.text for i in brand]
        # find_brand = find_brand_index('Виробник')
        # brand = brand[find_brand + 1].text

        product, _ = Product.objects.get_or_create(
            slug=slugify(title := title[0].text.strip()),
            defaults={
                'base_url': url,
                'title': title,
                'price': price[0].text.replace('\xa0', '').replace('грн', ''),
                # 'old_price': old_price[0].text.replace('\xa0', '').replace('грн', ''),
                'availability_in': availability_in[0].text.strip(),
                'description': '\n'.join([f'<p>{item.text}</p>' for item in description]),
                # 'color': color,
                # 'brand': brand
            }
        )

        # sizes = umisoup.select("")
        # sizes = {size.text.strip() for size in sizes}
        # for size in sizes:
        #     s, _ = Size.objects.get_or_create(name=size)
        #     product.sizes.add(s)    # використати до категорії які мають розміри

        categories = 'nozhi' #хардкодкатегорій
        cat, _ = Category.objects.get_or_create(name=categories, slug=categories)
        product.categories.add(cat)

        images = umisoup.select(".cs-product__img-row img")
        images = [img['src'] for img in images]
        images = [image.replace('w159_h159_', '') for image in images]

        image_names = [name.split('/')[-1] for name in images]
        print('Uploading images')
        for image, name in zip(images, image_names):
            print(name)
            upload_image_to_local_media(
                image,
                name.lower(),
                product
            )

        print("DONE!!!")

    except Exception as error:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print('Parsing Error', error, exc_tb.tb_lineno)


def worker(queue: Queue):
    while True:
        url = queue.get()
        print("[WORKING ON]", url)
        try:
            with requests.Session() as session:
                response = session.get(
                    url,
                    allow_redirects=True,
                    timeout=TIME_OUT
                )
                print(response.status_code)
                if response.status_code == 404:
                    print('Page not found', url)
                    break
                assert response.status_code in (200, 301, 302), 'Bad response'

            process(response.text, url)

        except (
            requests.Timeout,
            requests.TooManyRedirects,
            requests.ConnectionError,
            requests.RequestException,
            requests.ConnectTimeout,
            AssertionError
        ) as error:
            print('An error happen', error)
            queue.put(url)

        if queue.qsize() == 0:
            break


def main():
    category_urls = ['https://umitech.com.ua/ua/g111172754-nozhi']

    with requests.Session() as links_session:
        response = links_session.get(category_urls[0])

    umisoup = BeautifulSoup(response.content, "html.parser")
    links = umisoup.select(".cs-product-gallery__title a")
    links = [link.get('href') for link in links]

    queue = Queue()

    for url in links: #[:]
        queue.put(f'https://umitech.com.ua{url}')

    worker_number = 1

    with ThreadPoolExecutor(max_workers=worker_number) as executor:
        for _ in range(worker_number):
            executor.submit(worker, queue)


if __name__ == '__main__':
    main()