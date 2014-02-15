from bs4 import BeautifulSoup
import urllib2
import csv
from pyparsing import Literal, quotedString, removeQuotes, delimitedList
import time
from random import randint


# Scrape restaurant information
def restscrape(resturl, filenamersc, filenamerevsc):

    time.sleep(randint(2,8))
    # Read the url
    response = urllib2.urlopen(resturl)
    soup = BeautifulSoup(response.read())
    response.close()


    # Check if it is rated
    if soup.find(itemprop="ratingValue") == None:
        return

    # Anamoly
    if soup.find(class_="container no-reviews") != None:
        return

    # Check if it is not the alternate version
    if soup.find(id="mapbox") != None:
        print "alt version"
        restscrape(resturl, filenamersc, filenamerevsc)
        return

    # Check if it is not an alternate version
    if soup.find(class_="friend-count miniOrange") == None:
        print "alt version rev"
        restscrape(resturl, filenamersc, filenamerevsc)
        return

#### ##    ## ########  #######  
 ##  ###   ## ##       ##     ## 
 ##  ####  ## ##       ##     ## 
 ##  ## ## ## ######   ##     ## 
 ##  ##  #### ##       ##     ## 
 ##  ##   ### ##       ##     ## 
#### ##    ## ##        #######  

    # Key Yelp information
    title = soup.find(property="og:title").get("content").encode('utf-8')
    latitude = soup.find(property="place:location:latitude").get("content")
    longitude = soup.find(property="place:location:longitude").get("content")
    rating = soup.find(itemprop="ratingValue").get("content")
    reviewCount = soup.find(itemprop="reviewCount").get_text()

    if soup.find(id="cat_display") != None:
        categories = soup.find(id="cat_display").get_text().strip()
        categories = ' '.join(categories.split())
    else:
        categories = "None"

    if soup.find(class_="photo-box-img")['src'] != "http://s3-media1.ak.yelpcdn.com/assets/2/www/img/5f69f303f17c/default_avatars/business_medium_square.png":
        photos = "Has photos"
    else:
        photos = "None"

    if soup.find(id="bizUrl") != None:
         URL = soup.find(id="bizUrl").get_text().strip().encode('utf-8')
    else:
        URL = "None"

    # Get Neighborhoods
    # Particularly special code because it has to be stripped from javascript script
    # Automatically strip quotes from quoted strings
    # quotedString matches single or double quotes
    neighborhood = ""
    quotedString.setParseAction(removeQuotes)

    # Define a pattern to extract the neighborhoods: entry
    neighborhoodsSpec = Literal('\"neighborhoods\":') + '[' + delimitedList(quotedString)('neighborhoods') + ']'

    for hoods in neighborhoodsSpec.searchString(soup):
        neighborhood = str(hoods.neighborhoods)


    # Yelp Interaction/Information
    if soup.find(class_="yelp-menu") != None:
        menu = "Has menu"
    else:
        menu = "None"

    if soup.find(id="opentable-reservation-actions") != None:
        reservable = "Reservable"
    else:
        reservable = "None"

    if soup.find(class_="media-story offer-detail") != None:
        deal = "Has deal"
    else:
        deal = "None"
        
    if soup.find(id="delivery-address-form") != None:
        yelpDelivery = "Delivery system"
    else:
        yelpDelivery = "None"        

    if soup.find(id="bizSlide") != None:
        slides = "Has slides"
    else:
        slides = "None"


    # Restaurant status
    if soup.find(id="bizSupporter") != None:
        sponsor = "Sponsors"
    else:
        sponsor = "None"

    if soup.find(id="bizClaim") != None:
        claim = "Unclaimed"
    else:
        claim = "None"

    if soup.find(style="color:#999999;") == None:
        eliteReviews = "Has Elites"
    else:
        eliteReviews = "None"


    # Restaurant attributes from attributes section
    # Attributes self-explanatory
    if soup.find(class_="attr-transit") != None:
        transit = soup.find(class_="attr-transit").get_text().strip()
    else:
        transit = "None"

    if soup.find(class_="attr-BusinessHours") != None:
        hours = soup.find('dd', class_="attr-BusinessHours").get_text()
    else:
        hours = "None"

    if soup.find(class_="attr-RestaurantsAttire") != None:
        attire = soup.find('dd', class_="attr-RestaurantsAttire").get_text()
    else:
        attire = "None"

    if soup.find(class_="attr-BusinessAcceptsCreditCards") != None:
        creditCards = soup.find('dd', class_="attr-BusinessAcceptsCreditCards").get_text()
    else:
        creditCards = "None"

    if soup.find(class_="attr-BusinessParking") != None:
        parking = soup.find('dd', class_="attr-BusinessParking").get_text()
    else:
        parking = "None"

    if soup.find(class_="attr-RestaurantsPriceRange2") != None:
        price = soup.find('dd', class_="attr-RestaurantsPriceRange2").get_text().strip()
    else:
        price = "None"

    if soup.find(class_="attr-RestaurantsGoodForGroups") != None:
        groups = soup.find('dd', class_="attr-RestaurantsGoodForGroups").get_text()
    else:
        groups = "None"

    if soup.find(class_="attr-GoodForKids") != None:
        kids = soup.find('dd', class_="attr-GoodForKids").get_text()
    else:
        kids = "None"

    if soup.find(class_="attr-RestaurantsReservations") != None:
        reservations = soup.find('dd', class_="attr-RestaurantsReservations").get_text()
    else:
        reservations = "None"

    if soup.find(class_="attr-RestaurantsDelivery") != None:
        delivery = soup.find('dd', class_="attr-RestaurantsDelivery").get_text()
    else:
        delivery = "None"

    if soup.find(class_="attr-RestaurantsTakeOut") != None:
        takeout = soup.find('dd', class_="attr-RestaurantsTakeOut").get_text()
    else:
        takeout = "None"

    if soup.find(class_="attr-RestaurantsTableService") != None:
        service = soup.find('dd', class_="attr-RestaurantsTableService").get_text()
    else:
        service = "None"

    if soup.find(class_="attr-OutdoorSeating") != None:
        outdoorSeating = soup.find('dd', class_="attr-OutdoorSeating").get_text()
    else:
        outdoorSeating = "None"

    if soup.find(class_="attr-WiFi") != None:
        wifi = soup.find('dd', class_="attr-WiFi").get_text()
    else:
        wifi = "None"

    if soup.find(class_="attr-GoodForMeal") != None:
        meals = soup.find('dd', class_="attr-GoodForMeal").get_text()
    else:
        meals = "None"

    if soup.find(class_="attr-BestNights") != None:
        bestNights = soup.find('dd', class_="attr-BestNights").get_text()
    else:
        bestNights = "None"

    if soup.find(class_="attr-HappyHour") != None:
        happyHour = soup.find('dd', class_="attr-HappyHour").get_text()
    else:
        happyHour = "None"

    if soup.find(class_="attr-Alcohol") != None:
        alcohol = soup.find('dd', class_="attr-Alcohol").get_text()
    else:
        alcohol = "None"

    if soup.find(class_="attr-Smoking") != None:
        smoking = soup.find('dd', class_="attr-Smoking").get_text()
    else:
        smoking = "None"

    if soup.find(class_="attr-CoatCheck") != None:
        coatCheck = soup.find('dd', class_="attr-CoatCheck").get_text()
    else:
        coatCheck = "None"        

    if soup.find(class_="attr-NoiseLevel") != None:
        noise = soup.find('dd', class_="attr-NoiseLevel").get_text()
    else:
        noise = "None"

    if soup.find(class_="attr-GoodForDancing") != None:
        goodForDancing = soup.find('dd', class_="attr-GoodForDancing").get_text()
    else:
        goodForDancing = "None"

    if soup.find(class_="attr-Ambience") != None:
        ambience = soup.find('dd', class_="attr-Ambience").get_text()
    else:
        ambience = "None"

    if soup.find(class_="attr-HasTV") != None:
        tv = soup.find('dd', class_="attr-HasTV").get_text()
    else:
        tv = "None"

    if soup.find(class_="attr-Caters") != None:
        caters = soup.find('dd', class_="attr-Caters").get_text()
    else:
        caters = "None"

    if soup.find(class_="attr-WheelchairAccessible") != None:
        wheelchairAccessible = soup.find('dd', class_="attr-WheelchairAccessible").get_text()
    else:
        wheelchairAccessible = "None"

    if soup.find(class_="attr-DogsAllowed") != None:
        dogsAllowed = soup.find('dd', class_="attr-DogsAllowed").get_text()
    else:
        dogsAllowed = "None"


    with open(filenamersc, "ab") as filer:
        fr = csv.writer(filer)
        # Writing to CSV
        fr.writerow([resturl, title, latitude, longitude, rating, reviewCount, categories, photos, URL, neighborhood, menu, reservable, yelpDelivery, slides, sponsor, claim, eliteReviews, transit, hours, attire, creditCards, parking, price, groups, kids, reservations, deal, delivery, takeout, service, outdoorSeating, wifi, meals, bestNights, happyHour, alcohol, smoking, coatCheck, noise, goodForDancing, ambience, tv, caters, wheelchairAccessible])

