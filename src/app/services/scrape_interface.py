"""
Defines an abstract base class for all scraper classes to implement.
"""

from abc import ABC, abstractmethod
from typing import List, Dict


class ScrapeInterface(ABC):
    """
    Abstract base class for all scraper classes.

    Defines the interface for all scraper classes to implement.
    """

    def __init__(self, url: str) -> None:
        """
        Initializes the scraper with the given URL.

        Args:
            url (str): The URL of the website to scrape.
        """
        self.url: str = url
        self.outlets: List[Dict] = []

    @abstractmethod
    def scrape(self) -> None:
        """
        Scrapes the data from the website.
        """

    @abstractmethod
    def _parse(self, element) -> tuple:
        """
        Parses the data from the given element.

        Args:
            element (dict): The element containing the data to parse.

        Returns:
            tuple: The parsed data.
        """

    @property
    def get_data(self) -> List[Dict]:
        """
        Returns the scraped data.

        Returns:
            List[Dict]: The scraped data.
        """
        return self.outlets
