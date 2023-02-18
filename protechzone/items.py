# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose,Join

def clean_vert_link(vertlink):
    if vertlink:
        return vertlink.strip()
def check_availabe(item):
    if item:
        return item
    else:
        return "Not available right now"

class ProtechzoneItem(scrapy.Item):

    name_startup = scrapy.Field(
        output_processor=TakeFirst()
    )
    website_url = scrapy.Field(
        input_processor=MapCompose(check_availabe),
        output_processor=TakeFirst()
    )
    verts_link = scrapy.Field(
        input_processor=MapCompose(clean_vert_link),
    )
    description= scrapy.Field(
        output_processor=TakeFirst()
    )
    year_founded = scrapy.Field(
        output_processor=TakeFirst()
    )
    total_raised = scrapy.Field(
        input_processor=MapCompose(check_availabe),
        output_processor=TakeFirst()
    )
    funding_stage =scrapy.Field(
        output_processor=TakeFirst()
    )
    employees = scrapy.Field(
        output_processor=TakeFirst()
    )
    country = scrapy.Field(
        output_processor=TakeFirst()
    )
    operation_area = scrapy.Field(
        output_processor=TakeFirst()
    )
    hq_address = scrapy.Field(
        output_processor=TakeFirst()
    )
    other_office =scrapy.Field(
        output_processor=Join('')
    )
    linkedin_company = scrapy.Field()
