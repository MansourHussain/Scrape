import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest
import lxml


page_num = 2


while page_num < 288:
    # 1 lists
    district_Name = []
    property_size = []
    property_price = []
    links = []
    dates = []
    # beds = []
    # paths = []

    # 2 the link to the website
    # here I included the `page_num` in the link
    try:
        result = requests.get(f"https://www.bayut.sa/en/riyadh-region/villas-for-sale/page-{page_num}/")
        src = result.content

        # 4 create soup
        soup = BeautifulSoup(src, "lxml")

        # 5 titles we need: districtName, property Age, size, rooms, price
        districtName = soup.findAll("div", {"aria-label": "Location"})
        size = soup.findAll("span", {"aria-label": "Area"})
        price = soup.findAll("span",{"aria-label": "Price"})
        listing_link = soup.findAll("a", {"aria-label": "Listing link"})
        bed = soup.findAll("span", {"aria-label": "Beds"}, {"class": "b6a29bc0"})
        path = soup.findAll("span", {"aria-label": "Beds"}, {"class": "b6a29bc0"})


        main_url= 'https://www.bayut.sa'

        # 6 for loop to get text and append it to a list
        for i in range(len(districtName)):
            district_Name.append(districtName[i].text)
            links.append(main_url+listing_link[i].attrs["href"])
            property_size.append(size[i].text)
            property_price.append(price[i].text)
            # beds.append(bed[i].text)
            # paths.append(path[i].text)

        # 7 extract post date from inner page
        for link in (links):
            result = requests.get(link)
            src = result.content
            soup = BeautifulSoup(src, "lxml")
            date = soup.find("span", {"aria-label":"Reactivated date"})
            dates.append(date.text)

        page_num += 1
    except Exception as e:
        print(e)


    file_list = [district_Name, property_size, property_price, dates, links]
    exported = zip_longest(*file_list)
    # 8 create a csv file and fill it with values
    with open("C:/Users/Manso/Desktop/files\Data Analysis\Riyadh_Homes_english_beta.csv", "w") as homes_file:
        wr = csv.writer(homes_file, lineterminator="\n")
        wr.writerow(['district_Name', 'property_size', 'property_price', 'dates', 'links'])
        wr.writerows(exported)


