import scrapy


class PostsSpider(scrapy.Spider):
    name = 'posts'

    start_urls = [
        'https://forum.singaporeexpats.com/viewforum.php?f=93',
    ]

    def parse(self, response):
        for topic_list in response.xpath('//ul[has-class("topiclist topics")]'):
            for topic in topic_list.xpath('li/dl'):
                yield {
                    'topic': topic.xpath('dt/div/a/text()').get(),
                    'replies': topic.xpath('dd[1]/text()').get(),
                    'views': topic.xpath('dd[2]/text()').get(),
                }
                # yield response.follow(topic.xpath('div/a/@href').get(), \
                #     self.parse)

        for post in response.xpath('//div[has-class("page-body")]/div[4]/div[has-class("inner")]'):
            yield {
                'title': post.xpath('div[has-class("postbody")]/div/h3/a/text()').get(),
                'author': post.xpath('//*[has-class("author")]/span/strong/a/text()').get(),
                'content': post.xpath('div[has-class("postbody")]/div/div[has-class("content")]/text()').get(),
            }

        next_page = response.xpath('//li[has-class("arrow next")]/a/@href').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)