import csv

girlsDictionary = {}
boysDictionary = {}

with open("2000_GirlsNames.txt") as girls:
    for line in girls:

        line = line.replace("\n", "")
        line = line.replace(" ", ",")
        line = line.split(",")
        if line[0]!="449":
            girlsDictionary[line[0]] = int(line[1])
with open('girls.csv', 'w') as girlsCsv:
    writer = csv.writer(girlsCsv)
    writer.writerow(('Name', 'Count'))
    for key in girlsDictionary.keys():
        girlsCsv.write("%s,%s\n" % (key, girlsDictionary[key]))
girlsCsv.close()

with open("2000_BoysNames.txt") as girls:
    for line in girls:
        line = line.replace("\n", "")
        line = line.replace(" ", ",")
        line = line.split(",")
        if line[0] != "449":
            boysDictionary[line[0]] = int(line[1])
with open('boys.csv', 'w') as boysCsv:
    writer = csv.writer(boysCsv)
    writer.writerow(('Name', 'Count'))
    for key in boysDictionary.keys():
        boysCsv.write("%s,%s\n" % (key, boysDictionary[key]))
boysCsv.close()

csvfile = input("Which cvs file would you like to read? ")
thefile = open(csvfile)
for line in thefile:
    print(line)
thefile.close()
