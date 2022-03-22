import csv
import pdfplumber
import sys

from pdfminer.pdfparser import PDFSyntaxError

import sys_color as write


class Invoice:
    def __init__(self):
        self.number = ''
        self.date = ''
        self.total = ''


class Product:
    def __init__(self, number, description, tags, price):
        self.number = number
        self.description = ''
        for tok in description:
            self.description += (tok + ' ')
        self.tags = [x.strip() for x in tags.split(':')[1].split(', ')]
        self.price = price


def write_csv(inv, prod):
    csvfile = open('hardware.csv', 'a', newline='', encoding='utf-8')
    csvwriter = csv.writer(csvfile)
    for tg in prod.tags:
        row = [inv.date,
               inv.number,
               prod.description,
               prod.price,
               len(prod.tags),
               tg,
               inv.total]
        csvwriter.writerow(row)
        print(f'{row} written...')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        write.stderr('Parameter missing: <timesheet file>')
        sys.exit(0)
    pdf_name = sys.argv[1]
    print('Opening', pdf_name)
    try:
        pdf_file = pdfplumber.open(pdf_name)
    except FileNotFoundError as error:
        write.stderr(error)
        sys.exit(0)
    except PDFSyntaxError as error:
        write.stderr(error)
        sys.exit(0)
    invoice = Invoice()
    product = None
    for n in range(len(pdf_file.pages)):
        print(f'Parsing page {n + 1} of {len(pdf_file.pages)}')
        page_n = pdf_file.pages[n]
        page_n_text = page_n.extract_text().split('\n')
        for i in range(len(page_n_text)):
            item = page_n_text[i]
            if 'Invoice No:' in item:
                number = item.split()[2]
                if number != invoice.number:  # A new invoice is found
                    write.stdok('New invoice found:')
                    invoice = Invoice()  # create a new invoice
                    invoice.number = number  # assign it its new number
                    write.stdok(f'\tNumber: {number}')
                else:
                    continue
            if 'Invoice Date:' in item:
                date = item.split()[2]
                if date != invoice.date:
                    invoice.date = date
                    write.stdok(f'\tDate: {date}')
                else:
                    continue
            if 'System Service Tags:' in item:
                tokens = page_n_text[i - 1].split()
                write.stdok(f'New product found in Invoice {invoice.number}:')
                while True:
                    i += 1
                    next_line = page_n_text[i].strip()
                    if not next_line:
                        break
                    if '-' in next_line.split()[0]:
                        break
                    item += next_line
                product = Product(tokens[0], tokens[1:-4], item, tokens[-2])
                write.stdok(f'\t- {product.number}\n\t- {product.description}\n\t- {product.tags}\n\t- ${product.price}')
        page_0_table = page_n.extract_table()
        if not page_0_table:
            continue
        for entry in page_0_table:
            if 'Invoice Total:' in entry[0]:
                invoice.total = entry[1]
                write.stdok(f'Total for invoice {invoice.number} found: {invoice.total}')
        print(f'Writing invoice {invoice.number} to csv file...')
        write_csv(invoice, product)
    write.stdok('File written successfully as hardware.csv!')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
