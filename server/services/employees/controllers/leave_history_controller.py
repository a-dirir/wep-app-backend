from server.base.crud_new import CRUDNew


class LeaveHistory(CRUDNew):
    def __init__(self):
        super().__init__('LeaveHistory')
        self.methods = ['create', 'list', 'delete', 'showLinkedServices']

    def on_create(self, data: dict, db):
        emp_no = data.get('emp_no')
        leave_type = data.get('leave_type')
        if emp_no is None or leave_type is None:
            return False, 'emp_no and leave_type are required'

        # check the balance of the employee in leave_balances table
        success, results = db.get(table_name='leave_balances', columns=['leave_remaining'], where_items=[{'emp_no': emp_no,
                                                                                                          'leave_type': leave_type}])
        if not success:
            return False, {'error': results}

        if len(results) == 0:
            return False, f"Employee {emp_no} does not have a leave of type {leave_type}"

        balance = int(results[0]['leave_remaining'])

        leave_days = data.get('leave_days')
        if leave_days is None:
            return False, 'leave_days is required'

        if int(leave_days) > balance:
            return False, f"Employee {emp_no} does not have enough leave balance of type {leave_type}"

        return True, data

    def post_create(self, data: dict, db):
        emp_no = data.get('emp_no')
        leave_type = data.get('leave_type')
        leave_days = data.get('leave_days')

        # get the balance of this employee
        success, results = db.get(table_name='leave_balances', columns=['leave_taken'], where_items=[{'emp_no': emp_no,
                                                                                                      'leave_type': leave_type}])
        if not success:
            return False, results

        leave_taken = results[0]['leave_taken']

        # update the balance
        new_leave_taken = int(leave_taken) + int(leave_days)
        success, results = db.update(table_name='leave_balances', row={'leave_taken': f"{new_leave_taken}"},
                                     where_items=[{'emp_no': emp_no, 'leave_type': leave_type}])
        if not success:
            return False, results

        return True, data

    def post_delete(self, data: list, db):
        data = data[0]
        print(data)
        emp_no = data.get('emp_no')
        leave_type = data.get('leave_type')
        leave_days = data.get('leave_days')

        # get the balance of this employee
        success, results = db.get(table_name='leave_balances', columns=['leave_taken'], where_items=[{'emp_no': emp_no,
                                                                                                      'leave_type': leave_type}])
        if not success:
            return False, results

        leave_taken = results[0]['leave_taken']

        # update the balance
        new_leave_taken = int(leave_taken) - int(leave_days)
        success, results = db.update(table_name='leave_balances', row={'leave_taken': f"{new_leave_taken}"},
                                     where_items=[{'emp_no': emp_no, 'leave_type': leave_type}])
        if not success:
            return False, results

        return True, data
