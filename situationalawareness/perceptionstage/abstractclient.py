from abc import ABC, abstractmethod
from urllib3.util.url import Url
from requests.exceptions import HTTPError
import requests
import sys

class AbstractClient(ABC):
    def __init__(self, clientURL: Url):
        self.shutdownURL = clientURL.url+'/shutdown'
        super().__init__()

    def getShutdownURL(self):
        return self.shutdownURL

    def setShutdownURL(self, url):
        self.shutdownURL = url

    def restfulGet(self, url):
        response = requests.get(url)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
        return response.json()

    def shutdownService(self):
        requests.post(self.getShutdownURL())

'''
    def restfulGet(self, url):
        exceptRaised = False
        try:
            response = requests.get(url)
            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            exceptRaised = True
            # print("Could not connect to '"+url+"'", end=' ')
        except HTTPError as http_err:
            exceptRaised = True
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            exceptRaised = True
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            return response.json()
        finally:
            if exceptRaised:
                print("\nSystem exiting.")
                sys.exit(1)
'''

