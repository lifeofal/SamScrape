from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from chrome_Window_Options import chromeOptions
from selenium.common.exceptions import NoSuchElementException
import json
from multiprocessing import Pool



class PageIteration:

    def __init__(self):
        self.multi()

    def createDriver(self, pageNum):

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chromeOptions())
        driver.get(f'https://lostpoets.xyz/poets/{pageNum}-65536')

        driver.implicitly_wait(1)
        return driver

    def writeToJSONFile(self, path, fileName, data):
        filePathNameWExt = './' + path + '/' + fileName + '.json'
        with open(filePathNameWExt, 'w') as fp:
            json.dump(data, fp, ensure_ascii=False, indent=4, sort_keys=False)
            print("Json dump")

    def multi(self):
        pool = Pool(processes=3)
        for i in range(3):
            print("Process: ", i)
            if i == 0:
                pool_results = pool.apply_async(self.linkFollower, args=(1, 'properties1'))
            elif i == 1:
                pool_results = pool.apply_async(self.linkFollower, args=(21845, 'properties2'))
            else:
                pool_results = pool.apply_async(self.linkFollower, args=(43691, 'properties3'))


        # creating diff pools of multi threads
        pool.close()
        pool.join()

    def linkFollower(self, pageRange, filename):
        dataPage = {}
        driver = self.createDriver(pageRange)

        if pageRange == 1:
            pageBound = 21846
        elif pageRange == 21845:
            pageBound = 43692
        else:
            pageBound = 65536


        for i in range(pageRange, pageBound):  # 65536

            if pageRange == pageRange/2:
                print("""
                
                --- Reached half of thread range for thread ---
                
                
                """)
            url = f'https://lostpoets.xyz/poets/{i}-65536'

            entry = self.findPageInfo(driver, url)
            dataPage[f'Page {i}'] = [entry]

            print(f"Page {i}", entry)
        self.writeToJSONFile("./", filename, dataPage)

    def findPageInfo(self, driver, url):

        driver.get(url)

        entry = {}

        # try for the text values
        try:
            driver.implicitly_wait(2)
            driver.find_element_by_id('poet-details')
            driver.find_element_by_class_name('label')

        except NoSuchElementException:
            driver.implicitly_wait(0)
            return

        entry["ORIGIN"] = driver.find_element_by_xpath("//*[@id=\"poet-details\"]/div[3]/div/div[1]/span[2]").text
        entry["LATENT"] = driver.find_element_by_xpath("//*[@id=\"poet-details\"]/div[3]/div/div[2]/span[2]").text
        entry["AGE"] = driver.find_element_by_xpath("//*[@id=\"poet-details\"]/div[4]/div/div[1]/span[2]").text
        entry["GENRE"] = driver.find_element_by_xpath("//*[@id=\"poet-details\"]/div[4]/div/div[2]/span[2]").text

        # for key in entry:
        #     if not entry.get(key):
        #         entry[key] = "NULL"

        return entry
