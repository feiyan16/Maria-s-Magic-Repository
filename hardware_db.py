import csv
import json

import sys_color as write


class History:
    def __init__(self, name, loc, loan, ret):
        self.name = name.strip() if name.strip() else 'N/A'
        self.loc = loc.strip() if loc.strip() else 'N/A'
        self.loan = loan.strip() if loan.strip() else 'N/A'
        self.ret = ret.strip() if ret.strip() else 'N/A'

    def __str__(self):
        return f'name: {self.name},' \
               f'location: {self.loc},' \
               f'loan_date: {self.loan},' \
               f'return_date: {self.ret}'


class Hardware:
    def __init__(self, invoice_date, invoice_no, item, serial, _type, price, out_date):
        self.invoice_date = invoice_date.strip() if invoice_date.strip() else 'N/A'
        self.invoice_no = invoice_no.strip() if invoice_no.strip() else 'N/A'
        self.item = item.strip() if item.strip() else 'N/A'
        self.serial = serial.strip() if serial.strip() else 'N/A'
        self.type_ = _type.strip() if _type.strip() else 'N/A'
        self.price = price.strip() if price.strip() else 'N/A'
        self.out_date = out_date.strip() if out_date.strip() else 'N/A'
        self.history = []

    def __str__(self):
        return f'invoice_date: {self.invoice_date}, '\
               f'invoice_no: {self.invoice_no}, ' \
               f'item: {self.item}, ' \
               f'serial: {self.serial}, ' \
               f'type: {self.type_}, ' \
               f'price: {self.price}, ' \
               f'out of service: {self.out_date}, ' \
               f'history: {self.history}'

    def add_history(self, row):
        self.history.append(History(row[0], row[-3], row[-2], row[-1]))


class File:
    def __init__(self, table, name):
        self.name = name
        self.rows = []
        self.columns = {}
        headers = next(table)
        for row in table:
            self.rows.append(row)
            for i in range(len(row)):
                h = headers[i].upper().strip()
                if h not in self.columns:
                    self.columns[h] = [row[i]]
                else:
                    self.columns.get(h).append(row[i])

    def shape(self):
        return f'( rows: {len(self.rows)}, columns: {len(self.columns)} )'

    def get_row(self, i):
        return self.rows[i]

    def get_col(self, i):
        header = list(self.columns.keys())[i].upper()
        return self.columns.get(header)

    def get(self, r, c):
        header = list(self.columns.keys())[c].upper()
        column = self.columns.get(header)
        return column[r]


class Files:
    EXPENSES_LAPTOPS = File(csv.reader(open('expenses_laptops.csv', 'r')), 'expenses_laptops.csv')
    EXPENSES_MONITORS = File(csv.reader(open('expenses_monitors.csv', 'r')), 'expenses_monitors.csv')
    LAPTOPS = File(csv.reader(open('laptops.csv', 'r')), 'laptops.csv')
    MONITORS = File(csv.reader(open('monitors.csv', 'r')), 'monitors.csv')

    all = [EXPENSES_LAPTOPS, EXPENSES_MONITORS, LAPTOPS, MONITORS]

    def display(self):
        write.stdund('Files'.upper())
        for i in range(len(self.all)):
            file = self.all[i]
            print(f'{i + 1} - {file.name}')
        print('\n')


FILES = Files()


def create_hardware_dict(hardware_s):
    hardware_json = {"hardware": []}
    for hardware in hardware_s.values():
        historical = []
        for hist in hardware.history:
            historical.append({
                "name": hist.name,
                "location": hist.loc,
                "loan date": hist.loan,
                "return date": hist.ret
            })
        x = {
            "invoice date": hardware.invoice_date,
            "invoice no": hardware.invoice_no,
            "item": hardware.item,
            "serial": hardware.serial,
            "type": hardware.type_,
            "price": hardware.price,
            "out of service": hardware.out_date,
            "history": historical
        }
        hardware_json["hardware"].append(x)
    return hardware_json


def add_hardware(dictionary, file):
    for line in file.rows:
        # key = (line[1].strip(), line[6].strip())
        key = line[5].strip()
        if line and key:
            if key not in dictionary:
                # invoice_no, item, serial, _type, price, out_date
                dictionary[key] = Hardware(line[0], line[1], line[2], line[5], line[-1], line[3], line[-2])
            else:
                write.stdwarn(f'Duplicate hardware - {key}')
                print(f'\t\tORIGINAL - {dictionary.get(key)}')
                print(f'\t\tDUPLICATE - {line}')
                ans = write.stdin('Would you like to replace the original with the duplicate? (y/n): ')
                if 'y' in ans.lower():
                    dictionary[key] = Hardware(line[0], line[1], line[2], line[5], line[-1], line[3], line[-2])
                else:
                    continue


def make_history(file, dictionary):
    for line in file.rows:
        key = line[3].strip()
        if not key:
            continue
        try:
            hardware = dictionary[key]
        except KeyError:
            continue
        hardware.add_history(line)


if __name__ == '__main__':
    all_hardware = {}
    add_hardware(all_hardware, FILES.EXPENSES_LAPTOPS)
    add_hardware(all_hardware, FILES.EXPENSES_MONITORS)

    make_history(FILES.LAPTOPS, all_hardware)
    make_history(FILES.MONITORS, all_hardware)

    hardware_file = open('hardware.json', 'w')
    hardware_file.write(json.dumps(create_hardware_dict(all_hardware), indent=4))
