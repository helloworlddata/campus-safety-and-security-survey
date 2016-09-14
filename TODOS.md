- Extract School IDs and meta from e.g. extract_school_meta
- Extract just latest versions of school meta
  + put them into tidied/2014-school-meta
  + Does 2015 have the enrollment for 2014, or for 2015?
- Make one table for which every row has:
  + year, unit_id, school, name, address, enrollment, etc.


- Refactor compile_year
- compile_year should join school_meta and melted tables, currently it just has unit_id and crime counts
