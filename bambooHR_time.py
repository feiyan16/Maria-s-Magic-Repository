import sys
import csv


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def stdout(text):
    return input(f"{Colors.OKBLUE}{text}{Colors.ENDC}")


def stdok(text):
    print(f"{Colors.OKGREEN}{Colors.BOLD}{text}{Colors.ENDC}")


def stdwarn(text):
    print(f"{Colors.WARNING}\tWARNING: {text}...{Colors.ENDC}")


def stderr(text):
    print(f"{Colors.FAIL}{Colors.BOLD}ERROR: {text}!{Colors.ENDC}")


class Time:
    def __init__(self, date, hr, note):
        self.date = date
        self.hrs = hr
        self.note = note


class Employee:
    def __init__(self, emp_no, name):
        self.emp_no = emp_no.strip()
        self.name = name.strip()
        self.time_off = {'PTO': [], 'FMLA': [], 'UPT': [], 'Jury Duty': [], 'Comp Off': [], 'Holiday': []}
        self.billable = {}  # entry.billable[proj] = {task: [Time(date, tot_hrs, note)]}
        self.regular = 0
        self.total = -1

    def get_billable(self, project, task):
        total = 0
        for time in self.billable[project][task]:
            total += time.hrs
        return total

    def get_time_off_hrs(self, key):
        total = 0
        for time in self.time_off[key]:
            total += time.hrs
        return total

    def get_time_off_dates(self, key):
        dates = ''
        for time in self.time_off[key]:
            dates += (time.date + '; ')
        if not dates:
            return '--'
        return dates

    def display(self):
        print(self.name, '-', self.emp_no)
        print('\tRegular:', self.regular, 'hrs')
        print('\tTotal:', self.total, 'hrs')
        for key in self.time_off:
            print('\t*', key)
            for time in self.time_off[key]:
                print('\t\t~', time.date)
                print('\t\t ', time.hrs, 'hrs')
                print('\t\t ', time.note)
        for key in self.billable:
            print('\t' + key)
            for task in self.billable[key]:
                print('\t\t*', task)
                for time in self.billable[key][task]:
                    print('\t\t\t~', time.date)
                    print('\t\t\t ', time.hrs, 'hrs')
                    print('\t\t\t ', time.note)


def read_csv(filename):
    try:
        print('Opening', filename, '...')
        file = open(filename)
    except FileNotFoundError as error:
        stderr(error)
        sys.exit(0)
    stdok(filename + ' opened successfully!')
    try:
        print('Reading', filename, '...')
        csv_reader = csv.reader(file)
        print('Reading headers...')
        h = next(csv_reader)
        r = []
        print('Reading rows...')
        for row in csv_reader:
            r.append(row)
    except UnicodeDecodeError as error:
        stderr(error)
        sys.exit(0)
    stdok(filename + ' reading completed!')
    return h, r


def validate_hrs(hr):
    if '--' not in hr:
        return float(hr)
    else:
        stdwarn('This row has no hour, replacing hour value with 0')
        return 0


def validate_proj(proj):
    if not proj:
        stdwarn('This row has no project, replacing project value with Loyalty-Methods Internal')
        return 'Loyalty-Methods Internal'
    return proj


def validate_task(task):
    if not task:
        stdwarn('This row has no task, replacing task value with <No Task>')
        return '<No Task>'
    return task


def create_employees(data):
    entry_list = {}
    print('Parsing employees...')
    for i in range(len(data)):
        row = data[i]
        print(f'PARSING ROW {i}: ', row, '...')
        emp_no = row[0].strip()
        name = row[1].strip()
        date = row[2].strip()
        clk_in = row[3].strip()
        clk_out = row[4].strip()
        tot_hrs = validate_hrs(row[5].strip())
        proj = validate_proj(row[6].strip())
        task = validate_task(row[7].strip())
        note = row[8].strip() if row[8].strip() else '--'
        if emp_no in entry_list:
            entry = entry_list.get(emp_no)
        else:
            entry = Employee(emp_no, name)
            stdok(f'CREATED: {str(entry)} - EMP_NO.: {emp_no}')
            entry_list[emp_no] = entry
        if not date and not clk_in and not clk_out:
            entry.total = tot_hrs
            continue
        if clk_in in entry.time_off.keys() and clk_out in entry.time_off.keys():
            time = Time(date, tot_hrs, note)
            entry.time_off[clk_in].append(time)
            continue
        if proj in entry.billable:
            project = entry.billable[proj]
            if task in project:
                project[task].append(Time(date, tot_hrs, note))
            else:
                project[task] = [Time(date, tot_hrs, note)]
        else:
            entry.billable[proj] = {task: [Time(date, tot_hrs, note)]}
        entry.regular += tot_hrs
    return entry_list


