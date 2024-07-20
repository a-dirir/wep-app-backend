from datetime import datetime
from server.common.crud import CRUD
from server.util import get_logger


class SubClient(CRUD):
    def __init__(self):
        self.name = 'SubClient'
        super().__init__(self.name)
        self.logger = get_logger(f"CRUD_{self.name}")

    @staticmethod
    def get_quarter(date: str):
        # create date object from string
        date = datetime.strptime(date, '%Y-%m-%d')
        quarter = (date.month - 1) // 3 + 1
        return quarter

    def on_create(self, data: dict, db):
        # check if Name is missing
        if data.get('Name') is None:
            return {'error': 'Name is missing'}, 400

        # check if Name is at least 5 characters long
        if len(data['Name']) < 5:
            return {'error': 'Name is too short'}, 400

        # generate Client_ID from by getting first 5 letters from and Name, - and last 4 letters from the Name
        data['Sub_Client_ID'] = data['Name'][:5] + '-' + data['Name'][-4:]

        #  extract year from First_Engagement_Date
        if data.get('First_Engagement_Date') is not None:
            data['First_Engagement_Date'] = data.get('First_Engagement_Date').split('T')[0]
            data['Engagement_Year'] = data['First_Engagement_Date'].split('-')[0]
            data['Engagement_Quarter'] = f"Q{self.get_quarter(data['First_Engagement_Date'])}-{data['Engagement_Year']}"

        return data

    def on_update(self, data: dict, db):
        #  extract year from First_Engagement_Date
        if data.get('First_Engagement_Date') is not None:
            data['First_Engagement_Date'] = data.get('First_Engagement_Date').split('T')[0]
            data['Engagement_Year'] = data['First_Engagement_Date'].split('-')[0]
            data['Engagement_Quarter'] = f"Q{self.get_quarter(data['First_Engagement_Date'])}-{data['Engagement_Year']}"

        return data
