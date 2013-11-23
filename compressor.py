from os import listdir
from os.path import isfile, join
import json
import datetime

acc = 0

onlyfiles = [f for f in listdir("./") if isfile(join("./",f)) and f.endswith(".txt")]

start_time = datetime.datetime.now()
with open("bigtable.csv", "w+") as out:
	out.write("members,country,screen_name,type,closed,gid,name\n")
	for f in onlyfiles:
		for line in open(f, "r+"):		
			acc += 1
			if acc % 100000 == 0:
				print acc	
				print "Time passed:", (datetime.datetime.now() - start_time)
			try:
				j = json.loads(line.strip())
				data = [str(j.get('members_count')), str(j.get('country')), str(j.get('screen_name')), str(j.get('type')), str(j.get('is_closed')), str(j.get('gid')), str(j.get('name').encode('utf-8'))]
				out.write("\t".join(data) + "\n")
			except Exception,e:
				print "Problems while parsing\n" + line + "\n" + str(e)




