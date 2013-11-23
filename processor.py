from os import listdir
from os.path import isfile, join
import json

acc = 0

onlyfiles = [ f for f in listdir("./") if isfile(join("./",f)) and f.endswith(".txt")]

with open("result.csv", "w+") as out:
	for f in onlyfiles:
		for line in open(f, "r+"):		
			acc += 1
			if acc % 50000 == 0:
				print acc	
			try:
				j = json.loads(line.strip())
				members = j.get('members_count')
				country = j.get('country')
				out.write(str(members) + "," + str(country) + "\n")
			except:
				print "Problems while parsing\n" + line
