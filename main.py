from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

BASEPAGEURL = "https://www.mtbproject.com/featured/featured-rides/highest-rated"


def main():
    """Main entry point of project"""
    jsonObj = json.load(open('featuredRides.json', 'r', encoding='utf-8'))
    stateDict = {}
    for rideObj in jsonObj:
        if rideObj['state'].strip() in stateDict:
            stateDict[rideObj['state'].strip()] += 1
        else:
            stateDict[rideObj['state'].strip()] = 1

    rideList = []
    for key in stateDict:
        rideList.append([key, stateDict[key]])
    rideList = sorted(rideList, key=lambda ride: ride[1])
    print(rideList)

    # also need to get lat and long information. Should probably do this up front.
    # https://maps.googleapis.com/maps/api/geocode/json?address=ParkCity,UT&key=MY_KEY_HERE
    # scraper = MtbProjectScraper(BASEPAGEURL)
    # scraper.getInfoFromSites()
    # with open('featuredRides.json', 'w', encoding='utf-8') as f:
    #     f.write(scraper.toJSON())


class FeaturedRide:
    """Holds information about an individual featured ride."""

    def __init__(self):
        self.position = 0
        self.id = 0
        self.name = ""
        self.numReviews = 0
        self.city = ""
        self.state = ""
        self.numStars = 0
        self.reviewText = ""
        self.distance = 0


class MtbProjectScraper:
    """Scrapes info about top 300 featured rides on MTB project."""

    def __init__(self, basePageURL):
        self.featuredRides = []
        self.basePageURL = basePageURL

    def getInfoFromSites(self):
        # loop through sites, grabbing info from each one
        rideCount = 1
        for x in range(1, 11):
            # open page
            page = ""
            if x == 1:
                page = urlopen(self.basePageURL)
            else:
                page = urlopen(self.basePageURL + "?page=" + str(x))

            # get container divs for each featured ride card
            soup = BeautifulSoup(page, 'html.parser')
            cardTextContainers = soup.find_all(
                'div', {'class': 'card-with-photo trail-card text-black'})

            for cardText in cardTextContainers:
                self.featuredRides.append(
                    self.getFeaturedRideInfoFromCardText(cardText, rideCount))
                rideCount += 1

    def getFeaturedRideInfoFromCardText(self, rideCardContainer, position):
        featuredRide = FeaturedRide()

        featuredRide.id = rideCardContainer.find('a')['href'].split('/')[4]
        featuredRide.name = self.cleanText(rideCardContainer.find(
            'div', {'class': 'text-truncate title-row'}).text)
        featuredRide.distance = self.cleanText(rideCardContainer.find(
            'span', {'class': 'imperial'}).text)
        featuredRide.numReviews = int(self.cleanText(rideCardContainer.find(
            'span', {'class': 'score-details'}).text))
        cityState = self.cleanText(rideCardContainer.find(
            'div', {'class': 'text-truncate city-state'}).text)
        featuredRide.city = cityState.split(',')[0]
        featuredRide.state = cityState.split(',')[1]
        featuredRide.position = position

        return featuredRide

    def cleanText(self, text):
        return text.replace('\r', "").replace("\n", "").replace("\r\n", "").strip()

    def toJSON(self):
        return json.dumps(self.featuredRides, default=lambda obj: obj.__dict__, sort_keys=True, indent=4)


main()
