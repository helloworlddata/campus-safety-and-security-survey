"""
For every year:

unit_id,area,year_recorded,year_occurred,topic,category,count
10065401,on_campus,2008,2007,arrests,Drug,18
10065401,on_campus,2008,2005,arrests,Liquor,6
10065401,on_campus,2008,2005,arrests,Weapon,0
10065401,on_campus,2008,2006,arrests,Weapon,2


Grab the most recent year (e.g. 2007) and return:

unit_id,area,year_occurred,drug_arrests,liquor_arrests,weapon_arrests
"""



import yaml
from collections import defaultdict
from csv import DictReader, DictWriter
from loggy import loggy
from pathlib import Path
from sys import stdout

TOPICS = yaml.load(Path('wrangle', 'scripts', 'etc', 'topics.yaml').read_text())
BASE_HEADERS = ['unit_id', 'area', 'year_occurred']
CAT_HEADERS = []
for topic_name, category_maps in TOPICS.items():
    for v in category_maps.values():
        CAT_HEADERS.append(v + '_' + topic_name)

COMPILED_HEADERS = BASE_HEADERS + CAT_HEADERS

LOGGY = loggy('compile_year')

csvout = DictWriter(stdout, fieldnames=COMPILED_HEADERS)
csvout.writeheader()


dirname = Path('wrangle', 'corral', 'tidied')
for year_recorded in (yr for yr in range(2008, 2016)):
    for area in ['on_campus', 'off_campus', 'public_property', 'residence_hall']:

        recent_year = year_recorded - 1

        data = defaultdict(dict) # for each institution id, make a list

        for topic_name, category_maps in TOPICS.items():

            # 2008-off_campus-arrests.csv
            fname = dirname.joinpath("{year}-{area}-{topic}.csv".format(year=year_recorded,area=area,topic=topic_name))
            if fname.exists():
                LOGGY.info("Reading %s" % fname)

                for row in DictReader(fname.open()):
                    # we want just the rows in the most recent year
                    if int(row['year_occurred']) == recent_year:
                        uid = row['unit_id']
                        dt = (recent_year, area, uid)
                        catname = category_maps[row['category'].upper()]
                        ctheader = catname + '_' + topic_name

                        data[dt][ctheader] = row['count']

        for dt, cats in data.items():
            d = cats
            d['year_occurred'] = dt[0]
            d['area'] = dt[1]
            d['unit_id'] = dt[2]
            csvout.writerow(d)

        # HEADERS = TOPICS.items()


