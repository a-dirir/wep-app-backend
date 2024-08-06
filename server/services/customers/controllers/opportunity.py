from datetime import datetime
from server.common.crud import CRUD
from server.util import get_logger


class Opportunity(CRUD):
    def __init__(self):
        self.name = 'Opportunity'
        super().__init__(self.name)
        self.logger = get_logger(__class__.__name__)
        self.table_name = 'opportunities'

    @staticmethod
    def get_quarter(date:str):
        # create date object from string
        date = datetime.strptime(date, '%Y-%m-%d')

        quarter = (date.month - 1) // 3 + 1
        return quarter

    def on_create(self, data: dict, db):
        # check if Sub_Client_ID is missing
        if data.get('Sub_Client_ID') is None:
            return {'error': 'Sub_Client_Name is missing'}, 400

        conditions = {'Sub_Client_ID': data['Sub_Client_ID']}

        success, results = db.get_rows(table_name=self.table_name, where_items=[conditions])
        if not success:
            return {'error': results}, 400

        if len(results) > 0:
            data['Status'] = "Renewal"
        else:
            data['Status'] = "New"

        data['Start_Date'] = data['Start_Date'].split('T')[0]
        data['End_Date'] = data['End_Date'].split('T')[0]

        return data

    def on_update(self, data: dict, db):
        data['Start_Date'] = data['Start_Date'].split('T')[0]
        data['End_Date'] = data['End_Date'].split('T')[0]

        return data

