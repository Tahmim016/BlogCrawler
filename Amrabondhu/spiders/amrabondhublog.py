import scrapy
from datetime import datetime

class ScrapePost(scrapy.Spider):
    name = 'amrabondhu'

    start_urls = [
        'https://www.amrabondhu.com/'
    ]

    custom_settings = {
        'DOWNLOAD_DELAY': 1
    }

    num = 0

    def parse(self, response):
        page = response.url.split('/')
        file = 'Amrabondhu.html'
        with open(file, 'wb') as f:
            f.write(response.body)

        #post_url = response.css('.art-Post-inner')
        for url in response.css('.art-Post-inner'):
            get_link = url.css('.art-PostHeader a::attr(href)').get()
            #print(post_link)

            if get_link is not None:
                read_more = response.urljoin(get_link)
                #print(read_more)
            else:
                read_more = 'https://www.amrabondhu.com/'
                #print(read_more)

            yield scrapy.Request(read_more,callback=self.parse_content ,meta = {
                    'url': read_more
            })

        next_page = response.css('li.pager-next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page)

    def parse_content(self, response):
        page = response.url.split('/')[-2]
        filename = page + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)

        if ScrapePost.num <= 50000:
            ScrapePost.num += 1
        title = response.css('.art-PostHeader ::text').get()
        author = response.css('.art-PostHeaderIcons ::text')[1].get()
        text = response.css('.art-article p::text').getall()
        date = response.css('.art-PostHeaderIcons ::text')[2].get()
        date_time = datetime.now()
        access_time = date_time.strftime("%d/%m/%Y %I:%M:%S")


        yield{
            'ID': ScrapePost.num,
            'Title': title,
            'Author': author,
            'Text': text,
            'URL': response.meta['url'],
            'Published_date': date,
            'Accessed_time': access_time
        }