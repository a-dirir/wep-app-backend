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
                "index": True, default is False, used for indexing. 
                "required": True, default is True
                "foreign_key": "source table_name.column_name | alias table_name.column_name", default is None
                "client_permission": {'create': True, 'update': True, 'view': True}, default is True,
            }
        }
    }
}
"""

schema = OrderedDict({
    "iam_users": {
        "label": "IAM Users",
        "columns": {
            "email": {
              "type": "STRING(10,128)",
              "index": True,
              "label": "Email Address"
            },
            "name": {
              "type": "STRING(10,64)",
              "label": "Full Name"
            },
            "user_group": {
              "type": "STRING(4,64)",
              "label": "User Group"
            },
            "salt": {
                "type": "STRING(0,256)",
                "client_permission": {'create': False, 'update': False, 'view': False},
                "label": "Salt"
            },
            "password_hashed": {
                "type": "STRING(0,256)",
                "client_permission": {'create': False, 'update': False, 'view': False},
                "label": "Hashed Password"
            }
        },
    },
    "employees": {
        "label": "Employees",
        "columns": {
            "emp_no": {
                "type": "INT",
                "index": True,
                "label": "Employee Number",
                "client_permission": {'create': False, 'update': False, 'view': True}
            },
            "birth_date": {
                "type": "DATE",
                "label": "Birth Date"
            },
            "name": {
                "type": "STRING(45)",
                "label": "Employee Name"
            },
            "gender": {
                "type": "ENUM('M', 'F')",
                "label": "Employee Gender"
            },
            "hire_date": {
                "type": "DATE",
                "label": "Hire Date"
            }
        }
    },
    "departments": {
        "label": "Departments",
        "columns": {
            "dept_no": {
                "type": "STRING(4)",
                "label": "Department Number",
                "index": True,
                "client_permission": {'create': False, 'update': False, 'view': True}
            },
            "dept_name": {
                "type": "STRING(40)",
                "label": "Department Name",
            }
        }
    },
    "dept_manager": {
        "label": "Department Managers",
        "columns": {
            "dept_no": {
                "type": "CHAR(4)",
                "label": "Department Number",
                "index": True,
                "foreign_key": "departments.dept_no|departments.dept_name",
                "foreign_key_alias": "Department Name",
            },
            "emp_no": {
                "type": "INT",
                "label": "Employee Number",
                "index": True,
                "foreign_key": "employees.emp_no|employees.name",
                "foreign_key_alias": "Employee Name",
            },
            "from_date": {
                "type": "DATE",
                "label": "Start Date"
            },
            "to_date": {
                "type": "DATE",
                "label": "End Date"
            }
        }
    },
    "dept_emp": {
        "label": "Department Employees",
        "columns": {
            "emp_no": {
                "type": "INT",
                "label": "Employee Number",
                "index": True,
                "foreign_key": "employees.emp_no|employees.name",
                "foreign_key_alias": "Employee Name",
            },
            "dept_no": {
                "type": "CHAR(4)",
                "label": "Department Number",
                "index": True,
                "foreign_key": "departments.dept_no|departments.dept_name",
                "foreign_key_alias": "Department Name",
            },
            "from_date": {
                "type": "DATE",
                "label": "Start Date"
            },
            "to_date": {
                "type": "DATE",
                "label": "End Date"
            }
        }
    },
    "titles": {
        "label": "Titles",
        "columns": {
            "emp_no": {
                "type": "INT",
                "label": "Employee Number",
                "index": True,
                "foreign_key": "employees.emp_no|employees.name",
                "foreign_key_alias": "Employee Name",
            },
            "title": {
                "type": "STRING(50)",
                "label": "Title"
            },
            "from_date": {
                "type": "DATE",
                "label": "STart Date"
            },
            "to_date": {
                "type": "DATE",
                "label": "End Date"
            }
        }
    },
    "salaries": {
        "label": "Salaries",
        "columns": {
            "emp_no": {
                "type": "INT",
                "label": "Employee Number",
                "index": True,
                "foreign_key": "employees.emp_no|employees.name",
                "foreign_key_alias": "Employee Name",
            },
            "salary": {
                "type": "INT",
                "label": "Salary"
            },
            "from_date": {
                "type": "DATE",
                "label": "Start Date"
            },
            "to_date": {
                "type": "DATE",
                "label": "End Date"
            }
        }
    },
    "leave_balances": {
        "label": "Leave Balances",
        "columns": {
            "emp_no": {
                "type": "INT",
                "label": "Employee Number",
                "index": True,
                "foreign_key": "employees.emp_no|employees.name",
                "foreign_key_alias": "Employee Name",
            },
            "leave_type": {
                "type": "ENUM('Sick Leave', 'Annual Leave')",
                "label": "Leave Type"
            },
            "total_leave": {
                "type": "INT",
                "label": "Total Leave",
                "client_permission": {'create': True, 'update': False, 'view': True}
            },
            "leave_taken": {
                "type": "INT",
                "label": "Leave Taken",
                "client_permission": {'create': False, 'update': False, 'view': True}
            },
            "leave_remaining": {
                "type": "INT",
                "label": "Leave Remaining",
                "client_permission": {'create': False, 'update': False, 'view': True}
            }
        }
    },
    "leave_history": {
        "label": "Leave History",
        "columns": {
            "leave_id": {
                "type": "INT",
                "index": True,
                "label": "Leave ID",
                "client_permission": {'create': False, 'update': False, 'view': True}
            },
            "emp_no": {
                "type": "INT",
                "label": "Employee Number",
                "index": True,
                "foreign_key": "employees.emp_no|employees.name",
                "foreign_key_alias": "Employee Name",
            },
            "leave_type": {
                "type": "ENUM('Sick Leave', 'Annual Leave')",
                "label": "Leave Type"
            },
            "leave_start_date": {
                "type": "DATE",
                "label": "Leave Start Date"
            },
            "leave_end_date": {
                "type": "DATE",
                "label": "Leave End Date"
            },
            "leave_days": {
                "type": "INT",
                "not_null": True,
                "label": "Leave Days"
            },
            "reason": {
                "type": "STRING(255)",
                "label": "Reason"
            }
        }
    },
    "tasks": {
        "label": "Tasks",
        "columns": {
            "task_id": {
                "type": "INT",
                "index": True,
                "label": "Task ID",
                "client_permission": {'create': False, 'update': False, 'view': True}
            },
            "emp_no": {
                "type": "INT",
                "label": "Employee Number",
                "index": True,
                "foreign_key": "employees.emp_no|employees.name",
                "foreign_key_alias": "Employee Name",
            },
            "assigned_by": {
                "type": "INT",
                "label": "Assigned By",
                "index": True,
                "foreign_key": "employees.emp_no|employees.name",
                "foreign_key_alias": "Assigner Name",
            },
            "task_description": {
                "type": "STRING(255)",
                "label": "Task Description"
            },
            "deadline": {
                "type": "DATE",
                "label": "Deadline"
            },
            "status": {
                "type": "ENUM('Pending', 'In Progress', 'Completed')",
                "label": "Status"
            }
        }
    },
    "task_history": {
        "label": "Task History",
        "columns": {
            "history_id": {
                "type": "INT",
                "index": True,
                "label": "History ID",
                "client_permission": {'create': False, 'update': False, 'view': True}
            },
            "task_id": {
                "type": "INT",
                "label": "Task ID",
                "index": True,
                "foreign_key": "tasks.task_id|tasks.task_description",
                "foreign_key_alias": "Task Description",
            },
            "emp_no": {
                "type": "INT",
                "label": "Employee Number",
                "index": True,
                "foreign_key": "employees.emp_no|employees.name",
                "foreign_key_alias": "Employee Name",
            },
            "evaluation_date": {
                "type": "DATE",
                "label": "Evaluation Date"
            },
            "evaluation_score": {
                "type": "INT",
                "label": "Evaluation Score",
            },
            "comments": {
                "type": "STRING(255)",
                "label": "Comments"
            }
        }
    }
})


