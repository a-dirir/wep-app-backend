import os
import time
import requests
import json


class OpsNowConnector:
    def __init__(self):
        self.access_token_dev = self.get_access_token()
        # self.current_company = self.get_current_user()['result']['curCmpnId']

    def get_access_token(self):
        token = os.getenv('OPSNOW_ACCESS_TOKEN')

        return token

    def get_company_list(self):
        url = "https://service.opsnow.me/api_v2.0/authgroup/companyList/portal"

        payload = {}

        headers = {
            'authority': 'service.opsnow.me',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
            'authorization': f"Bearer {self.access_token_dev}",
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'pragma': 'no-cache',
            'referer': 'https://service.opsnow.me/dashboard',
            'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        }

        response = requests.request("GET", url, headers=headers, data=payload, allow_redirects=False)

        if response.status_code == 200:
            result = response.json()
            return result
        else:
            return None

    def get_current_user(self):
        url = "https://service.opsnow.me/api_v2.0/users/current-logged-in"

        payload = {}

        headers = {
            'authority': 'service.opsnow.me',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-GB,en;q=0.7',
            'authorization': f"Bearer {self.access_token_dev}",
            'content-type': 'application/json',
            'origin': 'https://asset.opsnow.me',
            'referer': 'https://asset.opsnow.me/',
            'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Brave";v="116"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        }

        response = requests.request("GET", url, headers=headers, data=payload, allow_redirects=False)

        if response.status_code == 200:
            return response.json()
        else:
            return None

    def set_current_company(self, company_id):
        self.current_company = company_id

        url = "https://service.opsnow.me/api_v2.0/users/current/company"

        payload = json.dumps({"curCmpnId": company_id})

        headers = {
            'authority': 'service.opsnow.me',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
            'authorization': f"Bearer {self.access_token_dev}",
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'origin': 'https://service.opsnow.me',
            'pragma': 'no-cache',
            'referer': 'https://service.opsnow.me/dashboard',
            'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        }

        response = requests.request("PUT", url, headers=headers, data=payload, allow_redirects=False)

        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_usage(self):
        url = "https://api.opsnow.me/asset/api_v2.0/elastic/filter/usage"
        current_date = time.strftime("%Y-%m-%d")
        date_14_days_ago = time.strftime("%Y-%m-%d", time.localtime(time.time() - 60 * 60 * 24 * 14))

        payload = json.dumps({
            "cmpnId": self.current_company,
            "keyList": [],
            "from": date_14_days_ago,
            "to": current_date,
            "periodType": "day",
            "actionType": "current",
            "keyTypes": []
        })

        headers = {
            'authority': 'api.opsnow.me',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
            'authorization': f"Bearer {self.access_token_dev}",
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'origin': 'https://asset.opsnow.me',
            'pragma': 'no-cache',
            'referer': 'https://asset.opsnow.me/',
            'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        }

        response = requests.request("PUT", url, headers=headers, data=payload, allow_redirects=False)

        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_resources_list(self, provider: str = 'aws'):
        url = "https://api.opsnow.me/asset/api_v2.0/rsrcInfoList"

        payload = json.dumps({
            "option": "usage",
            "prodTblNm": "TASM_CLOUD_PROD_L",
            "prvrCd": provider
        })

        headers = {
            'authority': 'api.opsnow.me',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
            'authorization': f"Bearer {self.access_token_dev}",
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'origin': 'https://asset.opsnow.me',
            'pragma': 'no-cache',
            'referer': 'https://asset.opsnow.me/',
            'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        }

        response = requests.request("POST", url, headers=headers, data=payload, allow_redirects=False)

        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_resource_usage(self, resource_id: str, provider: str = 'aws'):
        url = "https://api.opsnow.me/asset/api_v2.0/usage/aws/grid/current"

        payload = json.dumps({
            "cmpnId": self.current_company,
            "rsrcType": resource_id,
            "pageNum": 1,
            "limitCnt": 1000,
            "sortColId": "",
            "sortDirection": "ASC",
            "prvrCd": provider,
            "isGetHeader": "Y",
            "searchText": "",
            "accounts": [],
            "regions": [],
            "svcGrps": [],
            "tags": [],
            "langCd": "en",
            "excelYn": "N"
        })

        headers = {
            'authority': 'api.opsnow.me',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
            'authorization': f"Bearer {self.access_token_dev}",
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'origin': 'https://asset.opsnow.me',
            'pragma': 'no-cache',
            'referer': 'https://asset.opsnow.me/',
            'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        }

        response = requests.request("POST", url, headers=headers, data=payload, allow_redirects=False)

        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_total_user_product_aws(self, aws_account: list):
        url = "https://api.opsnow.me/asset/api_v2.0/dashboard/totaluseproduct"

        payload = json.dumps({
            "siteCd": "BGMEA",
            "cmpnId": self.current_company,
            "aws": "Y",
            "awsAccount": aws_account,
            "azure": None,
            "azuAccount": None,
            "ali": None,
            "aliAccount": None,
            "gcp": None,
            "gcpAccount": None,
            "ncp": None,
            "ncpAccount": None,
            "tencent": None,
            "tencentAccount": None,
            "oci": None,
            "ociAccount": None,
            "openstack": None,
            "openstackAccount": None
        })

        headers = {
            'authority': 'api.opsnow.me',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
            'authorization': f"Bearer {self.access_token_dev}",
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'origin': 'https://asset.opsnow.me',
            'pragma': 'no-cache',
            'referer': 'https://asset.opsnow.me/',
            'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        }

        response = requests.request("POST", url, headers=headers, data=payload, allow_redirects=False)

        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_total_user_product_azure(self, azure_account: list):
        url = "https://api.opsnow.me/asset/api_v2.0/dashboard/totaluseproduct"

        payload = json.dumps({
            "siteCd": "BGMEA",
            "cmpnId": self.current_company,
            "aws": None,
            "awsAccount": None,
            "azure": "Y",
            "azuAccount": azure_account,
            "ali": None,
            "aliAccount": None,
            "gcp": None,
            "gcpAccount": None,
            "ncp": None,
            "ncpAccount": None,
            "tencent": None,
            "tencentAccount": None,
            "oci": None,
            "ociAccount": None,
            "openstack": None,
            "openstackAccount": None
        })

        headers = {
            'authority': 'api.opsnow.me',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9,ar;q=0.8',
            'authorization': f"Bearer {self.access_token_dev}",
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'origin': 'https://asset.opsnow.me',
            'pragma': 'no-cache',
            'referer': 'https://asset.opsnow.me/',
            'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        }

        response = requests.request("POST", url, headers=headers, data=payload, allow_redirects=False)

        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_cost_summary(self, vendor, month,  year=2023):

        url = "https://metering.opsnow.me/MAZ/v3/user/billing/bill/main/summary"

        before_month = (month - 1) if month > 1 else 12
        before_year = year if month > 1 else (year - 1)

        if before_month < 10:
            before_month = f"0{before_month}"
        else:
            before_month = str(before_month)

        # append 0 if month is less than 10
        if month < 10:
            current_month = f"0{month}"
        else:
            current_month = str(month)
        payload = json.dumps({
            "siteId": "BGMEA",
            "vendor": vendor,
            "cmpnId": self.current_company,
            "userId": "2f9407ce-f24d-443c-93a6-eae016c7cc44",
            "chrgYear": year,
            "chrgMnth": current_month,
            "bfYear": before_year,
            "bfMnth": before_month
        })

        headers = {
            'authority': 'metering.opsnow.me',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-GB,en;q=0.9',
            'authorization': f"Bearer {self.access_token_dev}",
            'content-type': 'application/json',
            'origin': 'https://metering.opsnow.me',
            'referer': 'https://metering.opsnow.me/billing',
            'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Brave";v="116"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
        }

        response = requests.request("POST", url, headers=headers, data=payload, allow_redirects=False)

        if response.status_code == 200:
            return response.json()
        else:
            return None


