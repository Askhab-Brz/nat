import scrapy


class NatwestSpider(scrapy.Spider):
    name = 'natwest'
    start_urls = ['https://jobs.natwestgroup.com/search/jobs/in?page=1#']

    def parse(self, response):
        # Get the last page number
        pagination = response.xpath("//div[@class='pagination']")
        last_page = int(pagination.xpath(".//a[last()-1]/text()").get())

        # Loop through each page of job listings
        for page in range(1, last_page + 1):
            page_url = f"https://jobs.natwestgroup.com/search/jobs/in?page={page}#"
            yield scrapy.Request(page_url, callback=self.parse_job_listings)

    def parse_job_listings(self, response):
        job_links = response.css('a.job__link')

        # Loop through each job listing link and extract job data
        for job_link in job_links:
            yield response.follow(job_link, callback=self.parse_job_details)

    def parse_job_details(self, response):
        location = response.xpath("//div[@aria-label='Location']/text()").get().strip()
        contract_type = response.xpath("//div[@aria-label='Contract type']/span/text()").get()
        date_posted = response.xpath("//div[@aria-label='Date posted']/span/span/text()").get()
        vacancy_description = response.xpath(
            "//section[@class='job-page__description body-copy']/ul[1]/li/text()").getall()
        role_description = response.xpath(
            "//section[@class='job-page__description body-copy']/ul[2]/li/text()").getall()
        candidate_requirements = response.xpath(
            "//section[@class='job-page__description body-copy']/ul[3]/li/text()").getall()

        salary = response.xpath("//*[contains(text(),'£')]/text()").get(default='NO_DATA')

        yield {
            'location_data': location,
            'contract_type_data': contract_type,
            'date_posted_data': date_posted,
            'vacancy_description_data': vacancy_description,
            'role_description_data': role_description,
            'candidate_requirements_data': candidate_requirements,
            'salary_data': salary
        }
