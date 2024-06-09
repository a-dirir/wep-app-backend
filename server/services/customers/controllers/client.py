from server.common.crud import SimpleCRUD


class Client(SimpleCRUD):
    def __init__(self, table_name: str):
        super().__init__(table_name)

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
