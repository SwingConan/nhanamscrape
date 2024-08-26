import scrapy
from nhanamscrape.items import BookItem

class NhanamspiderSpider(scrapy.Spider):
    name = "nhanamspider"
    allowed_domains = ["nhasachphuongnam.com"]
    start_urls = ["https://nhasachphuongnam.com/sach-tieng-viet.html"]

    def parse(self, response):
        books = response.css('div.ut2-gl__item')

        # Lặp qua các sách trên trang
        for book in books:
            # Lấy URL tương đối của sách
            relative_url = book.css('.ut2-gl__name a::attr(href)').get()
            if relative_url:
                book_url = response.urljoin(relative_url)
                yield response.follow(book_url, callback=self.parse_book_page)

        # Lấy URL trang tiếp theo
        next_page = response.css('a.ty-pagination__item.ty-pagination__btn.ty-pagination__next.cm-history.cm-ajax::attr(href)').get()

        # Kiểm tra nếu có trang tiếp theo và trang đó không vượt quá trang 50
        if next_page is not None:
            next_page_url = response.urljoin(next_page)
            if 'sach-tieng-viet-page-51.html' not in next_page_url:  # Kiểm tra nếu URL không phải trang 50
                yield response.follow(next_page_url, callback=self.parse)

    def parse_book_page(self, response):
        book_item = BookItem()

        book_item['name'] = response.css('div.ut2-pb__title h1 bdi::text').get()
        book_item['price'] = response.css('span.ty-price-num::text').get()
        book_item['category'] = response.xpath('//div[@id="breadcrumbs_11"]/div/a[4]/bdi/text()').get()
        book_item['subcategory'] = response.xpath('//div[@id="breadcrumbs_11"]/div/a[5]/bdi/text()').get()
        book_item['size'] = response.xpath('//*[@id="content_features"]/div/div[2]/div[2]/text()').get()
        book_item['pages'] = response.xpath('//*[@id="content_features"]/div/div[3]/div[2]/text()').get()
        book_item['publishing_affiliate'] = response.xpath('//*[@id="tygh_main_container"]/div[3]/div/div/div/div/div[1]/div[2]/div[3]/div[2]/div[2]/div/a/span/span[2]/em/text()').get()
        book_item['barcode'] = response.css('div.ty-control-group span.ty-control-group__item::text').get()
        book_item['seller'] = response.xpath('//*[@id="tygh_main_container"]/div[3]/div/div/div/div/div[1]/div[2]/div[3]/div[2]/div[1]/div[2]/div[1]/a/text()').get()
        book_item['url'] = response.url
        book_item['description'] = response.xpath('//*[@id="content_description"]/div/p[1]/text()').get()

        yield book_item
