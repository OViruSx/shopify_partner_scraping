This is a simple script used to scrape the data of the official partners of shopify "https://www.shopify.com/partners/directory/services".
it scrapes data like: Partner name, partnering year, price range, services and contact info. It can be used given a number of pages to scrape. And then turn the data into a csv for further analyzing. 

Prerequisites:
* bs4. (Beautifulsoup)
* requests

you can change the delay time between requests for each page in the:
time.sleep(sec)  
^change the "sec" to any int of seconds you want. 
