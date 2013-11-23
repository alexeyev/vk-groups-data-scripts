from os import listdir
from os.path import isfile, join
import json

acc = 0

onlyfiles = [f for f in listdir("./") if isfile(join("./",f)) and f.endswith(".txt")]

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
				if j.get('members_count') == None:
					members = 0
				else:
					members = j.get('members_count')  
				if j.get('country') == None:
					country = 0
				else:
					country = j.get('country') 
				# a bit unsafe
				if j.get('deactivated') == None:
					put(members, country)
				#out.write(str(members) + "," + str(country) + "\n")
			except Exception,e:
				print "Problems while parsing\n" + line + "\n" + str(e)

	out.write("members_count, country, frequency\n")
	for m, c in bag:
		out.write(str(m) + "," + str(c) + "," + str(bag[(m,c)]) + "\n")





