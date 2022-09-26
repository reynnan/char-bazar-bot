from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from datetime import datetime

def select_world(world: str, browser: webdriver.Chrome):
    world_select = Select(browser.find_element(By.NAME,'filter_world'))
    world_select.select_by_value(world)

def select_vocation(vocation: str, browser: webdriver.Chrome):
    vocation_select = Select(browser.find_element(By.NAME,'filter_profession'))
    for index in range(len(vocation_select.options)):
        option = vocation_select.options[index]
        if (option.accessible_name == vocation):
            vocation_select.select_by_index(index)

def find_ending_auctions(browser: webdriver.Chrome):
    NOW = datetime.utcnow()
    auctions = browser.find_elements(By.CLASS_NAME, 'Auction')
    ending_soon = []

    for index in range(len(auctions)):
        auction = auctions[index]
        end_auction_time = datetime.fromtimestamp(int(auction.find_element(By.CLASS_NAME, 'AuctionTimer').get_attribute('data-timestamp')))

        # If ends in the next 24 hours add to the list
        if ((end_auction_time - NOW).days <= 1):
            bid = auction.find_element(By.CSS_SELECTOR, '.ShortAuctionDataValue > b').text
            name = auction.find_element(By.CLASS_NAME, 'AuctionHeader').text
            link = auction.find_element(By.CSS_SELECTOR, '.AuctionCharacterName > a').get_attribute('href')
            features = [] 
            for feature in auction.find_elements(By.CLASS_NAME, 'Entry'):
                features.append(feature.text)
            ending_soon.append({"bid": bid, "name": name, "link": link, "features": features})
    
    return ending_soon

def search_auctions(world: str, vocation: str):
    # SETUP
    options = Options()
    options.headless = True
    browser = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options)
    formatted_world = world.lower().capitalize()
    formatted_vocation = vocation.lower().capitalize()

    # GO TO CHAR BAZAR
    browser.get("https://www.tibia.com/charactertrade/?subtopic=currentcharactertrades")


    # SET THE RIGHT FILTERS
    select_world(formatted_world, browser)
    select_vocation(formatted_vocation, browser)

    # SEARCH
    browser.find_element(By.CSS_SELECTOR, '.BigButtonText[value="Apply"]').click()

    return find_ending_auctions(browser)