########  ######## ##     ## #### ######## ##      ##  ######  
##     ## ##       ##     ##  ##  ##       ##  ##  ## ##    ## 
##     ## ##       ##     ##  ##  ##       ##  ##  ## ##       
########  ######   ##     ##  ##  ######   ##  ##  ##  ######  
##   ##   ##        ##   ##   ##  ##       ##  ##  ##       ## 
##    ##  ##         ## ##    ##  ##       ##  ##  ## ##    ## 
##     ## ########    ###    #### ########  ###  ###   ######  

    # Parsing top 40 Reviews
    reviews = soup.findAll(itemprop="review")
    for review in reviews:
        
        # Get user data
        if review.find(title="User is Elite") != None:
            eliteStatus = "Elite"
        else:
            eliteStatus = "None"

        friendCount = review.find(class_="friend-count miniOrange").get_text()[:-8].strip()
        reviewCount = review.find(class_="review-count miniOrange").get_text()[:-8].strip()

        if review.find(class_="photo-box-img")['src'] != "http://s3-media4.ak.yelpcdn.com/assets/2/www/img/78074914700f/default_avatars/user_small_square.png":
            userPhoto = "Has photo"
        else:
            userPhoto = "None"

        reviewInfo = review.find(class_="reviewer_info").get_text().encode('utf-8')


        # Get review data
        reviewRating = review.find(itemprop="ratingValue").get("content")
        publish = review.find(itemprop="datePublished").get("content")
        description = review.find(itemprop="description").get_text().encode('utf-8')


        # Get review attributes
        if review.find(class_="i-wrap ig-wrap-common i-camera-common-wrap badge photo-count") != None:
            reviewPix = review.find(class_="i-wrap ig-wrap-common i-camera-common-wrap badge photo-count").get_text()[:-6].strip()
        else:
            reviewPix = "None"

        if review.find(class_="i-wrap ig-wrap-common i-opentable-badge-common-wrap badge opentable-badge-marker") != None:
            reviewSeated = "Seated"
        else:
            reviewSeated = "None"

        if review.find(class_="i ig-common i-deal-price-tag-common") != None:
            reviewDeal = "Purchased Deal"
        else:
            reviewDeal = "None"

        if review.find(class_="i-wrap ig-wrap-common i-checkin-burst-blue-small-common-wrap badge checkin checkin-irregular") != None:
            reviewCheckIn = review.find(class_="i-wrap ig-wrap-common i-checkin-burst-blue-small-common-wrap badge checkin checkin-irregular").get_text()[:-14].strip()
        else:
            reviewCheckIn = "None"


        # Special Qype users lack stats
        if review.find(class_="count"):
            usefulfunnycool = review.findAll(class_="count")
            # Get useful, funny, cool statistics
            if usefulfunnycool[0].get_text() != "":
                useful = usefulfunnycool[0].get_text()
            else:
                useful = 0

            if usefulfunnycool[1].get_text() != "":
                funny = usefulfunnycool[1].get_text()
            else:
                funny = 0

            if usefulfunnycool[2].get_text() != "":
                cool = usefulfunnycool[2].get_text()
            else:
                cool = 0
        else:
            useful = 0
            funny = 0
            cool = 0

        with open(filenamerevsc, "ab") as filerev:
            frev = csv.writer(filerev)
            # Writing to CSV
            frev.writerow([resturl, eliteStatus, friendCount, reviewCount, userPhoto, reviewInfo, reviewRating, publish, description, reviewPix, reviewSeated, reviewDeal, reviewCheckIn, useful, funny, cool])

