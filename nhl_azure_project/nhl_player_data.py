import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class NHLScraper:
    def __init__(self, season):
        self.season = season
        self.base_url = f"https://www.nhl.com/stats/skaters?reportType=season&seasonFrom={season}&seasonTo={season}&gameType=2&filter=gamesPlayed,gte,1&sort=points,goals,assists&page={{}}&pageSize=100"
        self.driver = webdriver.Chrome()
        self.page_num = 0
        self.all_player_data = []
        self.headers_table = []  # Initialize headers_table attribute

    def scrape(self):
        while True:
            self.driver.get(self.base_url.format(self.page_num))
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "rt-table"))
            )

            html_content = self.driver.page_source
            soup = BeautifulSoup(html_content, "html.parser")

            headers = soup.find_all("div", role="columnheader")
            self.headers_table = [
                header.text for header in headers if header.text != "i"
            ]  # Assign headers_table

            rows = soup.find_all("div", role="row")

            for row in rows:
                row_data = row.find_all("div", class_="rt-td")
                individual_row_data = [data.text.strip() for data in row_data[1:]]
                if individual_row_data:  # Check if row data is not empty
                    self.all_player_data.append(individual_row_data)

            next_button = soup.find("button", class_="next-button")
            if next_button and not next_button.has_attr("disabled"):
                self.page_num += 1
            else:
                break

            # Added a print statement to show progress
            logger.debug(f"Scraped page {self.page_num + 1}")

        self.driver.quit()


if __name__ == "__main__":
    season = input("Enter the season (e.g., 20142015): ")
    scraper = NHLScraper(season)
    scraper.scrape()
    nhl_stats_df = pd.DataFrame(scraper.all_player_data, columns=scraper.headers_table)
    nhl_stats_df.to_csv(f"nhl_player_stats_{season}.csv", index=False)
