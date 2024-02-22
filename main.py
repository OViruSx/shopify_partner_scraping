from bs4 import BeautifulSoup
import requests
import re
import time  
import csv 

def get_soup(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        return BeautifulSoup(response.text, 'html.parser')

def get_profile_data(profile):
    profile_name = profile.find('h3', class_='mb-1 text-xl font-semibold text-gray-900').text.strip()
    profile_price = profile.find('span', class_='font-medium text-base').text.strip()
    services = profile.find('span', class_='text-base xs:font-normal md:font-medium xs:inline-block md:block').text.strip()
    profile_url = base_url + profile['href']
    return profile_name, profile_price, services, profile_url

def get_additional_data(div):
    web = div.find('a', href=re.compile(r'.*https://.*'))
    email = div.find('a', href=re.compile(r'.*mailto:.*'))
    tel = div.find('a', href=re.compile(r'.*tel:.*'))
    rating = div.find('p', class_='text-base font-medium')
    partnering_date = div.find('p', class_='richtext').text.strip()
    return rating.text.strip(), web['href'] if web else 'No website', email['href'] if email else 'No email', tel['href'] if tel else 'No tel', partnering_date

base_url = 'https://www.shopify.com'

# writing to a csv file
with open('shopify_profiles.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # writing the headers
    writer.writerow(['Profile Name', 'Profile URL', 'Price Range', 'Services', 'Rating', 'Website', 'Email', 'Tel', 'Partnering Date'])

    # iterate over pages
    for page_num in range(1, 11):  # change the range as needed
        soup = get_soup(f'{base_url}/partners/directory/services?page={page_num}')

        # find all of the profile listings
        listings = soup.find_all(
            'a', 'w-full pt-4 pr-6 pb-4 pl-4 bg-transparent grid xs:grid-cols-[80px_1fr] md:grid-cols-[91px_1fr] grid-rows-[auto_auto]'
        )

        # getting all of the profile names, urls, price range, services
        for profile in listings:
            profile_name, profile_price, services, profile_url = get_profile_data(profile)
            print(profile_name, profile_url, profile_price, services)

            # getting the profile page
            profile_soup = get_soup(profile_url)
            divs = profile_soup.find_all(
                'div', class_='flex flex-col gap-y-5 relative md:rounded-lg xs:pt-0 md:pt-24 md:px-6 md:pb-6 md:shadow-light'
            )
            for div in divs:
                rating, web, email, tel, partnering_date = get_additional_data(div)
                print(rating, web, email, tel)
                print('About to write row')  
                writer.writerow([profile_name, profile_url, profile_price, services, rating, web, email, tel, partnering_date])
                print('Successfully wrote row')  

            time.sleep(2)  # delay for 2 seconds to avoid being blocked