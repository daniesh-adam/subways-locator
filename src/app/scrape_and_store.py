
"""Performs requests to the Google Maps Geocoding API."""
from app.services.scrape import Subway
from app.utils.database import create_table, add_many_to_table
import googlemaps


def get_geographical_coordinates(address: str) -> tuple[str]:
    """
    This function retrieves the geographical coordinates (latitude and longitude)
    and the formatted address of a given address using the Google Maps API.

    Parameters:
    address (str): The address to geocode.

    Returns:
    tuple[str]: A tuple containing the latitude, longitude, and formatted address.
    """

    lat = ""
    lng = ""
    formatted_address = ""

    # Retrieve geographical coordinates based on the address
    results = gmaps.geocode(address=address)

    # Extract the 'geographical coordinates' and 'formatted_address'
    for item in results:
        lat = item["geometry"]["location"]["lat"]
        lng = item["geometry"]["location"]["lng"]
        formatted_address = item["formatted_address"]

    return lat, lng, formatted_address


# ! API key
GMAPS_API_KEY = "AIzaSyBhjA6ve6TUVTHS6fuzS9Mw0BLlriBSuig"

# Initialise gmaps client
gmaps = googlemaps.Client(key=GMAPS_API_KEY)

# Scrape Subway data
subway = Subway("https://subway.com.my/find-a-subway")
subway.scrape()
subway_outlets_data = subway.get_data

# Replace the geographical coordinates
for data in subway_outlets_data:

    address = data["address"]

    lat, lng, formatted_address = get_geographical_coordinates(address=address)

    data["lat"] = lat
    data["lng"] = lng
    data["formatted_address"] = formatted_address

# Convert into a list of tuples and filter only "Kuala Lumpur"
subway_outlets_data = [
    (data["name"], data["address"], data["time"],
     data["waze_link"], data["lat"], data["lng"])
    for data in subway_outlets_data
    if "Kuala Lumpur" in data["formatted_address"]]

# Create database table and add data
DB = "app/data/outlets.db"
create_table(db_path=DB, table_name="subway")
add_many_to_table(db_path=DB, table_name="subway",
                  data=subway_outlets_data)
