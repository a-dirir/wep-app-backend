from server.services.monitoring.models.monitoring_models import AlarmsTemplatesModels
from sqlalchemy.orm import Session


class AlarmTemplate:
    def __init__(self):
        pass

    def createTemplate(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation
        customer = payload['access']['customers'][0]
        template_id = f"{customer}:{data['name']}"
        variables = self._extractVariablesFromTemplate(data['template'])
        variables = ','.join(variables)

        with Session(db.engine) as session:
            try:
                template = AlarmsTemplatesModels(
                    id=template_id,
                    name=data['name'],
                    domain=customer,
                    template=data['template'],
                    variables=variables
                )

                session.add(template)
                session.commit()
            except Exception as e:
                print(e)
                return {'error': 'Failed to create Template'}, 400

        return {}, 200

    def getTemplate(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        customer = payload['access']['customers'][0]

        with Session(db.engine) as session:
            try:
                template = session.query(AlarmsTemplatesModels).filter_by(name=data['name'], domain=customer).first().to_dict()
            except Exception as e:
                print(e)
                return {'error': 'Failed to get Template'}, 400

        return template, 200

    def getTemplates(self, payload: dict):
        db = payload['db']

        customer = payload['access']['customers'][0]

        with Session(db.engine) as session:
            try:
                templates = session.query(AlarmsTemplatesModels).filter_by(domain=customer).all()
                templates = [template.to_dict() for template in templates]
            except Exception as e:
                print(e)
                return {'error': 'Failed to get Templates'}, 400

        return templates, 200

    def updateTemplate(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        customer = payload['access']['customers'][0]
        tempate_id = f"{customer}:{data['name']}"

        with Session(db.engine) as session:
            try:
                template = session.query(AlarmsTemplatesModels).filter_by(id=tempate_id).first()
                template.template = data['template']
                variables = self._extractVariablesFromTemplate(data['template'])
                template.variables = ','.join(variables)
                session.commit()
            except Exception as e:
                print(e)
                return {'error': 'Failed to update Template'}, 400

        return {}, 200

    def deleteTemplate(self, payload: dict):
        data = payload['data']
        db = payload['db']

        # add validation

        customer = payload['access']['customers'][0]
        tempate_id = f"{customer}:{data['name']}"

        with Session(db.engine) as session:
            try:
                template = session.query(AlarmsTemplatesModels).filter_by(id=tempate_id).first()
                session.delete(template)
                session.commit()
            except Exception as e:
                print(e)
                return {'error': 'Failed to delete Template'}, 400

        return {}, 200

    def _extractVariablesFromTemplate(self, template: str):
        variables = []
        # extract variables from template between {{ and }}
        for i in range(len(template)-5):
            if template[i] == '{' and template[i+1] == '{':
                variable = ''
                for j in range(i+2, len(template)):
                    if template[j] == '}' and template[j+1] == '}':
                        if variable not in variables:
                            variables.append(variable)
                        break
                    else:
                        variable += template[j]

        return variables

