import requests

api_key = '579b464db66ec23bdd000001bd9ca6b688414f3d691f5cd8bc1b84cd'
url = 'https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070'

# Test with exact commodity name from sample record
r = requests.get(url, params={
    'api-key': api_key,
    'format': 'json',
    'limit': 3,
    'filters[commodity]': 'Tomato',
}, timeout=10)

import json
data = r.json()
print('Total:', data.get('total'))
print('Records:', len(data.get('records', [])))
if data.get('records'):
    print('Sample:', data['records'][0])

# Also test with lowercase filter
r2 = requests.get(url, params={
    'api-key': api_key,
    'format': 'json',
    'limit': 3,
    'filters[Commodity]': 'Tomato',
}, timeout=10)
data2 = r2.json()
print('Capital filter - Total:', data2.get('total'))
print('Capital filter - Records:', len(data2.get('records', [])))