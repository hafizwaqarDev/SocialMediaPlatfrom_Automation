from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.options import ArgOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import csv,time

class youtubeScraper():
    def __init__(self,Answer):
        self.answer = Answer.lower()
    
    def openBrowser(self):
        driverPath = ChromeDriverManager().install()
        servc = Service(driverPath)
        driver = webdriver.Chrome(service=servc)
    
    def userSearch(self):
        if self.answer == 'y':
            inputSearch = input('enter search youtuber name:- ')
            print(f"\n--------------------please wait loading--------------------\n")
            querry = f"https://www.youtube.com/results?search_query={inputSearch}&sp=EgIQAg%253D%253D"
            userSearch = '+'.join(querry.split(' '))
        if self.answer == 'v':
            inputSearch = input('enter search about the video:- ')
            print(f"\n--------------------please wait loading--------------------\n")
            querry = f"https://www.youtube.com/results?search_query={inputSearch}"
            userSearch = '+'.join(querry.split(' '))

    def scrollDown(self,driver,endpoint):
        for page in range(endpoint):
            body = driver.find_element(By.TAG_NAME, 'body')
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
    
    def clickElement(self,driver):
        try:
            xpath = '//div[@class="tab-content style-scope tp-yt-paper-tab"]/div[contains(text(),"About")]'
            element = driver.find_element(By.XPATH,xpath)
        except:
            time.sleep(2)
            xpath = '//tp-yt-paper-button[@id="expand"]'
            element = driver.find_element(By.XPATH,xpath)
            time.sleep(1)

    def getAndsaveLinks(self,driver,userSearch):
        driver.get(userSearch)
        time.sleep(8)
        print(f"\n[Info] How much time do you want to scroll down this page:- ")
        endpoint = int(input('enter a number:- '))
        self.scrollDown(driver,endpoint)
        urlsTag = driver.find_elements(By.XPATH,'//a[@id="main-link"]') or driver.find_elements(By.XPATH,'//a[@id="video-title"]')
        for tag in urlsTag:
            TagLinks = tag.get_attribute('href')
            with open(file='youtubeLinks.txt',mode='a') as file:
                file.write(TagLinks + '\n')
    
    def readFile(self):
        with open(file='youtubeLinks.txt',mode='r') as file:
            readData = file.readlines()
            youtubelinks = [data.strip() for data in readData]
        
    def parseData(self,driver,youtubelinks):
        try:
            # data scrape for youtube channels
            for link in youtubelinks:
                driver.get(link)
                time.sleep(2)
                endpoint = 3
                self.scrollDown(driver,endpoint)
                self.clickElement(driver)
                self.scrollDown(driver,endpoint)
                time.sleep(4)
                try: title = driver.find_element(By.XPATH,'//ytd-channel-name//yt-formatted-string').text.strip()
                except: title = 'None'
                try: youtubeId = driver.find_element(By.XPATH,'//yt-formatted-string[@id="channel-handle"]').get_attribute('textContent').strip()
                except: youtubeId = 'None'
                try: totalSubscriber = driver.find_element(By.XPATH,'//yt-formatted-string[@id="subscriber-count"]').text.strip()
                except: totalSubscriber = 'None'
                try: totalVideos = driver.find_element(By.XPATH,'//yt-formatted-string[@id="videos-count"]').get_attribute('innerText')
                except: totalVideos = 'None'
                try: content = driver.find_element(By.XPATH,'//div[@id="channel-tagline"]//div[@id="content"]').get_attribute('textContent').strip()
                except: content = 'None'
                try: image = driver.find_element(By.XPATH,'//img[@id="img"]').get_attribute('src')
                except: image = 'None'
                try: jonied = driver.find_element(By.XPATH,'//span[contains(text(),"Joined ")]/parent::yt-formatted-string').get_attribute('innerText')
                except: jonied = 'None'
                try: views = driver.find_element(By.XPATH,'//yt-formatted-string[contains(text(),"views")]').get_attribute('textContent').strip()
                except: views = 'None'
                try: 
                    socialMediaUrlTag = driver.find_elements(By.XPATH,'//div[@id="legacy-link-list-container"]/a')
                    socialMediaUrl = ' , '.join([tag.get_attribute('href') for tag in socialMediaUrlTag])
                except: socialMediaUrl = 'None'
                try: description = driver.find_element(By.XPATH,'//yt-formatted-string[@id="description"]').get_attribute('textContent').strip()
                except: description = 'None'
                row = [title,youtubeId,content,totalSubscriber,totalVideos,views,jonied,link,image,socialMediaUrl,description]
                print(f"[Info] Getting youtubers Data:- {title}")
                self.saveData(row)
        except:
            # data scrape for youtube Videos
            for url in youtubelinks:
                driver.get(url)
                time.sleep(6)
                endpoint = 1
                self.scrollDown(driver,endpoint)
                time.sleep(2)
                self.clickElement(driver)
                self.scrollDown(driver,3)
                try: videoTitle = driver.find_element(By.XPATH,'//ytd-watch-metadata//div[@id="title"]/h1/yt-formatted-string').text.strip()
                except: videoTitle = 'None'
                try: channelName = driver.find_element(By.XPATH,'//yt-formatted-string[contains(@class," ytd-channel-name ")]/a').text.strip()
                except: channelName = 'None'
                try: channelLink = driver.find_element(By.XPATH,'//yt-formatted-string[contains(@class," ytd-channel-name ")]/a').get_attribute('href').strip()
                except: channelLink = 'None'
                try: totalSubscriber = driver.find_element(By.XPATH,'//yt-formatted-string[@id="owner-sub-count"]').text.strip()
                except: totalSubscriber = 'None'
                try: totalViews = driver.find_element(By.XPATH,'//yt-formatted-string/span[contains(text(),"views")]').text.strip()
                except: totalViews = 'None'
                try: uploadDate = driver.find_element(By.XPATH,'//yt-formatted-string/span[contains(text(),"ago")]').get_attribute('textContent').strip()
                except: uploadDate = 'None'
                try: comments = driver.find_element(By.XPATH,'//span[text()=" Comments"]/parent::yt-formatted-string/span').get_attribute('textContent').strip()
                except: comments = 'None'
                try: aboutUs = driver.find_element(By.XPATH,'//ytd-text-inline-expander[@id="description-inline-expander"]').get_attribute('textContent').replace('\n','').strip()
                except: aboutUs = 'None'
                row = [videoTitle,url,channelName,channelLink,totalSubscriber,totalViews,uploadDate,comments,aboutUs]
                print(f"[Info] Getting youtube Video Data:- {videoTitle}")
                self.saveData(row)

    def header(self,answer):
        if answer.lower() == 'y':
            header = ['Channel Name','Youtuber Id','Content','Total Subscribers','Total Videos','Views','Jonied Date','Channel Link','Image','Social Media Links','Description']
            with open(file='youtubeData.csv',mode='w',encoding='UTF-8',newline='') as file:
                csv.writer(file).writerow(header)
                
        if answer.lower() == 'v':
            header = ['Video Title','Video Url','Channel Name','Channel Link','Total Subscriber','Total Views on Video','Upload Date','Comments','About Us']
            with open(file='youtubeData.csv',mode='w',encoding='UTF-8',newline='') as file:
                csv.writer(file).writerow(header)
   
    def saveData(self,row):
        with open(file='youtubeData.csv',mode='a',encoding='UTF-8',newline='') as file:
            csv.writer(file).writerow(row)
    
    def run(self):
        UserSearch = self.userSearch()
        driver = self.openBrowser()
        self.getAndsaveLinks(driver,UserSearch)
        yotubelinks = self.readFile()
        self.parseData(driver,yotubelinks)

open(file='youtubeLinks.txt',mode='w').close()
print(f"\n[Info] Do you want to delete all data and add new data! ")
dataanswer = input('enter your decision (y/n):- ')
print(f"\n[Info] Do you want to search videos Or youtube channels on Youtube?")
print(f"[Info] if do you want to search about the Videos? So, enter :- (v)")
print(f"[Info] if do you want to search about the Youtuber Channels? So, enter :- (y)")
answer = input('enter your descion:- ')
myClass = youtubeScraper(answer)
if dataanswer == 'y':
    myClass.header(answer)
    myClass.run()
else:
    myClass.run()
