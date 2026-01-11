

import requests

# Where USD is the base currency you want to use
url = 'https://v6.exchangerate-api.com/v6/579eaae88747e201b90b4623/latest/INR'

# Making our request
response = requests.get(url)
data = response.json()
tar='USD'
# Your JSON object
from pprint import pprint
val=data.get('conversion_rates',{}).get(tar)
# pprint(type(data))
print(val)

		