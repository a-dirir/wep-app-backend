from collections import OrderedDict

"""
This file contains the schema of the database. It is used to manage the database tables.
The schema is a dictionary of tables, where each table is a dictionary of columns.
Each column is a dictionary of properties, such as type, index, foreign_key, not_null, and so on.
Any data not updatable, must be an index, but not all indexes are not updatable.

schema_template = {
    "table_name": {
        "columns":
        {
            "column_name": {
                "type": "type", # STRING(128), DATE.
                "label": "label",
                "allowed_values": ["value1", "value2", ...], default is None
                "index": True, default is False, used for indexing. 
                "required": True, default is True
                "foreign_key": "source table_name.column_name | alias table_name.column_name", default is None
                "client_permission": {'create': True, 'update': True, 'view': True}, default is True,
            }
        }
    }
}
"""

# schema_old = OrderedDict({
#     "iam_users": {
#         "label": "IAM Users",
#         "columns": {
#             "email": {
#               "type": "STRING(128)",
#               "index": True,
#               "not_null": True,
#               "label": "Email Address"
#             },
#             "name": {
#               "type": "STRING(64)",
#               "label": "Full Name"
#             },
#             "user_group": {
#               "type": "STRING(64)",
#               "not_null": True,
#               "allowed_values": ["user", "admin"],
#               "label": "User Group"
#             },
#             "salt": {
#                 "type": "STRING(256)",
#                 "not_null": False,
#                 "server_only": {'create': True, 'edit': True, 'view': True},
#                 "label": "Salt"
#             },
#             "password_hashed": {
#                 "type": "STRING(256)",
#                 "not_null": False,
#                 "server_only": {'create': True, 'edit': True, 'view': True},
#                 "label": "Hashed Password"
#             }
#         },
#     },
#     "clients": {
#         "label": "Clients",
#         "columns": {
#             "Client_ID": {
#                 "type": "STRING(100)",
#                 "label": "Client ID",
#                 "index": True,
#                 "client_permission": {'create': False, 'edit': False, 'view': True},
#             },
#             "Name": {
#                 "type": "STRING(200)",
#                 "label": "Client Name",
#                 "index": True,
#             },
#         },
#     },
#     "sub_clients": {
#         "label": "Sub Clients",
#         "columns": {
#             "Sub_Client_ID": {
#                 "type": "STRING(100)",
#                 "label": "Sub-Client ID",
#                 "index": True,
#                 "client_permission": {'create': False, 'edit': False, 'view': True},
#             },
#             "Client_ID": {
#                 "type": "STRING(100)",
#                 "label": "Client ID",
#                 "foreign_key": "clients.Client_ID|clients.Name",
#             },
#             "Name": {
#                 "type": "STRING(200)",
#                 "label": "Sub-Client Name",
#                 "index": True,
#             },
#             "Status": {
#                 "type": "STRING(45)",
#                 "label": "Status",
#                 "allowed_values": ["Current", "Terminated"],
#             },
#             "First_Engagement_Date": {
#                 "type": "DATE",
#                 "label": "First Engagement Date"
#             },
#             "Engagement_Year": {
#                 "type": "STRING(45)",
#                 "label": "Engagement Year",
#                 "client_permission": {'create': False, 'edit': False, 'view': True},
#             },
#             "Engagement_Quarter": {
#                 "type": "STRING(45)",
#                 "label": "Engagement Quarter",
#                 "client_permission": {'create': False, 'edit': False, 'view': True},
#             },
#         }
#     },
#     "clients_contacts": {
#         "label": "Client Contacts",
#         "columns": {
#             "Sub_Client_ID": {
#                 "type": "STRING(100)",
#                 "foreign_key": "sub_clients.Sub_Client_ID|sub_clients.Name",
#                 "not_null": True,
#                 "label": "Sub-Client ID"
#             },
#             "Account_Manager": {
#                 "type": "STRING(80)",
#                 "foreign_key": "ms_account_managers.name",
#                 "not_null": True,
#                 "label": "Account Manager"
#             },
#             "MS_Focal_Point": {
#                 "type": "STRING(80)",
#                 "foreign_key": "ms_focal_points.name",
#                 "not_null": True,
#                 "label": "MS Focal Point"
#             },
#             "Domain": {
#                 "type": "STRING(100)",
#                 "not_null": True,
#                 "label": "Domain"
#             },
#             "Contact_Type": {
#                 "type": "STRING(80)",
#                 "not_null": True,
#                 "allowed_values": ["Primary Contact", "Secondary Contact", "Escalation Contact"],
#                 "index": True,
#                 "label": "Contact Type"
#             },
#             "Position": {
#                 "type": "STRING(80)",
#                 "not_null": True,
#                 "label": "Position"
#             },
#             "Contact_Name": {
#                 "type": "STRING(120)",
#                 "not_null": True,
#                 "index": True,
#                 "label": "Contact Name"
#             },
#             "Contact_Email": {
#                 "type": "STRING(80)",
#                 "not_null": True,
#                 "index": True,
#                 "label": "Contact Email"
#             },
#             "Contact_Number": {
#                 "type": "STRING(45)",
#                 "not_null": True,
#                 "label": "Contact Number"
#             },
#         }
#     },
#     "ms_focal_points": {
#         "label": "MS Focal Points",
#         "columns": {
#             "email": {
#               "type": "STRING(128)",
#               "index": True,
#               "not_null": True,
#               "label": "Email Address"
#             },
#             "name": {
#               "type": "STRING(64)",
#               "label": "Full Name"
#             },
#             "title": {
#               "type": "STRING(64)",
#               "label": "Title"
#             },
#             "phone_number": {
#               "type": "STRING(64)",
#               "label": "Phone Number"
#             },
#         },
#     },
#     "ms_account_managers": {
#         "label": "MS Account Managers",
#         "columns": {
#             "email": {
#               "type": "STRING(128)",
#               "index": True,
#               "not_null": True,
#               "label": "Email Address"
#             },
#             "name": {
#               "type": "STRING(64)",
#               "label": "Full Name"
#             },
#             "title": {
#               "type": "STRING(64)",
#               "label": "Title"
#             },
#             "phone_number": {
#               "type": "STRING(64)",
#               "label": "Phone Number"
#             },
#         },
#     },
#     "clients_url": {
#         "label": "Clients URL",
#         "columns": {
#             "Sub_Client_ID": {
#                 "type": "STRING(100)",
#                 "foreign_key": "sub_clients.Sub_Client_ID|sub_clients.Name",
#                 "not_null": True,
#                 "label": "Sub-Client ID"
#             },
#             "URL": {
#                 "type": "STRING(100)",
#                 "not_null": True,
#                 "index": True,
#                 "label": "URL"
#             },
#             "URL_SSL_Expiry_Date": {
#                 "type": "STRING(50)",
#                 "not_null": True,
#                 "label": "SSL Expiry Date"
#             },
#         }
#     },
#     "aws_accounts": {
#         "label": "AWS Accounts",
#         "columns": {
#             "Sub_Client_ID": {
#                 "type": "STRING(100)",
#                 "foreign_key": "sub_clients.Sub_Client_ID|sub_clients.Name",
#                 "not_null": True,
#                 "label": "Sub-Client ID"
#             },
#             "Account_ID": {
#                 "type": "STRING(100)",
#                 "not_null": True,
#                 "index": True,
#                 "label": "Account ID"
#             },
#             "Name": {
#                 "type": "STRING(200)",
#                 "not_null": True,
#                 "label": "Account Name"
#             },
#             "Master_Account": {
#                 "type": "STRING(100)",
#                 "label": "Master Account"
#             },
#             "region": {
#                 "type": "STRING(50)",
#                 "not_null": True,
#                 "label": "Region"
#             },
#         }
#     },
#     "azure_accounts": {
#         "label": "Azure Accounts",
#         "columns": {
#             "Sub_Client_ID": {
#                 "type": "STRING(100)",
#                 "foreign_key": "sub_clients.Sub_Client_ID|sub_clients.Name",
#                 "not_null": True,
#                 "label": "Sub-Client ID"
#             },
#             "Subscription_ID": {
#                 "type": "STRING(100)",
#                 "not_null": True,
#                 "index": True,
#                 "label": "Subscription ID"
#             },
#             "Tenant_ID": {
#                 "type": "STRING(100)",
#                 "not_null": True,
#                 "label": "Tenant ID"
#             },
#             "Name": {
#                 "type": "STRING(100)",
#                 "not_null": True,
#                 "label": "Account Name"
#             }
#         }
#     },
#     "m365_accounts": {
#         "label": "M365 Accounts",
#         "columns": {
#             "Sub_Client_ID": {
#                 "type": "STRING(100)",
#                 "foreign_key": "sub_clients.Sub_Client_ID",
#                 "not_null": True,
#                 "label": "Sub-Client ID"
#             },
#             "Tenant_ID": {
#                 "type": "STRING(100)",
#                 "not_null": True,
#                 "index": True,
#                 "label": "Tenant ID"
#             },
#             "Name": {
#                 "type": "STRING(200)",
#                 "not_null": True,
#                 "label": "Account Name"
#             }
#         }
#     },
#     "products": {
#         "label": "Products",
#         "columns": {
#             "Product_ID": {
#                 "type": "STRING(100)",
#                 "not_null": True,
#                 "index": True,
#                 "label": "Product ID"
#             },
#             "Name": {
#                 "type": "STRING(200)",
#                 "not_null": True,
#                 "label": "Product Name"
#             },
#             "Product_Type": {
#                 "type": "STRING(45)",
#                 "not_null": True,
#                 "label": "Product Type"
#             }
#         }
#     },
#     "addons": {
#         "label": "Addons",
#         "columns": {
#             "Addon_ID": {
#                 "type": "STRING(100)",
#                 "not_null": True,
#                 "index": True,
#                 "label": "Addon ID"
#             },
#             "Name": {
#                 "type": "STRING(200)",
#                 "not_null": True,
#                 "label": "Addon Name"
#             },
#             "Addon_Type": {
#                 "type": "STRING(45)",
#                 "not_null": True,
#                 "label": "Addon Type"
#             }
#         }
#     },
#     "opportunities": {
#         "label": "Opportunities",
#         "columns": {
#             "Opportunity_ID_UQ": {
#                 "type": "STRING(100)",
#                 "not_null": True,
#                 "index": True,
#                 "label": "Opportunity Unique ID"
#             },
#             "Opportunity_ID": {
#                 "type": "STRING(100)",
#                 "not_null": True,
#                 "label": "Opportunity ID"
#             },
#             "Sub_Client_ID": {
#                 "type": "STRING(100)",
#                 "foreign_key": "sub_clients.Sub_Client_ID|sub_clients.Name",
#                 "not_null": True,
#                 "label": "Sub-Client ID"
#             },
#             "Status": {
#                 "type": "STRING(80)",
#                 "not_null": True,
#                 "label": "Status",
#                 "server_only": {'create': True, 'edit': False, 'view': False},
#             },
#             "Start_Date": {
#                 "type": "DATE",
#                 "not_null": True,
#                 "label": "Start Date"
#             },
#             "End_Date": {
#                 "type": "DATE",
#                 "not_null": True,
#                 "label": "End Date"
#             },
#         }
#     },
#     "aws_opportunity_details": {
#         "label": "AWS Opportunity Details",
#         "columns": {
#             "Opportunity_ID": {
#                 "type": "STRING(100)",
#                 "foreign_key": "opportunities.Opportunity_ID",
#                 "not_null": True,
#                 "index": True,
#                 "label": "Opportunity ID"
#             },
#             "Account_ID": {
#                 "type": "STRING(100)",
#                 "foreign_key": "aws_accounts.Account_ID",
#                 "not_null": True,
#                 "index": True,
#                 "label": "Account ID"
#             },
#             "Product_ID": {
#                 "type": "STRING(100)",
#                 "foreign_key": "products.Product_ID|products.Name",
#                 "not_null": True,
#                 "label": "Product ID"
#             },
#             "Addon_ID": {
#                 "type": "STRING(100)",
#                 "foreign_key": "addons.Addon_ID|addons.Name",
#                 "not_null": True,
#                 "label": "Addon ID"
#             },
#         }
#     },
#     "azure_opportunity_details": {
#         "label": "Azure Opportunity Details",
#         "columns": {
#             "Opportunity_ID": {
#                 "type": "STRING(100)",
#                 "foreign_key": "opportunities.Opportunity_ID",
#                 "not_null": True,
#                 "index": True,
#                 "label": "Opportunity ID"
#             },
#             "Subscription_ID": {
#                 "type": "STRING(100)",
#                 "foreign_key": "azure_accounts.Subscription_ID",
#                 "not_null": True,
#                 "index": True,
#                 "label": "Subscription ID"
#             },
#             "Product_ID": {
#                 "type": "STRING(100)",
#                 "foreign_key": "products.Product_ID|products.Name",
#                 "not_null": True,
#                 "label": "Product ID"
#             },
#             "Addon_ID": {
#                 "type": "STRING(100)",
#                 "foreign_key": "addons.Addon_ID|addons.Name",
#                 "not_null": True,
#                 "label": "Addon ID"
#             },
#         }
#     },
#     "m365_opportunity_details": {
#         "label": "M365 Opportunity Details",
#         "columns": {
#             "Opportunity_ID": {
#                 "type": "STRING(100)",
#                 "foreign_key": "opportunities.Opportunity_ID",
#                 "not_null": True,
#                 "index": True,
#                 "label": "Opportunity ID"
#             },
#             "Tenant_ID": {
#                 "type": "STRING(100)",
#                 "foreign_key": "m365_accounts.Tenant_ID",
#                 "not_null": True,
#                 "index": True,
#                 "label": "Tenant ID"
#             },
#             "Product_ID": {
#                 "type": "STRING(100)",
#                 "foreign_key": "products.Product_ID|products.Name",
#                 "not_null": True,
#                 "label": "Product ID"
#             },
#             "Addon_ID": {
#                 "type": "STRING(100)",
#                 "foreign_key": "addons.Addon_ID|addons.Name",
#                 "not_null": True,
#                 "label": "Addon ID"
#             },
#         }
#     },
# })

