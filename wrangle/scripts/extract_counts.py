"""
Converts: Crime2013EXCEL/oncampuscrime101112.xls

|  UNITID_P |                INSTNM               | BURGLA11 |
|-----------|-------------------------------------|----------|
| 100654001 | Alabama A & M University            |       58 |
| 100663001 | University of Alabama at Birmingham |       11 |


To:

|  unit_id  | area      | topic  | category | count | year_occurred   | year_recorded |
|-----------|-----------|--------|----------|-------|-----------------|---------------|
| 100654001 | on_campus | crimes | BURGLA   |    58 |            2011 |          2013 |
| 100663001 | on_campus | crimes | BURGLA   |    11 |            2011 |          2013 |
"""

import argparse
from csv import DictWriter
from loggy import loggy
import re
from sys import stdout, stderr
import xlrd

METAHEADER_RX = re.compile(r'(?:^(?:UNITID_P|INSTNM|BRANCH|ADDR|CITY|STATE|ZIP|SECTOR|FILTER))|\w*TOTAL')

EXTRACTED_HEADERS = ['unit_id', 'area', 'year_recorded', 'year_occurred',
                   'topic', 'category', 'count']



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
    # expect the user to manually provide area, year_recorded, topic
    parser.add_argument('--year-recorded', type=str, required=True,
        help="e.g. 2013 from Crime2013EXCEL/")
    parser.add_argument('--area', type=str, required=True,
        help="e.g. on_campus from oncampuscrime10111213.xls")
    parser.add_argument('--topic', type=str, required=True,
        help="e.g. crimes from oncampuscrime10111213.xls")

    args = parser.parse_args()
    infile = args.infile
    year_recorded = args.year_recorded
    area = args.area
    topic = args.topic
    LOGGY.info('Year of record: %s' % year_recorded)
    LOGGY.info('Area: %s' % area)
    LOGGY.info('Topic: %s' % topic)


    xlsname = args.infile.name
    LOGGY.info('Opening spreadsheet: %s' % xlsname)
    book = xlrd.open_workbook(xlsname, logfile=stderr)

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




    data = []
    for n in range(1, sheet.nrows):
        rowvals = [int(c.value) if c.ctype == 2 else c.value for c in sheet.row(n)]
        row = dict(zip(rawheaders, rowvals))

        for cathead in catheaders:
            category, yr = re.match('(\w+?)(\d+)$', cathead).groups()
            occyear = 2000 + int(yr)
            cellval = row[cathead]
            d = {
                'area': area,
                'topic': topic,
                'year_recorded': year_recorded,
                'count': cellval,
                'unit_id': row['UNITID_P'],
                'category': category,
                'year_occurred': occyear,
            }
            data.append(d)

    LOGGY.info("Number of datums: %s" % len(data))
    csvout = DictWriter(stdout, fieldnames=EXTRACTED_HEADERS)
    csvout.writeheader()

    csvout.writerows(sorted(data, key=lambda x: (x['unit_id'], x['category'], x['year_occurred'])))






