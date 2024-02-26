from server.services.customers.models.contact_model import ContactModel
from server.services.customers.models.sub_client_model import SubClientModel
from sqlalchemy.orm import Session


class Contact:
    def __init__(self):
        pass

    def createContact(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                contact = ContactModel(
                    Sub_Client_ID=data['Sub_Client_ID'],
                    Account_Manager=data['Account_Manager'],
                    MS_Focal_Point=data['MS_Focal_Point'],
                    Domain=data['Domain'],
                    Contact_Type=data['Contact_Type'],
                    Position=data['Position'],
                    Contact_Name=data['Contact_Name'],
                    Contact_Email=data['Contact_Email'],
                    Contact_Number=data['Contact_Number']
                )

                session.add(contact)
                session.commit()
            except Exception as e:
                print(e)
                return {'error': 'Failed to create Contact'}, 400


        return {}, 200

    def getContact(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                contact = session.query(ContactModel).filter_by(Sub_Client_ID=data['Sub_Client_ID'],
                                                                Contact_Name=data['Contact_Name'],
                                                                Contact_Type=data['Contact_Type']
                                                                ).first().to_dict()
            except Exception as e:
                print(e)
                return {'error': 'Failed to get Contact'}, 400


        return contact, 200

    def getContacts(self, payload: dict):
        db = payload['db']

        with Session(db.engine) as session:
            try:
                contacts = session.query(ContactModel).all()
                contacts = [contact.to_dict() for contact in contacts]

                # add sub client name to contact
                for contact in contacts:
                    contact['Sub_Client_Name'] = session.query(SubClientModel).filter_by(Sub_Client_ID=contact['Sub_Client_ID']).first().Name

            except Exception as e:
                print(e)
                return {'error': 'Failed to get Contacts'}, 400

        return contacts, 200

    def updateContact(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                contact = session.query(ContactModel).filter_by(Contact_ID=data['Contact_ID']).first().to_dict()
                print(contact)
                # contact['Sub_Client_ID'] = data['Sub_Client_ID']
                # contact['Account_Manager'] = data['Account_Manager']
                # contact['MS_Focal_Point'] = data['MS_Focal_Point']
                contact['Domain'] = data['Domain']
                # contact['Position'] = data['Position']
                # contact['Contact_Name'] = data['Contact_Name']
                # contact['Contact_Type'] = data['Contact_Type']
                # contact['Contact_Email'] = data['Contact_Email']
                # contact['Contact_Number'] = data['Contact_Number']
                print(contact)
                session.flush()
                session.commit()
            except Exception as e:
                print(e)
                return {'error': 'Failed to update Contact'}, 400

        return {}, 200

    def deleteContact(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        with Session(db.engine) as session:
            try:
                contact = session.query(ContactModel).filter_by(Sub_Client_ID=data['Sub_Client_ID'],
                                                                Contact_Name=data['Contact_Name'],
                                                                Contact_Type=data['Contact_Type']
                                                                ).first().to_dict()

                session.delete(contact)
                session.commit()
            except Exception as e:
                print(e)
                return {'error': 'Failed to delete Contact'}, 400

        return {}, 200




