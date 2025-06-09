# # save_utils.py

# import csv
# import os

# def save_to_csv(parsed_data, filename="parsed_resumes.csv"):
#     fieldnames = ["Name", "Email", "Phone Number", "LinkedIn", "Education", "Experience", "Projects", "Skills"]

#     # Check if the file already exists
#     file_exists = os.path.isfile(filename)

#     with open(filename, mode="a", newline='', encoding="utf-8") as f:
#         writer = csv.DictWriter(f, fieldnames=fieldnames)

#         if not file_exists:
#             writer.writeheader()

#         row = {key: parsed_data.get(key, "") for key in fieldnames}

#         # Convert lists/dicts to string for storage
#         for k in row:
#             if isinstance(row[k], (list, dict)):
#                 row[k] = str(row[k])

#         writer.writerow(row)
import csv
import pandas as pd

def save_to_csv(parsed_data, file_name="parsed_resume.csv"):
    flat_rows = []

    for key, value in parsed_data.items():
        if isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    item_copy = item.copy()
                    item_copy["Section"] = key
                    flat_rows.append(item_copy)
                else:
                    flat_rows.append({"Section": key, "Value": item})
        else:
            flat_rows.append({"Section": key, "Value": value})

    df = pd.DataFrame(flat_rows)
    df.to_csv(file_name, index=False)
    return df  # ✅ Make sure to return the DataFrame

