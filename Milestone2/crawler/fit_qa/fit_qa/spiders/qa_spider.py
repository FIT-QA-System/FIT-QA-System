import scrapy
import re


class QA_Spider(scrapy.Spider):
    name = "qas"
    start_urls = [
        'https://services.fit.edu/it_faq/sitemap/A/en.html',
        'https://services.fit.edu/it_faq/sitemap/C/en.html',
        'https://services.fit.edu/it_faq/sitemap/D/en.html',
        'https://services.fit.edu/it_faq/sitemap/E/en.html',
        'https://services.fit.edu/it_faq/sitemap/F/en.html',
        'https://services.fit.edu/it_faq/sitemap/H/en.html',
        'https://services.fit.edu/it_faq/sitemap/I/en.html',
        'https://services.fit.edu/it_faq/sitemap/L/en.html',
        'https://services.fit.edu/it_faq/sitemap/M/en.html',
        'https://services.fit.edu/it_faq/sitemap/O/en.html',
        'https://services.fit.edu/it_faq/sitemap/P/en.html',
        'https://services.fit.edu/it_faq/sitemap/R/en.html',
        'https://services.fit.edu/it_faq/sitemap/S/en.html',
        'https://services.fit.edu/it_faq/sitemap/U/en.html',
        'https://services.fit.edu/it_faq/sitemap/W/en.html',
    ]

    url_prefix = "https://services.fit.edu"

    def parse(self, response):
        urls = response.css('div#mainContent>section>ul li a::attr(href)').extract()
        print(urls)
        for url in urls:
             yield scrapy.Request(url=self.url_prefix + url, callback=self.parse_question_page)

    def parse_question_page(self, response):
        yield{
            "url": response.url,
            "question": response.css('header h2::text').extract_first(),
            "answer_html": response.css('article.answer').extract(),
            "ID": re.search(r'\d+', response.css('#solution_id a::text').extract_first()).group(),
            "category": response.css('.breadcrumb span::text').extract_first(),

        }



# class QA_Spider(scrapy.Spider):
#     name = "qas"
#
#     def start_requests(self):
#         self.start_urls = [
#             'https://services.fit.edu/it_faq/sitemap/A/en.html',
#             'https://services.fit.edu/it_faq/sitemap/C/en.html',
#             'https://services.fit.edu/it_faq/sitemap/D/en.html',
#             'https://services.fit.edu/it_faq/sitemap/E/en.html',
#             'https://services.fit.edu/it_faq/sitemap/F/en.html',
#             'https://services.fit.edu/it_faq/sitemap/H/en.html',
#             'https://services.fit.edu/it_faq/sitemap/I/en.html',
#             'https://services.fit.edu/it_faq/sitemap/L/en.html',
#             'https://services.fit.edu/it_faq/sitemap/M/en.html',
#             'https://services.fit.edu/it_faq/sitemap/O/en.html',
#             'https://services.fit.edu/it_faq/sitemap/P/en.html',
#             'https://services.fit.edu/it_faq/sitemap/R/en.html',
#             'https://services.fit.edu/it_faq/sitemap/S/en.html',
#             'https://services.fit.edu/it_faq/sitemap/U/en.html',
#             'https://services.fit.edu/it_faq/sitemap/W/en.html',
#
#         ]
#         for url in self.start_urls:
#             yield scrapy.Request(url=url, callback=self.parse_letter_page)
#
#     def parse_letter_page(self, response):
#         urls = response.css('div#mainContent ul li a::attr(href)').extract()
#
#         for url in urls:
#             yield scrapy.Request(url=url, callback=self.parse_question_page)
#
#     def parse_question_page(self, response):
#         yield {
#             'question': response.css('header h2').extract_first(),
#             'answer': "\n".join(response.css('article.answer').extract()),
#             'answer_html': response.css('article.answer').extract(),
#             'category': response.css('ul.breadcrum span').extract(),
#             'url': response.url,
#             'id': response.css('#solution_id a').extract_first(),
#
#         }
#
