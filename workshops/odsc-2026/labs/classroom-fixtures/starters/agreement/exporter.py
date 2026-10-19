import csv
import io

def export_rows(rows):
    stream = io.StringIO(newline="")
    writer = csv.writer(stream)
    writer.writerow(["customer_id", "region"])
    for row in rows:
        writer.writerow([row["customer_id"], row["region"]])
    return stream.getvalue()
