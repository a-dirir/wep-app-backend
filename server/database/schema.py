"""
This file contains the schema of the database. It is used to manage the database tables.
The schema is a dictionary of tables, where each table is a dictionary of columns.
Each column is a dictionary of properties, such as type, primary_key, foreign_key, unique, not_null, and default.
Supported types: INT, VARCHAR, DATE

schema_template = {
    "table_name": {
        "columns":
        {
            "column_name": {
                "type": "type",
                "primary_key": True, default is False
                "foreign_key": "table_name.column_name", default is ""
                "unique": True, default is False
                "not_null": True, default is False
                "default": "", default is "",
                "allowed_values": ["value1", "value2", ...], default is []
            }
        }
    }
}
"""


schema = {
    "iam_api_keys": {
        "columns": {
            "key_id": {
                "type": "VARCHAR(256)",
                "primary_key": True,
                "unique": True,
                "not_null": True
            },
            "key_value": {
                "type": "VARCHAR(512)",
                "unique": True,
                "not_null": True
            },
            "key_group": {
                "type": "VARCHAR(64)",
                "not_null": True
            },
            "key_owner": {
                "type": "VARCHAR(128)",
                "not_null": True
            },
            "key_rate_limit": {
                "type": "INT",
                "not_null": True
            },
            "key_last_time_used": {
              "type": "DATETIME",
              "not_null": True
            },
        },
    },
    "iam_users": {
        "columns": {
            "email": {
              "type": "VARCHAR(128)",
              "primary_key": True,
              "unique": True,
              "not_null": True
            },
            "name": {
              "type": "VARCHAR(64)"
            },
            "group": {
              "type": "VARCHAR(64)",
              "foreign_key": "iam_groups.name",
              "unique": True,
              "not_null": True
            }
        },
    },
    "iam_groups": {
        "columns": {
            "name": {
              "type": "VARCHAR(64)",
              "primary_key": True,
              "unique": True,
              "not_null": True
            },
            "description": {
              "type": "VARCHAR(128)"
            },
            "policy": {
              "type": "VARCHAR(64)",
              "foreign_key": "iam_policies.name",
              "unique": True,
              "not_null": True
            }
        }
    },
    "iam_policies": {
        "columns": {
            "name": {
              "type": "VARCHAR(64)",
              "primary_key": True,
              "unique": True,
              "not_null": True
            },
            "description": {
              "type": "VARCHAR(128)"
            },
            "policy": {
              "type": "JSON",
              "not_null": True
            },
            "expanded_policy": {
              "type": "JSON",
              "not_null": True
            },
        }
    },
    "clients": {
        "columns": {
            "Client_ID": {
                "type": "VARCHAR(100)",
                "primary_key": True,
                "unique": True,
                "not_null": True
            },
            "Name": {
                "type": "VARCHAR(200)",
                "unique": True,
                "not_null": True
            },
        }
    },
    "sub_clients": {
        "columns": {
            "Sub_Client_ID": {
                "type": "VARCHAR(100)",
                "primary_key": True,
                "unique": True,
                "not_null": True
            },
            "Client_ID": {
                "type": "VARCHAR(100)",
                "foreign_key": "clients.Client_ID",
                "not_null": True
            },
            "Name": {
                "type": "VARCHAR(200)",
                "unique": True,
                "not_null": True
            },
            "Status": {
                "type": "VARCHAR(45)",
                "not_null": True,
                "allowed_values": ["Current", "Terminated"]
            },
            "First_Engagement_Date": {
                "type": "DATE",
                "not_null": True
            },
            "Engagement_Year": {
                "type": "VARCHAR(45)",
                "not_null": True,
            },
            "Engagement_Quarter": {
                "type": "VARCHAR(45)",
                "not_null": True,
            },
        }
    }
}
