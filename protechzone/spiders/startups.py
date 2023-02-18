import re
import scrapy
from scrapy.selector import Selector
from scrapy_splash import SplashRequest
from scrapy.loader import ItemLoader
from ..items import ProtechzoneItem
from w3lib.http import basic_auth_header


class StartupsSpider(scrapy.Spider):
    name = 'startups'
    allowed_domains = ['proptechzone.com']

    script = '''
        function main(splash, args)
            splash:on_request(function(request)
                if request.url.find("css")then
                    request.abort()
                end
            end)
            splash.images_enabled = false
            splash.js_enabled = false
            assert(splash:go(args.url))
            assert(splash:wait(0.5))
            return splash:html()
        end
    '''
    count_perpage = 16
    page = 1

    def getting_url(self, page):
        print(page)
        url = f"https://proptechzone.com/startups/?sf_data=results&sf_paged={page}"
        return url

    def start_requests(self):
        yield scrapy.Request(
            url=self.getting_url(page=self.page),
            headers={
                'cookie': '_wpfuuid=54a11329-3c6c-4304-b146-e66be747b717; ln_or=eyIyNDUwMDE4IjoiZCJ9; _gid=GA1.2.1907190756.1676670361; _ga=GA1.2.245010864.1673620014; _ga_W5JG9JN9ET=GS1.1.1676670359.2.1.1676671660.0.0.0',
            },
            callback=self.parse
        )

    def parse(self, response):
        auth = basic_auth_header('user', 'userpass')

        sel = Selector(text=response.body)

        startup_list = sel.xpath("//li[@class='prop-arch-item']")

        total_count_string = sel.xpath(
            "//span[@class='results-count-wrap']/text()").get()
        total_count = int(re.search(r'\d+', total_count_string).group())

        for startup in startup_list:
            new_url = startup.xpath(
                ".//a[@class='home-arch-item-btn frameless-btn']/@href").get()
            yield SplashRequest(
                url=new_url,
                endpoint='execute',
                callback=self.parse_summary,
                args={
                    'lua_source': self.script,
                    'wait': 0.5,
                    'viewport': '1024x2480',
                    'timeout': 90,
                    'images': 0
                },
                splash_headers={'Authorization': auth},
            )

        if self.count_perpage <= total_count:
            self.page += 1
            self.count_perpage += 16

            yield scrapy.Request(
                url=self.getting_url(page=self.page),
                headers={
                    'cookie': '_wpfuuid=54a11329-3c6c-4304-b146-e66be747b717; ln_or=eyIyNDUwMDE4IjoiZCJ9; _gid=GA1.2.1907190756.1676670361; _ga=GA1.2.245010864.1673620014; _ga_W5JG9JN9ET=GS1.1.1676670359.2.1.1676671660.0.0.0',
                },
                callback=self.parse
            )

    def parse_summary(self, response):
        sel = Selector(text=response.body)
        loader = ItemLoader(item=ProtechzoneItem(),
                            selector=sel, response=response)
        loader.add_xpath('name_startup', "//h1[@class='entry-title']/text()")
        loader.add_xpath('website_url', "//a[@class='startup-url']/@href")
        loader.add_xpath(
            'verts_link', "//li[@class='archived-sub-vertical-item']/a/text()")
        loader.add_xpath(
            'description', "//span[@class='top-excerpt-wrap']/p/text()")
        loader.add_xpath(
            'year_founded', "//div[@class='startup-top-info-stats-cont']/div[1]/div[@class='stat-cont']/span[2]/text()")
        loader.add_xpath(
            'total_raised', "//div[@class='startup-top-info-stats-cont']/div[2]/div[@class='stat-cont']/span[2]/text()")
        loader.add_xpath(
            'funding_stage', "//div[@class='startup-top-info-stats-cont']/div[3]/div[@class='stat-cont']/span[2]/text()")
        loader.add_xpath(
            'employees', "//div[@class='startup-top-info-stats-cont']/div[4]/div[@class='stat-cont']/span[2]/text()")
        loader.add_xpath(
            'country', "//div[@class='startup-side-info-icons-mobile']/div[1]/div[@class='stat-cont']/span[@class='startup-page-stat-data']/text()")
        loader.add_xpath(
            'operation_area', "//div[@class='startup-side-info-icons-mobile']/div[2]/div[@class='stat-cont']/span[2]/text()")
        loader.add_xpath(
            'hq_address', "//div[@class='startup-side-info-icons-mobile']/div[3]/div[@class='stat-cont']/span[2]/text()")
        loader.add_xpath(
            'other_office', "//div[@class='startup-side-info-icons-mobile']/div[4]/div[@class='stat-cont']/span[2]/text()")
        loader.add_xpath(
            'linkedin_company', "//section/div[@class='sidebar-social-wrapper']/a/@href")
        yield loader.load_item()
