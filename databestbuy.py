import requests
from bs4 import BeautifulSoup
from database import Database

# URL of the Best Buy page
url = 'https://www.bestbuy.ca/en-ca/category/keyboards/20394?intlreferer=https://www.google.com/&intlredir=https://www.bestbuy.com/site/mice-keyboards/computer-keyboards/abcat0513004.c?id=abcat0513004'

# Headers to mimic a real browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Initialize the database
db = Database()

# Make the request to get the HTML content
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all product items
    products = soup.find_all('div', class_='productItemRow_hyNOs')

    # Extract information for each product and add to database
    for product in products:
        name = product.find('div', class_='productItemName_3IZ3c')
        price = product.find('div', class_='productPricingContainer_3gTS3')
        link = product.find('a', class_='link_3hcyN')

        product_name = name.text.strip() if name else ''
        product_price = price.text.strip() if price else ''
        product_url = f"https://www.bestbuy.ca{link['href']}" if link and 'href' in link.attrs else ''

        db.add_product(product_name, product_price, product_url)

    print("Product information added to the database")

    # Close the database connection
    db.close()

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
