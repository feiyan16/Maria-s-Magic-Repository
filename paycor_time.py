import csv
import sys


class Employee:
    def __init__(self):
        self.name = '-'
        self.badge_no = '0'
        self.location = '-'
        # self.cli_proj_role = []
        self.hours = {'Regular': 0, 'PTO': 0, 'UPT': 0, 'HOL': 0, 'FMLA': 0, 'Jury Duty': 0}
        self.time_off_dates = {'PTO': [], 'UPT': [], 'FMLA': [], 'Jury Duty': [], 'HOL': []}
        self.total_hrs = -1

    def get_dates(self, key):
        if len(self.time_off_dates[key]) == 0:
            return '-'
        if len(self.time_off_dates[key]) == 1:
            return self.time_off_dates[key][0]
        start = self.time_off_dates[key][0]
        end = self.time_off_dates[key][-1]
        return start + ' - ' + end

    def display(self):
        print(self.name)
        print('\t*', self.badge_no)
        print('\t*', self.location)
        print('\t*', self.hours)
        print('\t*', self.time_off_dates)
        print('\t*', self.total_hrs)


class Project:
    def __init__(self, name, roles):
        self.name = name
        self.roles = roles


class Client:
    def __init__(self, name):
        self.name = name
        self.projects = []

    def display(self):
        print(self.name)
        for p in self.projects:
            print('\t*', p.name)
            for r in p.roles:
                print('\t\t-', r + '(s):')
                for res in p.roles[r]:
                    print('\t\t\t*', res)


def read_csv(name):
    print('Opening', name, '...')
    file = open(name)
    print(name, 'successfully opened!')
    print('Reading', name, '...')
    try:
        csv_reader = csv.reader(file)
        h = next(csv_reader)
        r = []
        for row in csv_reader:
            r.append(row)
    except UnicodeDecodeError:
        print('ERROR:', name, 'in wrong encoding format')
        sys.exit(0)
    print(name, 'read successfully!')
    return h, r


def create_employees(data):
    dictionary = {}
    name = ''
    print('Parsing columns: A - D...')
    for row in data:
        e_obj: Employee = Employee()
        if len(row[0].strip()) != 0:
            e_obj.name = row[0].strip()
            e_obj.badge_no = row[1].strip()
            e_obj.location = row[2].strip()
            e_obj.time_off_dates['HOL'].append(row[3].strip())
            dictionary[e_obj.name] = e_obj
    # for row in data:
    #     name = row[0].strip() if len(row[0].strip()) != 0 else name
    #     employee = dictionary[name]
    #     if not row[6].strip() or not row[7].strip() or not row[8].strip():
    #         continue
    #     client = row[6].strip()
    #     project = row[7].strip()
    #     role = row[8].strip()
    #     if (client, project, role) not in employee.cli_proj_role:
    #         employee.cli_proj_role.append((client, project, role))
    print('Parsing columns: S - U...')
    for row in data:
        name = row[0].strip() if len(row[0].strip()) != 0 else name
        e_obj = dictionary[name]
        if not row[18].strip() and not row[20].strip():
            continue
        if 'totals' in row[18].strip().lower():
            try:
                e_obj.total_hrs = float(row[20].strip())
            except ValueError:
                print('ERROR:', row[20].strip(), 'cannot be converted to a float value, string value will be used '
                                                 'instead')
                e_obj.total_hrs = row[20].strip()
            continue
        iu = row[19].strip().split(',')[-1]
        if 'Yes' in iu:
            key = row[18].strip()
            value = row[20].strip()
            try:
                e_obj.hours[key] += float(value)
            except ValueError:
                print('ERROR:', value, 'cannot be added to hour bucket because it cannot be converted to a '
                                       'float')
                sys.exit(0)
            except KeyError:
                print('ERROR:', key, 'does not exist as a key in employee.hours dictionary')
                sys.exit(0)
    print('Parsing columns: X - AC...')
    keys = ['PTO', 'UPT', 'FMLA', 'Jury Duty', 'HOL']
    for row in data:
        name = row[0].strip() if len(row[0].strip()) != 0 else name
        e_obj = dictionary[name]
        if not row[23].strip():
            continue
        date = row[23].strip()
        type_ = row[24].strip()
        if 'Balance' in type_:
            continue
        for i in range(25, len(row)):
            if row[i].strip():
                key = keys[i - 25]
                try:
                    e_obj.time_off_dates[key].append(date)
                except KeyError:
                    print('ERROR:', key, 'does not exist as a key in employee.time_off_dates dictionary')
                    sys.exit(0)
    return dictionary