def create_clients(data):
    print('Creating clients...')
    dictionary = {}  # {client: {proj1: {task1: [], ..., taskN: []}, ..., projN: {task1: [], ..., taskN: []}}, ...}
    for e in data:
        employee = data.get(e)
        emp_no = employee.emp_no
        projects = employee.billable
        for project in projects:
            client = project.split(' ')[0]
            if client not in dictionary:
                dictionary[client] = {}
        for project in projects:
            client = project.split(' ')[0]
            if project not in dictionary[client]:
                dictionary[client][project] = {}
        for project in projects:
            client = project.split(' ')[0]
            tasks = projects[project].keys()
            for task in tasks:
                if task not in dictionary[client][project]:
                    dictionary[client][project][task] = [emp_no]
                else:
                    dictionary[client][project][task].append(emp_no)
    return dictionary


def create_rows(c_data, e_data):
    print('Creating rows for report...')
    array = []
    for client in c_data:
        show_client = True
        for project in c_data[client]:
            show_project = True
            for task in c_data[client][project]:
                for emp_no in c_data[client][project][task]:
                    emp = e_data[emp_no]
                    # {'PTO': [], 'FMLA': [], 'UPT': [], 'Jury Duty': [], 'Comp Off': [], 'Holiday': []}
                    row = [task, emp.name, emp.get_billable(project, task),
                           emp.get_time_off_hrs('PTO'), emp.get_time_off_dates('PTO'),
                           emp.get_time_off_hrs('FMLA'), emp.get_time_off_dates('FMLA'),
                           emp.get_time_off_hrs('UPT'), emp.get_time_off_dates('UPT'),
                           emp.get_time_off_hrs('Jury Duty'), emp.get_time_off_dates('Jury Duty'),
                           emp.get_time_off_hrs('Comp Off'), emp.get_time_off_dates('Comp Off'),
                           emp.get_time_off_hrs('Holiday'), emp.get_time_off_dates('Holiday'),
                           emp.total]
                    if show_client and show_project:
                        row.insert(0, project)
                        row.insert(0, client)
                        show_client = False
                        show_project = False
                    elif not show_client and show_project:
                        row.insert(0, project)
                        row.insert(0, '')
                        show_project = False
                    else:
                        row.insert(0, '')
                        row.insert(0, '')
                    array.append(row)
    return array


def write_report(name, data):
    print('Writing Report...')
    csvfile = open(name, 'w')
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['', '', '', '', '',
                        'PTO', '',
                        'FMLA', '',
                        'UPT', '',
                        'Jury Duty', '',
                        'Comp Off', '',
                        'Holiday'])
    csvwriter.writerow([
        'Client', 'Project', 'Role', 'Resource', 'Billable',
        'Hours', 'Date',  # PTO
        'Hours', 'Date',  #
        'Hours', 'Date',  #
        'Hours', 'Date',  #
        'Hours', 'Date',  #
        'Hours', 'Date',  #
        'Total'
    ])
    csvwriter.writerows(data)
    stdok(f'Report written successfully as {name}')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if len(sys.argv) < 2:
        stderr('Parameter missing: <timesheet file>')
        sys.exit(0)
    timesheet = sys.argv[1]
    headers, rows = read_csv(timesheet)
    employees = create_employees(rows)
    stdok('Employees parsed successfully!\n')
    if 'y' in stdout('Would you like to view employees? (y/n)').strip().lower():
        for item in employees:
            employees.get(item).display()
    print()
    clients = create_clients(employees)
    stdok('Clients created successfully!\n')
    rows = create_rows(clients, employees)
    stdok('Rows created successfully!\n')
    if 'y' in stdout('Would you like to view rows? (y/n)').strip().lower():
        for item in rows:
            print(item)
    print()
    write_report('report.csv', rows)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
