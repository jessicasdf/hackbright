with open('names.txt') as f:
	data=f.readlines()
	
stripped=[]
for name in data:
	stripped.append(name.strip())

data = sorted(stripped)

print "The names are:"
for name in data:
	print name