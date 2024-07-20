from os import getenv
import requests


class NewRelicAgent:
    def __init__(self):
        self.url = getenv('NEW_RELIC_URL')
        self.api_key = getenv('NEW_RELIC_API_KEY')

    def run(self, query):
        headers = {
            'API-Key': self.api_key,
            'Content-Type': 'application/json'
        }

        json_data = {
            'query': query,
        }

        response = requests.post(self.url, headers=headers, json=json_data)

        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_accounts(self):
        query = """
            {
              actor {
                accounts(scope: GLOBAL) {
                  id
                  name
                }
              }
            }
        """

        results = self.run(query)
        if results is None:
            return

        accounts = results['data']['actor']['accounts']

        return accounts

    def get_policies(self, account_id: str):
        query = f"""
        {{
          actor {{
            account(id: {account_id}) {{
              alerts {{
                policiesSearch {{
                  policies {{
                    id
                    name
                  }}
                }}
              }}
            }}
          }}
        }}
        """

        results = self.run(query)
        if results is None:
            return

        policies = results['data']['actor']['account']['alerts']['policiesSearch']['policies']

        return policies

    def get_all_alerts_conditions(self, account_id: str, policy_id: str):
        query = f"""
            {{
              actor {{
                account(id: {account_id}) {{
                  alerts {{
                    nrqlConditionsSearch(searchCriteria: {{policyId: "{policy_id}"}}) {{
                      nrqlConditions {{
                        name
                        nrql {{
                          query
                        }}
                        enabled
                        id
                      }}
                      totalCount

                    }}
                  }}
                }}
              }}
            }}
        """
        results = self.run(query)
        if results is None:
            return

        alert_conditions = results['data']['actor']['account']['alerts']['nrqlConditionsSearch']['nrqlConditions']

        return alert_conditions

    def get_alert_condition_details(self, account_id: str, condition_id: str):
        query = f"""
            {{
              actor {{
                account(id: {account_id}) {{
                  alerts {{
                    nrqlCondition(id: "{condition_id}") {{
                      enabled
                      id
                      name
                      nrql {{
                        query
                      }}
                      terms {{
                        operator
                        priority
                        threshold
                        thresholdDuration
                        thresholdOccurrences
                      }}
                    }}
                  }}
                }}
              }}
            }}
        """
        results = self.run(query)
        if results is None:
            return

        nrql_condition = results['data']['actor']['account']['alerts']['nrqlCondition']

        return nrql_condition

    def get_cloud_providers(self, account_id: str):
        query = f"""
            {{
              actor {{
                account(id: {account_id}) {{
                  cloud {{
                    providers {{
                      id
                      name
                      services {{
                        id
                        name
                      }}
                    }}
                  }}
                }}
              }}
            }}
        """
        results = self.run(query)
        if results is None:
            return

        cloud_providers = results['data']['actor']['account']['cloud']['providers']

        return cloud_providers

    def get_ai_issues(self, account_id: str, start_time: int, end_time: int):
        query = f"""
            {{
              actor {{
                account(id: {account_id}) {{
                  aiIssues {{
                    issues(
                      timeWindow: {{startTime: {start_time}, endTime: {end_time}}}
                      filter: {{states: ACTIVATED}}
                    ) {{
                      issues {{
                        title
                        origins
                        policyIds
                        entityNames
                        conditionName
                        issueId
                        priority
                        createdAt
                        description
                        state
                      }}
                    }}
                  }}
                }}
              }}
            }}
        """
        results = self.run(query)
        if results is None:
            return

        ai_issues = results['data']['actor']['account']['aiIssues']['issues']['issues']

        return ai_issues

    def get_ai_incidents(self, account_id: str, start_time: int, end_time: int):
        query = f"""
            {{
              actor {{
                account(id: {account_id}) {{
                  aiIssues {{
                    incidents(
                    timeWindow: {{startTime: {start_time}, endTime: {end_time}}}
                    filter: {{states: CREATED}}
                    ) {{
                      incidents {{
                        title
                        entityNames
                        state
                        priority
                        timestamp
                        description
                        createdAt
                        updatedAt
                      }}
                    }}
                  }}
                }}
              }}
            }}
        """
        results = self.run(query)
        if results is None:
            return

        ai_incidents = results['data']['actor']['account']['aiIssues']['incidents']['incidents']

        return ai_incidents

    def get_alert_incidents(self, account_id: str):
        account_id = int(account_id)
        query = f"""
              {{
                actor {{
                  account(id: {account_id}) {{
                    aiIssues {{
                      incidents(
                      filter: {{states: CREATED}}
                      ) {{
                        incidents {{
                          title
                          entityNames
                          entityGuids
                          description
                          createdAt
                          updatedAt
                          incidentId
                        }}
                      }}
                    }}
                  }}
                }}
              }}
          """
        results = self.run(query)
        if results is None:
            return

        ai_incidents = results['data']['actor']['account']['aiIssues']['incidents']['incidents']

        return ai_incidents

