# Name: Zuha Umar
# Roll No: 20I-0603

#Importing libraries
import scrapy
import csv
import re
import os

class I200603urduStoriesSpiderSpider(scrapy.Spider):
    name = "I200603urdu_stories_spider"
    allowed_domains=["www.urduzone.net"]
    start_urls=["https://www.urduzone.net"]
    extra_links=[
                    "https://www.urduzone.net/aik-thi-malka/",
                    "ttps://www.urduzone.net/sitaron-kay-angan-mein/",
                    "https://www.urduzone.net/qurbani-aik-ahsas/",
                    "https://www.urduzone.net/dil-kay-arman/",
                    "https://www.urduzone.net/aas-ka-panchi/",
                    "https://www.urduzone.net/lafz/",
                    "https://www.urduzone.net/sitaron-ko-chamakne/",
                    "https://www.urduzone.net/gumrah/",
                    "https://www.urduzone.net/aapa/",
                    "https://www.urduzone.net/raja-aur-rani/",
                    "https://www.urduzone.net/mughalta/",
                    "https://www.urduzone.net/phir-youn-huwa/",
                    "https://www.urduzone.net/azmaish/",
                    "https://www.urduzone.net/kambukht-ramju/",
                    "https://www.urduzone.net/phanda/",
                    "https://www.urduzone.net/sacha-fankar-part1/",
                    "https://www.urduzone.net/sacha-fankar-part2/",
                    "https://www.urduzone.net/dhoka/",
                    "https://www.urduzone.net/akhri-goli/",
                    "https://www.urduzone.net/mazhabi-chola/",
                    "https://www.urduzone.net/pachtawe-ki-aag/",
                    "https://www.urduzone.net/kanton-ki-fasal/",
                    "https://www.urduzone.net/khazan-kay-baad/",
                    "https://www.urduzone.net/meekay-aur-susraal-ki-mahro/",
                    "https://www.urduzone.net/saas-ka-keisa-insaf/",
                    "https://www.urduzone.net/ahsas/"
                    "https://www.urduzone.net/makan-ghar-tak/"
               ]
    
    def notSkipPage(self,response):
        #Extracting title of the page
        page_title=response.xpath('//title/text()').get()
        #Define a regular expression pattern to match the following words
        title_pattern=r'(Archives|Khawateen Digest|3 Aurtain 3 Kahaniyan|Home|Urdu Short Stories|Three Aurtein Three Kahaniyan|Posts|Three Women Three Stories)'
        #Return false if the title matches the pattern
        if re.search(title_pattern,page_title):
            return False  
        else:
            return True

    def parse(self,response):
        #Navigate to the Urdu Short Stories page
        yield scrapy.Request(url="https://www.urduzone.net/category/urdu-short-stories/",callback=self.parse_stories)
        #Navigate to the 3 aurtain 3 kahaniyan page
        yield scrapy.Request(url="https://www.urduzone.net/category/3-aurtain-3-kahaniyan/",callback=self.parse_stories)
        
        for story_link in self.extra_links:
            yield scrapy.Request(url=response.urljoin(story_link),callback=self.parse_individual_story)

    def parse_stories(self,response):
        story_links=response.xpath('//a/@href').getall()
        for story_link in story_links:
            yield scrapy.Request(url=response.urljoin(story_link),callback=self.parse_individual_story)

    def parse_individual_story(self,response):
        
            if self.notSkipPage(response):     
                #Extract story title in Roman Urdu
                story_title=response.xpath('//title/text()').get()
                #Extracting all text from HTML response
                all_text=response.css('*::text').getall()
                #Using regular expression to filter out Urdu from the text
                urdu_pattern=r'[\u0600-\u06FF]+'
                urdu_text=[text for text in all_text if re.search(urdu_pattern, text)]
                #Concatenate the filtered Urdu text into a single string
                urdu_text=' '.join(urdu_text)
                #Printing the extracted title and Urdu story on the terminal
                self.logger.info(f"Title:{story_title}")
                self.logger.info(f"Urdu Text:{urdu_text}")

                #Writing the extracted story to a CSV file
                file_exists=os.path.isfile('urduStories.csv')
                with open('urduStories.csv','a',newline='',encoding='utf-8') as csv_file:
                    writer = csv.writer(csv_file)             
                    if not file_exists:
                        writer.writerow(['Title','Story'])       
                    writer.writerow([story_title,urdu_text])