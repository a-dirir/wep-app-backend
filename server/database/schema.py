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
            "user_group": {
              "type": "VARCHAR(64)",
              "unique": True,
              "not_null": True,
              "allowed_values": ["user", "admin"]
            },
            "salt": {
                "type": "VARCHAR(256)",
                "not_null": True
            },
            "password_hashed": {
                "type": "VARCHAR(64)",
                "not_null": True
            }
        },
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
    },
    "clients_contacts": {
        "columns": {
            "Sub_Client_ID": {
                "type": "VARCHAR(100)",
                "foreign_key": "sub_clients.Sub_Client_ID",
                "not_null": True
            },
            "Account_Manager": {
                "type": "VARCHAR(80)",
                "not_null": True
            },
            "MS_Focal_Point": {
                "type": "VARCHAR(80)",
                "not_null": True
            },
            "Domain": {
                "type": "VARCHAR(100)",
                "not_null": True
            },
            "Contact_Type": {
                "type": "VARCHAR(80)",
                "not_null": True
            },
            "Position": {
                "type": "VARCHAR(80)",
                "not_null": True
            },
            "Contact_Name": {
                "type": "VARCHAR(120)",
                "not_null": True
            },
            "Contact_Email": {
                "type": "VARCHAR(80)",
                "not_null": True
            },
            "Contact_Number": {
                "type": "VARCHAR(45)",
                "not_null": True
            },
            "Contact_ID": {
                "type": "INT",
                "primary_key": True,
                "not_null": True
            },
        }
    },
    "clients_url": {
        "columns": {
            "Sub_Client_ID": {
                "type": "VARCHAR(100)",
                "foreign_key": "sub_clients.Sub_Client_ID",
                "not_null": True
            },
            "URL": {
                "type": "VARCHAR(100)",
                "primary_key": True,
                "not_null": True
            },
            "URL_SSL_Expiry_Date": {
                "type": "VARCHAR(50)",
                "not_null": True
            },
        }
    },
    "aws_accounts": {
        "columns": {
            "Sub_Client_ID": {
                "type": "VARCHAR(100)",
                "foreign_key": "sub_clients.Sub_Client_ID",
                "not_null": True
            },
            "Account_ID": {
                "type": "VARCHAR(100)",
                "primary_key": True,
                "not_null": True
            },
            "Name": {
                "type": "VARCHAR(200)",
                "not_null": True
            },
            "Master_Account": {
                "type": "VARCHAR(100)",
                "not_null": True,
            },
            "region": {
                "type": "VARCHAR(50)",
                "not_null": True,
            },
        }
    },
    "azure_accounts": {
        "columns": {
            "Sub_Client_ID": {
                "type": "VARCHAR(100)",
                "foreign_key": "sub_clients.Sub_Client_ID",
                "not_null": True
            },
            "Subscription_ID": {
                "type": "VARCHAR(100)",
                "primary_key": True,
                "not_null": True
            },
            "Tenant_ID": {
                "type": "VARCHAR(100)",
                "not_null": True
            },
            "Name": {
                "type": "VARCHAR(100)",
                "not_null": True,
            }
        }
    },
    "m365_accounts": {
        "columns": {
            "Sub_Client_ID": {
                "type": "VARCHAR(100)",
                "foreign_key": "sub_clients.Sub_Client_ID",
                "not_null": True
            },
            "Tenant_ID": {
                "type": "VARCHAR(100)",
                "primary_key": True,
                "not_null": True
            },
            "Name": {
                "type": "VARCHAR(200)",
                "not_null": True
            }
        }
    },
    "products": {
        "columns": {
            "Product_ID": {
                "type": "VARCHAR(100)",
                "primary_key": True,
                "not_null": True
            },
            "Name": {
                "type": "VARCHAR(200)",
                "not_null": True
            },
            "Product_Type": {
                "type": "VARCHAR(45)",
                "not_null": True,
            }
        }
    },
    "addons": {
        "columns": {
            "Addon_ID": {
                "type": "VARCHAR(100)",
                "primary_key": True,
                "not_null": True
            },
            "Name": {
                "type": "VARCHAR(200)",
                "not_null": True
            },
            "Addon_Type": {
                "type": "VARCHAR(45)",
                "not_null": True,
            }
        }
    },
    "opportunities": {
        "columns": {
            "Opportunity_ID_UQ": {
                "type": "VARCHAR(100)",
                "primary_key": True,
                "not_null": True
            },
            "Opportunity_ID": {
                "type": "VARCHAR(100)",
                "primary_key": True,
                "not_null": True
            },
            "Sub_Client_ID": {
                "type": "VARCHAR(100)",
                "foreign_key": "sub_clients.Sub_Client_ID",
                "not_null": True
            },
            "Status": {
                "type": "VARCHAR(80)",
                "not_null": True,
            },
            "Start_Date": {
                "type": "DATE",
                "not_null": True
            },
            "End_Date": {
                "type": "DATE",
                "not_null": True
            },
        }
    },
    "aws_opportunity_details": {
        "columns": {
            "Opportunity_ID": {
                "type": "VARCHAR(100)",
                "primary_key": True,
                "foreign_key": "opportunities.Opportunity_ID",
                "not_null": True
            },
            "Account_ID": {
                "type": "VARCHAR(100)",
                "foreign_key": "aws_accounts.Account_ID",
                "not_null": True
            },
            "Product_ID": {
                "type": "VARCHAR(100)",
                "foreign_key": "products.Product_ID",
                "not_null": True
            },
            "Addon_ID": {
                "type": "VARCHAR(100)",
                "foreign_key": "addons.Addon_ID",
                "not_null": True
            },
        }
    },
    "azure_opportunity_details": {
        "columns": {
            "Opportunity_ID": {
                "type": "VARCHAR(100)",
                "primary_key": True,
                "foreign_key": "opportunities.Opportunity_ID",
                "not_null": True
            },
            "Subscription_ID": {
                "type": "VARCHAR(100)",
                "foreign_key": "azure_accounts.Subscription_ID",
                "not_null": True
            },
            "Product_ID": {
                "type": "VARCHAR(100)",
                "foreign_key": "products.Product_ID",
                "not_null": True
            },
            "Addon_ID": {
                "type": "VARCHAR(100)",
                "foreign_key": "addons.Addon_ID",
                "not_null": True
            },
        }
    },
    "m365_opportunity_details": {
        "columns": {
            "Opportunity_ID": {
                "type": "VARCHAR(100)",
                "primary_key": True,
                "foreign_key": "opportunities.Opportunity_ID",
                "not_null": True
            },
            "Tenant_ID": {
                "type": "VARCHAR(100)",
                "foreign_key": "m365_accounts.Tenant_ID",
                "not_null": True
            },
            "Product_ID": {
                "type": "VARCHAR(100)",
                "foreign_key": "products.Product_ID",
                "not_null": True
            },
            "Addon_ID": {
                "type": "VARCHAR(100)",
                "foreign_key": "addons.Addon_ID",
                "not_null": True
            },
        }
    }
}
