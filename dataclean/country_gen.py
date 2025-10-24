import csv

def select_columns_no_pandas(input_csv, output_csv, columns):
    with open(input_csv, newline="", encoding="utf-8") as f_in:
        reader = csv.DictReader(f_in)
        # Validate columns
        missing = [c for c in columns if c not in (reader.fieldnames or [])]
        if missing:
            raise KeyError(f"Missing columns: {missing}. Available: {reader.fieldnames}")

        with open(output_csv, "w", newline="", encoding="utf-8") as f_out:
            writer = csv.DictWriter(f_out, fieldnames=columns)
            writer.writeheader()
            for row in reader:
                writer.writerow({c: row.get(c, "") for c in columns})

#select_columns_no_pandas("vaccinations.csv","exact_country_in_vaccination.csv",["iso_code","location"])

#select_columns_no_pandas("locations.csv","select_country_from_location.csv",["iso_code","location","source_name","source_website"])

select_columns_no_pandas("vaccinations-by-manufacturer.csv","vaccine_selection.csv",["location","date","vaccine"])
select_columns_no_pandas("merge_csv.csv","merge_select.csv",["location","date","vaccine"])