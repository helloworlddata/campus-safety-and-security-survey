"""
Converts:

|  UNITID_P |                INSTNM               | BURGLA11 |
|-----------|-------------------------------------|----------|
| 100654001 | Alabama A & M University            |       58 |
| 100663001 | University of Alabama at Birmingham |       11 |


To:

|  unit_id  | area     | category | count | year_occurrence | year_reported |
|-----------|----------|----------|-------|-----------------|---------------|
| 100654001 | oncampus | BURGLA   |    58 |            2011 |          2013 |
| 100663001 | oncampus | BURGLA   |    11 |            2011 |          2013 |
"""
