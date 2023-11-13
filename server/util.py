from binascii import hexlify, unhexlify
from time import time
from hashlib import sha256

import requests
import json


def check_authorization(user_policy, controller, method):
    if user_policy['Permissions'].get(controller) is None:
        return False

    if method not in user_policy['Permissions'][controller]:
        return False

    return True


def find_element(element, arr):
    for idx, val in enumerate(arr):
        if val == element:
            return idx
    return -1


def c2s(msg):
    return str(hexlify(msg), encoding='utf8')


def c2b(msg):
    return unhexlify(bytes(msg, encoding='utf8'))


def get_current_time():
    return int(time())


def get_time_difference(given_time):
    return int(given_time - time())


def hash_msg(msg):
    return sha256(msg).digest()


# open customers.csv file and return a list of customers
def get_customers():
    customers = []
    with open('customers.csv', 'r') as f:
        for line in f:
            customers.append(line.strip().split(','))
    headers = {
        'x-ms-client-session-id': 'c846177efd184cba8ef8f7688bbfea70',
        'x-ms-correlation-request-id': 'c7e55348-00d5-4ca1-9be6-76af0e1d683d',
        'Accept-Language': 'en',
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6Ii1LSTNROW5OUjdiUm9meG1lWm9YcWJIWkdldyIsImtpZCI6Ii1LSTNROW5OUjdiUm9meG1lWm9YcWJIWkdldyJ9.eyJhdWQiOiJodHRwczovL21hbmFnZW1lbnQuY29yZS53aW5kb3dzLm5ldC8iLCJpc3MiOiJodHRwczovL3N0cy53aW5kb3dzLm5ldC8wY2VhMGFiNy0yMjM0LTRmNTctYmM4MC00ZDNlNjZkZjQ3OTEvIiwiaWF0IjoxNjk0NTIxOTYzLCJuYmYiOjE2OTQ1MjE5NjMsImV4cCI6MTY5NDUyNjgxNiwiYWNyIjoiMSIsImFpbyI6IkFUUUF5LzhVQUFBQUE5VGZyOFhwSUgvZjVId1l0Rm1OY1o0ZVZBeWhaclh2UEF6ZGVoYzJ5MmUzcmprUk85dDd4QkhDbFRlWnpJWTMiLCJhbXIiOlsicHdkIl0sImFwcGlkIjoiYzQ0YjQwODMtM2JiMC00OWMxLWI0N2QtOTc0ZTUzY2JkZjNjIiwiYXBwaWRhY3IiOiIyIiwiZmFtaWx5X25hbWUiOiJEaXJpciIsImdpdmVuX25hbWUiOiJBaG1lZCIsImdyb3VwcyI6WyJjYjZjNTEyZS05MmNhLTRiNTMtODQxNC00NzhmMzc4MjU5YmQiLCJkYWY1NTYzNS1lMTlhLTQxOWQtYjIxMC1iZTdjZDgyMGNiMzYiLCIzOWYwNWU2Ny1hYWJkLTRjNDItODkwZS00NWVhMGU1MDI1MDUiLCJjOWI5MmI3OS1mNTFhLTQyMDgtODVlYy03YjY3YzJkNmNhYjYiLCJlMGI0ZjM3YS02OGVkLTRiNTAtYTA0Ny01YjY1YjhhZWI1NjIiLCI3OGNhYTVhYi0wYzY5LTRkZTEtODM2ZC01MTBhNTk4MWRlOWEiLCIzZjFhODliMi04ZDE3LTQxNmMtODViZS05YjdiY2IwZDAyZTAiLCIwM2EwMDdkYS0xZTAxLTRiNjQtYWI4Ny1hNGZlOWIzZWZmYjQiLCJmYjkwNGVmZC04ZGFiLTRkNDQtYjIyOS00MDFhOWJhYjczZmUiXSwiaXBhZGRyIjoiMjAwMTo4Zjg6MTE2NTpiZjk6NDVlYTphYjViOmJiM2U6OWEiLCJuYW1lIjoiQWhtZWQgRGlyaXIiLCJvaWQiOiIzN2JlYjQzZS02OTAxLTRlMTQtOGQ4Mi0xNWJkZmI1ZDZlZTYiLCJwdWlkIjoiMTAwMzIwMDIwQkRBNEE0NyIsInJoIjoiMC5BVHdBdHdycUREUWlWMC04Z0UwLVp0OUhrVVpJZjNrQXV0ZFB1a1Bhd2ZqMk1CTThBTlEuIiwic2NwIjoidXNlcl9pbXBlcnNvbmF0aW9uIiwic3ViIjoiSDRSbEp5Y0c3ajJUTHoyenE5dGl1QkJWR0g1TXNXU0lwMmtLcUlhNS0wcyIsInRpZCI6IjBjZWEwYWI3LTIyMzQtNGY1Ny1iYzgwLTRkM2U2NmRmNDc5MSIsInVuaXF1ZV9uYW1lIjoiYWhtZWQuZGlyaXJAYmVzcGluZ2xvYmFsLmFlIiwidXBuIjoiYWhtZWQuZGlyaXJAYmVzcGluZ2xvYmFsLmFlIiwidXRpIjoiNnhyN19ybXk3RUtHTWlKcDI0eFlBQSIsInZlciI6IjEuMCIsInhtc190Y2R0IjoxNTc0MjU1NjA1fQ.a4wM8q7x9OBS4g9diMXIoFhvHpMhmpOn4U6Aa0HnzKZlwy-ME9FddGHqLw4FDGF26puXPo2uhegG9KSbZM2WMKvVlzcGiq_GrrDpA92DBYbjUy-LMrGOfF8QOBEFlDvE3qNOKBMIn0x_A2QFN-cOD3MAFCMqUm-sRHXzPplP9D-49KzQQaBGIJZ4bMtW-5Ukx18RqVLQ6Mw8RI5_hBo4_Ya6j7kk51Zd4wZkLCBaJwte273f6HY7bpezfcvrulM1diVNnaO1MDu2R3NEmE8u6x_XB9Ovjxy3S4CXl4f9NwLul-zncuRrYxCWdzUHxgJcSYFwmSieR_mnuc-LL2D2lQ',
        'x-ms-tracking-id': 'c7e55348-00d5-4ca1-9be6-76af0e1d683d',
        'x-ms-effective-locale': 'en.en-gb',
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'Referer': '',
        'x-ms-client-request-id': 'e5eb0f56-4a96-477d-ad15-9a8421c6d013',
        'user-id': '204b13c6d7588e00ab54e20cc8ca71f42c8dd363308f25332fa30e5935accbb8',
        'user-type': 'apikey'
    }
    for customer in customers:
        print(customer)
        # send request to get customer info
        payload = json.dumps({
            "access": {
                "action": "IAM:Customer:createCustomer",
                "customers": [
                    "*"
                ],
                "resources": [
                    "*"
                ]
            },
            "data": {
                "id": customer[0],
                "name": customer[0],
                "config": {
                    "opsnowid": customer[1]
                },
            }
        })
        r = requests.post(f'http://127.0.0.1:8080/', data=payload, headers=headers)
        print(r.status_code)

print(get_customers())





