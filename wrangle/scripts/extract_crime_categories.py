"""
Converts:

|  UNITID_P |                INSTNM               | BURGLA11 |
|-----------|-------------------------------------|----------|
| 100654001 | Alabama A & M University            |       58 |
| 100663001 | University of Alabama at Birmingham |       11 |


To:

|  unit_id  | area     | category | count | year_occurred   | year_recorded |
|-----------|----------|----------|-------|-----------------|---------------|
| 100654001 | oncampus | BURGLA   |    58 |            2011 |          2013 |
| 100663001 | oncampus | BURGLA   |    11 |            2011 |          2013 |
"""

import argparse
from csv import DictWriter
from loggy import loggy
import re
from sys import stdout
import xlrd

METAHEADER_RX = re.compile(r'(?:^(?:UNITID_P|INSTNM|BRANCH|ADDR|CITY|STATE|ZIP|SECTOR|FILTER))|\w*TOTAL')

OUT_HEADERS = ['unit_id', 'area', 'category', 'count', 'year_occurred', 'year_recorded']



LOGGY = loggy('extract_crime_categories')


def extract_categorical_headers(rawheaders):
    """
    returns a list of strings that refer to categories of crime, not metadata
    ['UNITID_P', 'VEHIC5','ARSON5','MURD6','NEG_M6']
    """
    return [h for h in rawheaders if not METAHEADER_RX.match(h.upper())]



if __name__ == '__main__':
    parser = argparse.ArgumentParser("Reads a spreadsheet, spits out CSV")
    parser.add_argument('infile', type=argparse.FileType('r'))
    args = parser.parse_args()
    infile = args.infile
    xlsname = args.infile.name
    # year of record derived from subdirectory name:
    # wrangle/corral/fetched/Crime2008EXCEL/Oncampuscrime050607.xls
    year_recorded = re.search('(?<=Crime)\d{4}(?=EXCEL)', xlsname).group()
    area = 'TK'

    LOGGY.info('Opening spreadsheet: %s' % xlsname)
    LOGGY.info('Area: %s' % area)
    LOGGY.info('Year of record: %s' % year_recorded)


    book = xlrd.open_workbook(xlsname)
    if book.nsheets > 1:
        LOGGY.warn("Warning: %s sheets found (expecting just 1)" % book.nsheets)

    sheet = book.sheets()[0]
    LOGGY.info("Row count: %s" % sheet.nrows)
    rawheaders = sheet.row_values(0)
    LOGGY.info('Raw header count: %s' % len(rawheaders))
    LOGGY.info(','.join(rawheaders))

    # Get the categorical headers
    catheaders = extract_categorical_headers(rawheaders)
    LOGGY.info('Categorical header count: %s' % len(catheaders))
    LOGGY.info(','.join(catheaders))

    csvout = DictWriter(stdout, fieldnames=OUT_HEADERS)
    csvout.writeheader()

    for n in range(1, sheet.nrows):
        row = dict(zip(rawheaders, sheet.row_values(n)))
        for cat in catheaders:
            value = row[cat]
            d = {
                'area': area,
                'count': value,
                'unit_id': row['UNITID_P'],
                'category': cat,
                'year_recorded': year_recorded,
                'year_occurred': 9999,
            }
            csvout.writerow(d)