##     ##    ###    #### ##    ## 
###   ###   ## ##    ##  ###   ## 
#### ####  ##   ##   ##  ####  ## 
## ### ## ##     ##  ##  ## ## ## 
##     ## #########  ##  ##  #### 
##     ## ##     ##  ##  ##   ### 
##     ## ##     ## #### ##    ## 

# List of all locations
# 'Alphabet_City','Battery_Park','Chelsea','Chinatown','Civic_Center','East_Harlem','East_Village','Financial_District','Flatiron','Gramercy','Greenwich_Village','Harlem','Hell\'s_Kitchen','Inwood','Kips_Bay','Koreatown','Little_Italy','Lower_East_Side','Manhattan_Valley','Marble_Hill','Meatpacking_District','Midtown_East','Midtown_West','Morningside_Heights','Murray_Hill','NoHo','Nolita','Roosevelt_Island','SoHo','South_Street_Seaport','South_Village','Stuyvesant_Town','Theater_District','TriBeCa','Two_Bridges','Union_Square','Upper_East_Side','Upper_West_Side','Washington_Heights','West_Village', 'Yorkville'

# Yorkville entirely encompassed by Upper East Side
# Theater District entirely encompassed by Midtown West

# List all the locations
searchLocations = ['Alphabet_City','Battery_Park','Chelsea','Chinatown','Civic_Center','East_Harlem','East_Village','Financial_District','Flatiron','Gramercy','Greenwich_Village','Harlem','Hell\'s_Kitchen','Inwood','Kips_Bay','Koreatown','Little_Italy','Lower_East_Side','Manhattan_Valley','Marble_Hill','Meatpacking_District','Midtown_East','Midtown_West','Morningside_Heights','Murray_Hill','NoHo','Nolita','Roosevelt_Island','SoHo','South_Street_Seaport','South_Village','Stuyvesant_Town','TriBeCa','Two_Bridges','Union_Square','Upper_East_Side','Upper_West_Side','Washington_Heights','West_Village']

