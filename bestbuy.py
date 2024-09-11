import requests

url = 'https://www.bestbuy.ca/en-ca/category/over-ear-headphones/21271?icmp=pa_categorydetail_headphones_shopby_cat_overear'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    with open('page.html', 'w', encoding='utf-8') as file:
        file.write(response.text)
    print("HTML content written to page.html")
else:
    print(f"Failed to retrieve page. Status code: {response.status_code}")
