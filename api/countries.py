from http.server import BaseHTTPRequestHandler
from urllib import parse
import requests

class handler(BaseHTTPRequestHandler):
 
    def do_GET(self):
        # Parse query parameters
        path = self.path
        url_components = parse.urlparse(path)
        query_params = parse.parse_qs(url_components.query)

        # Initialize the response
        response = ''

        # Check to see if country parameter is in the query
        if 'country' in query_params:
            
            # Get the first value for 'country'
            country = query_params['country'][0]  
           
            # Make a request to the REST Countries API
            api_response = requests.get(f'https://restcountries.com/v3.1/name/{country}')
            
            if api_response.status_code == 200:
                # Assuming the first result is the most relevant
                country_info = api_response.json()[0]  
                capital = country_info['capital'][0] if 'capital' in country_info else 'No capital found.'
                response = f'The capital of {country} is {capital}.'
            
            else:
                response = f'Country not found: {country}.'

        # Check to see if capital parameter is in the query
        elif 'capital' in query_params:
            
            # Get the first value for 'capital'
            capital = query_params['capital'][0] 
            
            # Make a request to the REST Countries API by capital
            api_response = requests.get(f'https://restcountries.com/v3.1/capital/{capital}')
            
            if api_response.status_code == 200:
                country_info = api_response.json()[0] 
                country = country_info['name']['common']
                response = f'{capital} is the capital of {country}.'
            else:
                response = f'No country found with capital: {capital}.'

        else:
            response = 'Invalid query. Please specify a country or a capital.'

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(response.encode())