import shodan
import time
import requests
import re

SHODAN_API_KEY = 'enter api key'
api = shodan.Shodan(SHODAN_API_KEY)


# print(api.search(query='product:nginx', facets='country,org'))


def request_page_from_shodan(query, page=1):
    while True:
        try:
            instances = api.search(query, page=page)
            return instances
        except shodan.APIError as e:
            print(f"Error: {e}")
            time.sleep(5)


def query_shodan(query):
    print("[*] querying the first page")
    first_page = request_page_from_shodan(query)
    total = first_page['total']
    already_processed = len(first_page['matches'])
    result = process_page(first_page)
    page = 2
    while already_processed < total:
        # break just in your testing, API queries have monthly limits
        break
    print("querying page {page}")
    page = request_page_from_shodan(query, page=page)
    already_processed += len(page['matches'])
    result += process_page(page)
    page += 1
    return result


#
#
def process_page(page):
    result = []
    for instance in page['matches']:
        # if has_valid_credentials(instance):
        print(f"[+] valid credentials at : {instance['ip_str']}:{instance['port']}")
        result.append(instance)
    return result


res = query_shodan('title:dvwa')
print(res)