def create_projects(data):
    dictionary = {}  # project_name : {role1 : [], role2: [], ..., roleN: []}
    res = ''
    print('Parsing columns H - I...')
    for row in data:
        res = row[0].strip() if len(row[0].strip()) != 0 else res
        if not row[7].strip():
            continue
        key = row[7].strip()
        value = row[8].strip()
        if key not in dictionary:
            dictionary[key] = {value: [res]}
        elif value not in dictionary[key]:
            dictionary[key][value] = [res]
        elif res not in dictionary[key][value]:
            dictionary[key][value].append(res)
    return dictionary


def create_clients(data, p_data):
    dictionary = {}
    print('Parsing columns G - H...')
    for row in data:
        if not row[6].strip():
            continue
        key = row[6].strip()
        value = row[7].strip()
        if key not in dictionary:
            dictionary[key] = [value]
        elif value not in dictionary[key]:
            dictionary[key].append(value)
    array = []
    for c_name in dictionary:
        c_obj = Client(c_name)
        array.append(c_obj)
        for p_name in dictionary[c_name]:
            c_obj.projects.append(Project(p_name, p_data[p_name]))
    return array


# fields = ['Clients', 'Projects', 'Resources', 'Regular Hours', 'Date (PTO)', 'Hours (PTO)', ..., 'Total Hours']
def create_rows(c_data, e_data):
    array = []
    for c in c_data:
        show_client = True
        for proj in c.projects:
            show_project = True
            for role in proj.roles:
                for name in proj.roles[role]:
                    resource = e_data[name]
                    row = [name, role, resource.hours['Regular'],
                           resource.get_dates('PTO'), resource.hours['PTO'],
                           resource.get_dates('UPT'), resource.hours['UPT'],
                           resource.get_dates('HOL'), resource.hours['HOL'],
                           resource.get_dates('FMLA'), resource.hours['FMLA'],
                           resource.get_dates('Jury Duty'), resource.hours['Jury Duty'],
                           resource.total_hrs]
                    if show_client and show_project:
                        row.insert(0, proj.name)
                        row.insert(0, c.name)
                        show_client = False
                        show_project = False
                    elif not show_client and show_project:
                        row.insert(0, proj.name)
                        row.insert(0, '')
                        show_project = False
                    else:
                        row.insert(0, '')
                        row.insert(0, '')
                    array.append(row)
    return array


def write_report(name, data):
    csvfile = open(name, 'w')
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['', '', '', '', '',
                        'PTO', '',
                        'UPT', '',
                        'HOL', '',
                        'FMLA', '',
                        'Jury Duty'])
    csvwriter.writerow([
        'Client', 'Project', 'Resource', 'Role', 'Regular',
        'Date', 'Hours',  # PTO
        'Date', 'Hours',  # UPT
        'Date', 'Hours',  # HOL
        'Date', 'Hours',  # FMLA
        'Date', 'Hours',  # Jury Duty
        'Total'
    ])
    csvwriter.writerows(data)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Parameter missing: <filename>')
        sys.exit(0)
    filename = sys.argv[1]
    try:
        print('Trying to parse', filename, '...')
        headers, rows = read_csv(filename)
    except FileNotFoundError:
        print('ERROR:', filename, 'cannot be found')
        sys.exit(0)
    print('Parsing columns to create employees...')
    employees = create_employees(rows)
    print('Employees created successfully!')
    for employee in employees.values():
        employee.display()
    print('Parsing columns to create clients and projects...')
    clients = create_clients(rows, create_projects(rows))
    print('Clients and projects created successfully!')
    for client in clients:
        client.display()
    print('Writing report...')
    write_report('report.csv', create_rows(clients, employees))
    print('Report written successfully!')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
