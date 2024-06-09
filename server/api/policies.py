policies = {
    "admin": {
        "version": "v1",
        "statements": [
            {
                "effect": "allow",
                "actions": ["*"],
                "customers": ["*"],
                "resources": ["*"]
            }
        ]
    },
    "user": {
        "version": "v1",
        "statements": [
            {
                "effect": "allow",
                "actions": ["*"],
                "customers": ["*"],
                "resources": ["*"]
            }
        ]
    }
}
