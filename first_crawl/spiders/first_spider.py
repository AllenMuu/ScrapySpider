import scrapy


class firstSpider(scrapy.Spider):
    name = "first_spider"  # 爬虫名字

    start_urls = [
        'http://lab.scrapyd.cn' # 爬虫地址
    ]

    def parse(self, response):
        famous = response.css('div.quote')  # 提取所有名言 放入famous

        for f in famous:
            content = f.css('.text::text').extract_first()  # 提取第一条名言内容
            author = f.css('.author::text').extract_first()  # 提取作者
            tags = f.css('.tags.tag::text').extract()  # tags 有好多所以不是提取第一个
            tags = ','.join(tags)  # 数组转换成字符串

            # 文件操作
            fileName = '%s-语录.txt' % author  # 文件名
            with open(fileName, "a+") as file:
                file.write(content)
                file.write('\n')  # 换行
                file.write('标签:' + tags)
                file.write('\n------------------------------------\n')

        next_page = response.css('li.next a::attr(href)').extract_first()  # 爬取下一页

        if next_page is not None:
            next_page = response.urljoin(next_page)  # 相对路径拼成绝对路径

            yield scrapy.Request(next_page, callback=self.parse)
