"""
Contains Subway class to scrape outlet data from Subway website.
"""

import re
import json
import requests
from bs4 import BeautifulSoup
from .scrape_interface import ScrapeInterface


class Subway(ScrapeInterface):
    """
    Scraper class for scraping data from the Subway website.
    """

    def __init__(self, url: str) -> None:
        super().__init__(url)
        self.url = url

    def scrape(self) -> None:
        """
        Scrapes the data from the Subway website.
        """
        html_text = requests.get(self.url, timeout=5).text

        outlet_data = re.search(
            r'"markerData":(\[.*?\}\]),', html_text).group(1)
        outlet_json_data = json.loads(outlet_data)

        for outlet in outlet_json_data:
            (name, address, time, google_maps_link, waze_link, lat, lng
             ) = self._parse(outlet)

            self.outlets.append({
                "name": name,
                "address": address,
                "time": time,
                "google_maps_link": google_maps_link,
                "waze_link": waze_link,
                "lat": lat,
                "lng": lng,
            })

    def _parse(self, element) -> tuple:
        """
        Parses the data from the given element.

        Args:
            element (dict): The element containing the data to parse.

        Returns:
            tuple: The parsed data.
        """

        # Extract content to parse
        content = element["infoBox"]["content"]
        soup = BeautifulSoup(content, "html.parser")

        # Extract store name
        name = soup.find("h4").text.strip()

        # Extract address
        address = soup.find("div", class_="infoboxcontent").p.text.strip()

        # Extract time
        time = soup.find("div", class_="infoboxcontent").p.find_next_sibling(
            "p").text.strip()

        # Extract Google Maps and Waze links
        direction_buttons = soup.find(
            "div", class_="directionButton").find_all("a")
        google_maps_link = direction_buttons[0]["href"]
        waze_link = direction_buttons[1]["href"]

        # Extract latitude and longitude
        lat = float(element["position"]["lat"])
        lng = float(element["position"]["lng"])

        return name, address, time, google_maps_link, waze_link, lat, lng


if __name__ == "__main__":

    subway = Subway("https://subway.com.my/find-a-subway")
    subway.scrape()
    print(len(subway.get_data))
