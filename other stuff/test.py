import csv
import glob

# Step 1: List all CSV files
csv_files = glob.glob("C:\\Users\\CodeUser\\Downloads\\korean_drama.csv\\*.csv")  # adjust path

# Step 2: Prepare to write to combined CSV
seen_titles = set()
with open("combined_ratings.csv", "w", newline='', encoding="utf-8") as outfile:
    writer = None
    
    for file in csv_files:
        with open(file, "r", newline='', encoding="utf-8") as infile:
            reader = csv.DictReader(infile)
            
            if writer is None:
                # Write header only once
                writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
                writer.writeheader()
            
            for row in reader:
                title = row['title'].strip()  # adjust column name if needed
                if title not in seen_titles:
                    writer.writerow(row)
                    seen_titles.add(title)
