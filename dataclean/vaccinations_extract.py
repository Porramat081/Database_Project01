import csv
import os
import tempfile

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

def add_right_constant_column_no_pandas(input_csv, output_csv, new_col_name="url", value=""):
    with open(input_csv, newline="", encoding="utf-8") as f_in, \
         open(output_csv, "w", newline="", encoding="utf-8") as f_out:
        reader = csv.reader(f_in)
        writer = csv.writer(f_out)

        first = True
        for row in reader:
            if first:
                # If the first row looks like a header, prepend the column name.
                # If your CSV has NO header, comment out this line and always write `value` instead.
                writer.writerow(row + [new_col_name])
                first = False
            else:
                writer.writerow(row + [value])


add_right_constant_column_no_pandas("unique_state.csv","uniqye_state_usa.csv",new_col_name="isoCode",value="USA")
#select_columns_no_pandas("vaccinations.csv","exact_vaccination.csv",["iso_code","date","people_vaccinated","people_fully_vaccinated","total_boosters"])

#add_right_constant_column_no_pandas("exact_vaccination.csv","add_url_vaccination.csv")

#select_columns_no_pandas("vaccinations.csv","exact_vaccination.csv",["location","date","people_vaccinated","people_fully_vaccinated","total_boosters"])

#select_columns_no_pandas("merge_csv.csv","exact_merge.csv",["location","date","people_vaccinated","people_fully_vaccinated","total_boosters","source_url"])