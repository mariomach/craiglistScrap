# -*- coding: utf-8 -*-
import scrapy


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    allowed_domains = ['seattle.craigslist.org/']
    start_urls = ['https://seattle.craigslist.org/search/acc']
    
    def parse(self, response):
        listings = len(response.xpath("//p[@class='result-info']/a[@class='result-title hdrlnk']/text()").getall())
        title = response.xpath("//p[@class='result-info']/a[@class='result-title hdrlnk']/text()").getall()
        date = response.xpath("//p[@class='result-info']/time/@datetime").getall()
        link = response.xpath("//p[@class='result-info']/a/@href").getall()

        # for each in range(listings):
        #     yield {
        #         "Title": title[each],
        #         "Date": date[each],
        #     }
            
        for each in range(listings):
            yield scrapy.Request(link[each], 
                                 callback=self.parse_listing, 
                                 meta={'date': date[each],
                                        'link': link[each],
                                        'title': title[each]}, dont_filter=True)

        next_url = response.xpath("//a[@class='button next']/@href").get()
        if next_url:
            base_url = 'https://seattle.craigslist.org'
            absolute_next_page_url = base_url + next_url
    
            yield scrapy.Request(absolute_next_page_url, callback=self.parse, dont_filter=True)

    def parse_listing(self, response):
        date = response.meta['date']
        link = response.meta['link']
        title = response.meta['title']
        compensation = response.xpath("//p[@class='attrgroup']/span/b/text()").get()
        employment_type = response.xpath("//p[@class='attrgroup']/span[2]/b/text()").get()

        yield {
            "Title": title,
            "Date": date,
            "Link": link,
            "Compensation": compensation,
            "Employment Type": employment_type,
            }
            
