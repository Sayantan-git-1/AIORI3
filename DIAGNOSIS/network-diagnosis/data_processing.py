import csv
import math
import statistics

with open("dataset/network_data.csv", newline="", encoding="utf-8") as file:
	rows = list(csv.DictReader(file))

print(rows[:5])
print()
numeric_columns = {}
for column in rows[0] if rows else []:
	values = []
	for row in rows:
		try:
			value = float(row[column])
			if not math.isnan(value):
				values.append(value)
		except (TypeError, ValueError):
			continue
	if values:
		numeric_columns[column] = values

print({
	column: {
		"count": len(values),
		"mean": statistics.mean(values),
		"std": statistics.stdev(values) if len(values) > 1 else 0.0,
		"min": min(values),
		"max": max(values),
	}
	for column, values in numeric_columns.items()
})
print()
print({
	column: sum(value is None or value.strip() == "" for value in (row[column] for row in rows))
	for column in (rows[0] if rows else [])
})