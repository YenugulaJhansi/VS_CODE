class Employee:
    def __init__(self, username, employee_id, manager_id, active=True):
    
        self.username = username
        self.employee_id = employee_id
        self.manager_id = manager_id
        self.active = active

    def get_management_chain(self, employees_dict):
        
        chain = [self.username]
        current_manager_id = self.manager_id

        while current_manager_id:
            manager = employees_dict.get(current_manager_id)
            if manager:
                chain.append(manager.username)
                current_manager_id = manager.manager_id
            else:
                break

        return " -> ".join(reversed(chain))


def parse_employee_data(file_path):
    
    employees = {}

    with open(file_path, 'r') as file:
        employee_data = {}
        for line in file:
            line = line.strip()

            if line == "##############":  # Indicates the end of one employee record
                if employee_data:
                    # Extract employee data and create Employee object
                    username = employee_data.get("username")
                    employee_id = int(employee_data.get("employeeid"))
                    manager_id = int(employee_data.get("managerid")) if employee_data.get("managerid") != employee_data.get("employeeid") else None
                    active = employee_data.get("employeestatus") == "Active"

                    employees[employee_id] = Employee(username, employee_id, manager_id, active)
                    employee_data = {}  # Reset for next employee

            elif line:  # Parse key-value pairs
                key, value = line.split(": ")
                employee_data[key.lower()] = value.strip()

    return employees


def print_active_employee_chains(employees):

    for employee in employees.values():
        if employee.active:
            print(f"{employee.username} -> {employee.get_management_chain(employees)}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python parse_ldap.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    
    employees = parse_employee_data(file_path)


    print_active_employee_chains(employees)