schema = OrderedDict({
    "iam_users": {
        "label": "IAM Users",
        "columns": {
            "email": {
              "type": "STRING(128)",
              "index": True,
              "not_null": True,
              "label": "Email Address"
            },
            "name": {
              "type": "STRING(64)",
              "label": "Full Name"
            },
            "user_group": {
              "type": "STRING(64)",
              "not_null": True,
              "allowed_values": ["user", "admin"],
              "label": "User Group"
            },
            "salt": {
                "type": "STRING(256)",
                "not_null": False,
                "server_only": {'create': True, 'edit': True, 'view': True},
                "label": "Salt"
            },
            "password_hashed": {
                "type": "STRING(256)",
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
                "type": "STRING(0,100)",
                "label": "Client ID",
                "index": True,
                "client_permission": {'create': False, 'edit': False, 'view': True},
            },
            "Name": {
                "type": "STRING(0,200)",
                "label": "Client Name",
                "index": True,
            },
        },
        'column_order': ['Client ID', 'Client Name']
    },
    "sub_clients": {
        "label": "Sub Clients",
        "columns": {
            "Sub_Client_ID": {
                "type": "STRING(0,100)",
                "label": "Sub-Client ID",
                "index": True,
                "client_permission": {'create': False, 'edit': False, 'view': True},
            },
            "Client_ID": {
                "type": "STRING(0,100)",
                "label": "Client ID",
                "foreign_key": "clients.Client_ID|clients.Name",
                "foreign_key_alias": "Client Name",
            },
            "Name": {
                "type": "STRING(0,200)",
                "label": "Sub-Client Name",
                "index": True,
            },
            "Status": {
                "type": "STRING(0,45)",
                "label": "Status",
                "allowed_values": ["Current", "Terminated"],
            },
            "First_Engagement_Date": {
                "type": "DATE(DD-MM-YYYY)",
                "label": "First Engagement Date"
            },
            "Engagement_Year": {
                "type": "STRING(0,45)",
                "label": "Engagement Year",
                "client_permission": {'create': False, 'edit': False, 'view': True},
            },
            "Engagement_Quarter": {
                "type": "STRING(0,45)",
                "label": "Engagement Quarter",
                "client_permission": {'create': False, 'edit': False, 'view': True},
            },
        },
        'column_order': ['Client ID', 'Client Name', 'Sub-Client ID', 'Sub-Client Name', 'Status',
                         'First Engagement Date', 'Engagement Year', 'Engagement Quarter']
    }
})

