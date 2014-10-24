import csv
with open('sweep.csv') as f:
	reader=csv.DictReader(f)
	for row in reader:
		if reader.line_num<10:
			print row

