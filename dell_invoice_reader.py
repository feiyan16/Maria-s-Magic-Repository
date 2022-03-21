import csv
import pdfplumber


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
    csvfile = open('hardware.csv', 'w', newline='', encoding='utf-8')
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['invoice_date', 'invoice_no', 'description', 'price_ea', 'qty', 'tag', 'total'])
    for tg in prod.tags:
        csvwriter.writerow([inv.date,
                            inv.number,
                            prod.description,
                            prod.price,
                            len(prod.tags),
                            tg,
                            inv.total])


if __name__ == '__main__':
    pdf_file = pdfplumber.open('/Users/feiyansu/Desktop/dell_10521931460.pdf')
    invoice = Invoice()
    product = None
    page_0 = pdf_file.pages[0]
    page_0_text = page_0.extract_text().split('\n')
    for i in range(len(page_0_text)):
        item = page_0_text[i]
        if 'Invoice No:' in item:
            invoice.number = item.split()[2]
        if 'Invoice Date:' in item:
            invoice.date = item.split()[2]
        if 'System Service Tags:' in item:
            tokens = page_0_text[i - 1].split()
            while True:
                i += 1
                next_line = page_0_text[i].strip()
                if not next_line:
                    break
                if '-' in next_line.split()[0]:
                    break
                item += next_line
            product = Product(tokens[0], tokens[1:-4], item, tokens[-2])
    page_0_table = page_0.extract_table()
    for row in page_0_table:
        if 'Invoice Total:' in row[0]:
            invoice.total = row[1]
    write_csv(invoice, product)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
