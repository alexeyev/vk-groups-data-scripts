from os import listdir
from os.path import isfile, join
import json

acc = 0

onlyfiles = [ f for f in listdir("./") if isfile(join("./",f)) and f.endswith(".txt")]

bag = {}

def put(mmbr, cntr):
	global bag
	if not (mmbr, cntr) in bag:
		bag[(mmbr, cntr)] = 0
	bag[(mmbr, cntr)] += 1

with open("hist.csv", "w+") as out:
	for f in onlyfiles:
		for line in open(f, "r+"):		
			acc += 1
			if acc % 50000 == 0:
				print acc	
			try:
				j = json.loads(line.strip())
				members = j.get('members_count')
				country = j.get('country')
				if members != None:
					put(members,country)
				#out.write(str(members) + "," + str(country) + "\n")
			except Exception,e:
				print "Problems while parsing\n" + line + "\n" + str(e)
	for m, c in bag:
		out.write(str(m) + "," + str(c) + "," + str(bag[(m,c)]) + "\n")
