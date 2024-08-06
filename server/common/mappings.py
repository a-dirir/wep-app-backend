controller_db_mappings = {
    'Customers': {
        'Client': 'clients',
        'SubClient': 'sub_clients',
        'Contact': 'clients_contacts',
        'FocalPoint': 'ms_focal_points',
        'AccountManager': 'ms_account_managers',
        'Synthetic': 'clients_url',
        'AwsAccount': 'aws_accounts',
        'AzureAccount': 'azure_accounts',
        'M365Account': 'm365_accounts',
        'Opportunity': 'opportunities',
        'AwsOpportunity': 'aws_opportunity_details',
        'AzureOpportunity': 'azure_opportunity_details',
        'M365Opportunity': 'm365_opportunity_details',
        'Addon': 'addons',
        'Product': 'products',
    },
    'IAM': {
        'User': 'iam_users'
    },
}