# Agent spoofer, default agent got IP banned too fast.
opener = urllib2.build_opener()
# IE 9 proved to be the most successful
opener.addheaders = [('User-agent', 'IE 9/Windows: Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)')]
urllib2.install_opener(opener)

# Iterate through
for searchLocation in searchLocations:
    # Print for reference
    print searchLocation
    filenamer = "yelpr_" + searchLocation + ".csv"
    filenamerev = "yelprev_" + searchLocation + ".csv"

    # File setup
    with open(filenamer, "ab") as filer:
        fr = csv.writer(filer)
        # Write reference row
        fr.writerow(['resturl', 'title', 'latitude', 'longitude', 'rating', 'reviewCount', 'categories', 'photos', 'URL', 'neighborhood', 'menu', 'reservable', 'yelpDelivery', 'slides', 'sponsor', 'claim', 'eliteReviews', 'transit', 'hours', 'attire', 'creditCards', 'parking', 'price', 'groups', 'kids', 'reservations', 'deal', 'delivery', 'takeout', 'service', 'outdoorSeating', 'wifi', 'meals', 'bestNights', 'happyHour', 'alcohol', 'smoking', 'coatCheck', 'noise', 'goodForDancing', 'ambience', 'tv', 'caters', 'wheelchairAccessible'])

    with open(filenamerev, "ab") as filerev:
        frev = csv.writer(filerev)
        # Write reference row
        frev.writerow(['resturl', 'eliteStatus', 'friendCount', 'reviewCount', 'userPhoto', 'reviewInfo', 'reviewRating', 'publish', 'description', 'reviewPix', 'reviewSeated', 'reviewDeal', 'reviewCheckIn', 'useful', 'funny', 'cool'])

    # Build number to iterate search #
    for num in range(0,100):

        print num
        # Build URL
        searchurl = "http://www.yelp.com/search?find_desc=restaurants&start=" + str(num*10) + "&l=p:NY:New_York:Manhattan:" + searchLocation
        
        # Read URL
        responseMain = urllib2.urlopen(searchurl)
        soupMain = BeautifulSoup(responseMain.read())
        responseMain.close()

        # If there are no more entries, break out of the loop and go to the next searchLocation
        if soupMain.find(class_="broaden-search-suggestions") != None:
            break

        # Otherwise get listings
        listings = soupMain.find_all(class_="search-result natural-search-result biz-listing-large")
        listingurls = []

        # Iterate through listings
        for listing in listings:
     
            # Check if no ratings
            if listing.find(class_="biz-rating biz-rating-large clearfix") != None:
                # Pull the url if it has ratings and add to list
                listingurls.append(listing.find('a')['href'])

        # Then get the url list
        for listingurl in listingurls:
            
            print listingurl
            # Then use scrapers on the urls 
            restscrape(str("http://www.yelp.com" + listingurl), filenamer, filenamerev)

        # Delays to help reduce queries and reduce the possibility of IP Ban
        time.sleep(60)

    time.sleep(600)