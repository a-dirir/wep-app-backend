from server.common.crud_new import CRUDNew
from server.util import get_logger


class Client(CRUDNew):
    def __init__(self):
        self.name = 'Client'
        super().__init__(self.name)
        self.logger = get_logger(__class__.__name__)

    def on_create(self, data: dict, db):
        # check if Name is missing
        if data.get('Name') is None:
            return {'error': 'Name is missing'}, 400

        # check if Name is at least 5 characters long
        if len(data['Name']) < 5:
            return {'error': 'Name is too short'}, 400

        # generate Client_ID from by getting first 5 letters from and Name, - and last 4 letters from the Name
        data['Client_ID'] = data['Name'][:5] + '-' + data['Name'][-4:]

        return data
