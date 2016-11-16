from calendar import monthrange
from get_records.items import RecordItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class RecordsSpider(CrawlSpider):
    name = "records"
    allowed_domains = ["www.assembly.wales"]

    # URL string with format specifiers
    url_string = ("http://www.assembly.wales/en/bus-home/pages/plenary.aspx?" +
                  "assembly=4&category=Record%20of%20Proceedings&startDt=01/{month}/{year}" +
                  "&endDt={end_day}/{month}/{year}")

    # create a list of start urls to crawl formatting the string above
    # so that correct month end dates are used i.e. 28 for February
    # on non-leap years
    start_urls = []
    for year in range(2013, 2017):
        for month in range(1, 13):
            start_urls.append(url_string.format(month=month, year=year,
                                                end_day=monthrange(year, month)[1]))

    rules = (
        Rule(
            LinkExtractor(
                allow=(),
                restrict_xpaths=("//a[contains(text(),'English')]",)
            ),
            callback="parse_records",
            follow=True
        ),
    )

    def parse_records(self, response):
        # XPaths
        date_xpath = '//*[@id="ropDate"]/span/text()'
        contribution_xpath = '//div[@class="transcriptContribution"]'
        time_xpath = 'div[@class="timeContainer"]/span/text()'
        contribution_container_xpath = 'div[@class="contributionContainer"]'
        member_name_xpath = 'div[@class="memberNameContainer"]/span[@class="memberName"]/text()'
        contribution_text_xpath = 'div[@class="contribContainer"]/text()'
        contribution_question_xpath = 'div[@class="contribContainer"]/span[@class="contributeTypeO"]/text()'

        # Item that will hold the data
        item = RecordItem()
        # Date record being parsed took place on
        date = response.selector.xpath(date_xpath).extract()
        # 'date' in item should be a list of dicts
        item['date'] = date
        # List of all contributions made in the record being parsed
        contributions = response.xpath(contribution_xpath)

        # Log the date being parsed
        print('Parsing the plenary session held on {}'.format(date))

        item['contributions'] = []

        # Loop through the contributions, store each one as a dict in a list
        for contribution in contributions:
            # Time of the contribution
            contribution_time = contribution.xpath(
                time_xpath).extract_first(default=None)

            # Select the container element that holds other details
            contribution_container = contribution.xpath(
                contribution_container_xpath
            )

            # Name of the AM contributing
            contributor_name = contribution_container.xpath(
                member_name_xpath).extract_first(default=None)

            # What was said
            contribution_text = contribution_container.xpath(
                contribution_text_xpath).extract_first(default=None)

            # Text of a written question
            contribution_question = contribution_container.xpath(
                contribution_question_xpath).extract_first(default=None)

            # dict to hold our data
            contribution_dict = {}

            # All verbal submissionshave a time stamp
            # other elements (such as agenda headings and votes) don't
            # so this if statement stops empty values entering
            # the data
            if contribution_time is not None:

                contribution_dict['contribution_time'] = contribution_time
                contribution_dict['contributor_name'] = contributor_name

                # Contribution text and questions don't exist at the same
                # time, so the below just stops empty key: value pairs
                # entering the data
                if contribution_text is not None:
                    contribution_dict['contribution_text'] = contribution_text

                if contribution_question is not None:
                    contribution_dict['contribution_question'] = contribution_question

                item['contributions'].append(contribution_dict)
        return item
