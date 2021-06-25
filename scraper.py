from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import pandas as pd
import os

spider_name = "thebar"

# Set CWD to current file location
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

wait_seconds = 10
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://de.thebar.com/cocktail-rezepte?seeAll=true")

# Accept Cookies
WebDriverWait(driver, wait_seconds).until(
                EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler'))).click()

# Get acces to the page (age > 18)
age_select_day = Select(driver.find_element(By.ID, 'age_select_day'))
age_select_day.select_by_value('4')

age_select_month = Select(driver.find_element(By.ID, 'age_select_month'))
age_select_month.select_by_value('9')

age_select_year = Select(driver.find_element(By.ID, 'age_select_year'))
age_select_year.select_by_value('1997')

driver.find_element(By.ID,'age_confirm_btn').click()

# Extract the ~270 recipe tiles with general information and a link to the detail page
recipe_tiles = driver.find_elements(By.CLASS_NAME,'recipe-tile')

cocktail_names = []
cocktail_urls = []
cocktail_ratings = []
cocktail_votes = []
cocktail_difficulties = []
cocktail_img_urls = []

for recipe_tile in recipe_tiles:
    cocktail_names.append(recipe_tile.find_element(By.CSS_SELECTOR ,'h3').text)
    cocktail_urls.append(recipe_tile.find_element(By.CSS_SELECTOR ,'a').get_attribute("href"))
    cocktail_difficulties.append(recipe_tile.find_element(By.CLASS_NAME, "item-difficulty").find_element(By.CLASS_NAME, "tag").text)
    cocktail_img_urls.append(recipe_tile.find_element(By.CSS_SELECTOR, "img").get_attribute("src"))

    # Extract the rating and the count of rates of the cocktail
    cocktail_rating_div = recipe_tile.find_element(By.CLASS_NAME ,'item-rating-count')
    cocktail_ratings.append(cocktail_rating_div.find_element(By.CSS_SELECTOR, "meta").get_attribute("content"))
    cocktail_votes.append(cocktail_rating_div.text)

assert len(cocktail_names) == len(cocktail_urls) == len(cocktail_ratings) == len(cocktail_votes) == len(cocktail_difficulties) == len(cocktail_img_urls)

# Save the received data to a csv file
cocktail_df = pd.DataFrame({"name": cocktail_names,
                            "url":cocktail_urls,
                            "rating":cocktail_ratings,
                            "votes": cocktail_votes,
                            "difficulty": cocktail_difficulties,
                            "img_url": cocktail_img_urls,
                            "spider": [spider_name]*len(cocktail_names)})

cocktail_df.to_csv(path_or_buf = os.path.join("data", "cocktails_"+spider_name+".csv"), index=False, encoding = "utf-8")
