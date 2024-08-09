from collections import OrderedDict

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
                "index": True, default is False
                "foreign_key": "table_name.column_name", default is ""
                "unique": True, default is False
                "not_null": True, default is False
                "default": "", default is "",
                "allowed_values": ["value1", "value2", ...], default is [],
                "server_only": {'create': False, 'edit': False, 'view': False}, default is False,
            }
        }
    }
}
"""


from collections import OrderedDict

schema = OrderedDict({
    "iam_users": {
        "label": "IAM Users",
        "columns": {
            "email": {
              "type": "VARCHAR(128)",
              "index": True,
              "not_null": True,
              "label": "Email Address"
            },
            "name": {
              "type": "VARCHAR(64)",
              "label": "Full Name"
            },
            "user_group": {
              "type": "VARCHAR(64)",
              "not_null": True,
              "allowed_values": ["user", "admin"],
              "label": "User Group"
            },
            "salt": {
                "type": "VARCHAR(256)",
                "not_null": False,
                "server_only": {'create': True, 'edit': True, 'view': True},
                "label": "Salt"
            },
            "password_hashed": {
                "type": "VARCHAR(256)",
                "not_null": False,
                "server_only": {'create': True, 'edit': True, 'view': True},
                "label": "Hashed Password"
            }
        },
    },
    "clients": {
        "label": "Clients",
        "columns": {
            "Client_ID": {
                "type": "VARCHAR(100)",
                "not_null": True,
                "server_only": {'create': True, 'edit': True, 'view': False},
                "label": "Client ID"
            },
            "Name": {
                "type": "VARCHAR(200)",
                "not_null": True,
                "index": True,
                "label": "Client Name"
            },
        },
    },
    "sub_clients": {
        "label": "Sub Clients",
        "columns": {
            "Sub_Client_ID": {
                "type": "VARCHAR(100)",
                "not_null": True,
                "server_only": {'create': True, 'edit': True, 'view': False},
                "label": "Sub-Client ID"
            },
            "Client_ID": {
                "type": "VARCHAR(100)",
                "foreign_key": "clients.Client_ID|clients.Name",
                "not_null": True,
                "label": "Client ID"
            },
            "Name": {
                "type": "VARCHAR(200)",
                "not_null": True,
                "index": True,
                "label": "Sub-Client Name"
            },
            "Status": {
                "type": "VARCHAR(45)",
                "not_null": True,
                "allowed_values": ["Current", "Terminated"],
                "label": "Status"
            },
            "First_Engagement_Date": {
                "type": "DATE",
                "not_null": True,
                "label": "First Engagement Date"
            },
            "Engagement_Year": {
                "type": "VARCHAR(45)",
                "not_null": True,
                "label": "Engagement Year",
                "server_only": {'create': True, 'edit': True, 'view': False},
            },
            "Engagement_Quarter": {
                "type": "VARCHAR(45)",
                "not_null": True,
                "label": "Engagement Quarter",
                "server_only": {'create': True, 'edit': True, 'view': False},
            },
        }
    },
    "clients_contacts": {
        "label": "Client Contacts",
        "columns": {
            "Sub_Client_ID": {
                "type": "VARCHAR(100)",
                "foreign_key": "sub_clients.Sub_Client_ID|sub_clients.Name",
                "not_null": True,
                "label": "Sub-Client ID"
            },
            "Account_Manager": {
                "type": "VARCHAR(80)",
                "foreign_key": "ms_account_managers.name",
                "not_null": True,
                "label": "Account Manager"
            },
            "MS_Focal_Point": {
                "type": "VARCHAR(80)",
                "foreign_key": "ms_focal_points.name",
                "not_null": True,
                "label": "MS Focal Point"
            },
            "Domain": {
                "type": "VARCHAR(100)",
                "not_null": True,
                "label": "Domain"
            },
            "Contact_Type": {
                "type": "VARCHAR(80)",
                "not_null": True,
                "allowed_values": ["Primary Contact", "Secondary Contact", "Escalation Contact"],
                "index": True,
                "label": "Contact Type"
            },
            "Position": {
                "type": "VARCHAR(80)",
                "not_null": True,
                "label": "Position"
            },
            "Contact_Name": {
                "type": "VARCHAR(120)",
                "not_null": True,
                "index": True,
                "label": "Contact Name"
            },
            "Contact_Email": {
                "type": "VARCHAR(80)",
                "not_null": True,
                "index": True,
                "label": "Contact Email"
            },
            "Contact_Number": {
                "type": "VARCHAR(45)",
                "not_null": True,
                "label": "Contact Number"
            },
        }
    },
    "ms_focal_points": {
        "label": "MS Focal Points",
        "columns": {
            "email": {
              "type": "VARCHAR(128)",
              "index": True,
              "not_null": True,
              "label": "Email Address"
            },
            "name": {
              "type": "VARCHAR(64)",
              "label": "Full Name"
            },
            "title": {
              "type": "VARCHAR(64)",
              "label": "Title"
            },
            "phone_number": {
              "type": "VARCHAR(64)",
              "label": "Phone Number"
            },
        },
    },
    "ms_account_managers": {
        "label": "MS Account Managers",
        "columns": {
            "email": {
              "type": "VARCHAR(128)",
              "index": True,
              "not_null": True,
              "label": "Email Address"
            },
            "name": {
              "type": "VARCHAR(64)",
              "label": "Full Name"
            },
            "title": {
              "type": "VARCHAR(64)",
              "label": "Title"
            },
            "phone_number": {
              "type": "VARCHAR(64)",
              "label": "Phone Number"
            },
        },
    },
    "clients_url": {
        "label": "Clients URL",
        "columns": {
            "Sub_Client_ID": {
                "type": "VARCHAR(100)",
                "foreign_key": "sub_clients.Sub_Client_ID|sub_clients.Name",
                "not_null": True,
                "label": "Sub-Client ID"
            },
            "URL": {
                "type": "VARCHAR(100)",
                "not_null": True,
                "index": True,
                "label": "URL"
            },
            "URL_SSL_Expiry_Date": {
                "type": "VARCHAR(50)",
                "not_null": True,
                "label": "SSL Expiry Date"
            },
        }
    },
    "aws_accounts": {
        "label": "AWS Accounts",
        "columns": {
            "Sub_Client_ID": {
                "type": "VARCHAR(100)",
                "foreign_key": "sub_clients.Sub_Client_ID|sub_clients.Name",
                "not_null": True,
                "label": "Sub-Client ID"
            },
            "Account_ID": {
                "type": "VARCHAR(100)",
                "not_null": True,
                "index": True,
                "label": "Account ID"
            },
            "Name": {
                "type": "VARCHAR(200)",
                "not_null": True,
                "label": "Account Name"
            },
            "Master_Account": {
                "type": "VARCHAR(100)",
                "label": "Master Account"
            },
            "region": {
                "type": "VARCHAR(50)",
                "not_null": True,
                "label": "Region"
            },
        }
    },
    "azure_accounts": {
        "label": "Azure Accounts",
        "columns": {
            "Sub_Client_ID": {
                "type": "VARCHAR(100)",
                "foreign_key": "sub_clients.Sub_Client_ID|sub_clients.Name",
                "not_null": True,
                "label": "Sub-Client ID"
            },
            "Subscription_ID": {
                "type": "VARCHAR(100)",
                "not_null": True,
                "index": True,
                "label": "Subscription ID"
            },
            "Tenant_ID": {
                "type": "VARCHAR(100)",
                "not_null": True,
                "label": "Tenant ID"
            },
            "Name": {
                "type": "VARCHAR(100)",
                "not_null": True,
                "label": "Account Name"
            }
        }
    },
    "m365_accounts": {
        "label": "M365 Accounts",
        "columns": {
            "Sub_Client_ID": {
                "type": "VARCHAR(100)",
                "foreign_key": "sub_clients.Sub_Client_ID",
                "not_null": True,
                "label": "Sub-Client ID"
            },
            "Tenant_ID": {
                "type": "VARCHAR(100)",
                "not_null": True,
                "index": True,
                "label": "Tenant ID"
            },
            "Name": {
                "type": "VARCHAR(200)",
                "not_null": True,
                "label": "Account Name"
            }
        }
    },
    "products": {
        "label": "Products",
        "columns": {
            "Product_ID": {
                "type": "VARCHAR(100)",
                "not_null": True,
                "index": True,
                "label": "Product ID"
            },
            "Name": {
                "type": "VARCHAR(200)",
                "not_null": True,
                "label": "Product Name"
            },
            "Product_Type": {
                "type": "VARCHAR(45)",
                "not_null": True,
                "label": "Product Type"
            }
        }
    },
    "addons": {
        "label": "Addons",
        "columns": {
            "Addon_ID": {
                "type": "VARCHAR(100)",
                "not_null": True,
                "index": True,
                "label": "Addon ID"
            },
            "Name": {
                "type": "VARCHAR(200)",
                "not_null": True,
                "label": "Addon Name"
            },
            "Addon_Type": {
                "type": "VARCHAR(45)",
                "not_null": True,
                "label": "Addon Type"
            }
        }
    },
    "opportunities": {
        "label": "Opportunities",
        "columns": {
            "Opportunity_ID_UQ": {
                "type": "VARCHAR(100)",
                "not_null": True,
                "index": True,
                "label": "Opportunity Unique ID"
            },
            "Opportunity_ID": {
                "type": "VARCHAR(100)",
                "not_null": True,
                "label": "Opportunity ID"
            },
            "Sub_Client_ID": {
                "type": "VARCHAR(100)",
                "foreign_key": "sub_clients.Sub_Client_ID|sub_clients.Name",
                "not_null": True,
                "label": "Sub-Client ID"
            },
            "Status": {
                "type": "VARCHAR(80)",
                "not_null": True,
                "label": "Status",
                "server_only": {'create': True, 'edit': False, 'view': False},
            },
            "Start_Date": {
                "type": "DATE",
                "not_null": True,
                "label": "Start Date"
            },
            "End_Date": {
                "type": "DATE",
                "not_null": True,
                "label": "End Date"
            },
        }
    },
    "aws_opportunity_details": {
        "label": "AWS Opportunity Details",
        "columns": {
            "Opportunity_ID": {
                "type": "VARCHAR(100)",
                "foreign_key": "opportunities.Opportunity_ID",
                "not_null": True,
                "index": True,
                "label": "Opportunity ID"
            },
            "Account_ID": {
                "type": "VARCHAR(100)",
                "foreign_key": "aws_accounts.Account_ID",
                "not_null": True,
                "index": True,
                "label": "Account ID"
            },
            "Product_ID": {
                "type": "VARCHAR(100)",
                "foreign_key": "products.Product_ID|products.Name",
                "not_null": True,
                "label": "Product ID"
            },
            "Addon_ID": {
                "type": "VARCHAR(100)",
                "foreign_key": "addons.Addon_ID|addons.Name",
                "not_null": True,
                "label": "Addon ID"
            },
        }
    },
    "azure_opportunity_details": {
        "label": "Azure Opportunity Details",
        "columns": {
            "Opportunity_ID": {
                "type": "VARCHAR(100)",
                "foreign_key": "opportunities.Opportunity_ID",
                "not_null": True,
                "index": True,
                "label": "Opportunity ID"
            },
            "Subscription_ID": {
                "type": "VARCHAR(100)",
                "foreign_key": "azure_accounts.Subscription_ID",
                "not_null": True,
                "index": True,
                "label": "Subscription ID"
            },
            "Product_ID": {
                "type": "VARCHAR(100)",
                "foreign_key": "products.Product_ID|products.Name",
                "not_null": True,
                "label": "Product ID"
            },
            "Addon_ID": {
                "type": "VARCHAR(100)",
                "foreign_key": "addons.Addon_ID|addons.Name",
                "not_null": True,
                "label": "Addon ID"
            },
        }
    },
    "m365_opportunity_details": {
        "label": "M365 Opportunity Details",
        "columns": {
            "Opportunity_ID": {
                "type": "VARCHAR(100)",
                "foreign_key": "opportunities.Opportunity_ID",
                "not_null": True,
                "index": True,
                "label": "Opportunity ID"
            },
            "Tenant_ID": {
                "type": "VARCHAR(100)",
                "foreign_key": "m365_accounts.Tenant_ID",
                "not_null": True,
                "index": True,
                "label": "Tenant ID"
            },
            "Product_ID": {
                "type": "VARCHAR(100)",
                "foreign_key": "products.Product_ID|products.Name",
                "not_null": True,
                "label": "Product ID"
            },
            "Addon_ID": {
                "type": "VARCHAR(100)",
                "foreign_key": "addons.Addon_ID|addons.Name",
                "not_null": True,
                "label": "Addon ID"
            },
        }
    },
})
