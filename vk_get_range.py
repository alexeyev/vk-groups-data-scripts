from urllib2 import *
from sys import argv
from random import shuffle
import json, io, datetime

# random shuffling
def mix(array):
	def wrap(array):
		return chunk_array(array, 1)
	def unwrap(wrapped_array):
		return [one_element_array[0] for one_element_array in wrapped_array]
	wrapped_array = wrap(array) 	
	shuffle(wrapped_array)
	return unwrap(wrapped_array)

# splitting array to chunks with n elements each (i love disgusting one-liners)
def chunk_array(array, n):
	return [array[start: start + n] for start in [n * i for i in range(len(array) / n + 1)] if start <> len(array)]

# made constant so as not to create a new object every time
url_pattern = "http://api.vk.com/method/groups.getById?fields=members_count,country&group_ids="
headers = {'User-agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; de; rv:1.9.1.5)', 'Content-type' : 'text/html; charset=UTF8'}

def build_url(chunk):
	global url_pattern
	return url_pattern + ",".join([str(index) for index in chunk])

def build_request(chunk):
	global headers
	return Request(build_url(chunk), None, headers)

def build_json_dump(js):
	return unicode(json.dumps(js, ensure_ascii=False))

# --- running stuff ---

start_time = datetime.datetime.now()

# ids chunk size for submitting to API
chunk_size = 500

# big piece size (implemented due to memory issues)
piece_size = 100 * 1000

# ids overall range
start = int(argv[1])
finish = int(argv[2])

pieces = (finish - start + 1) / piece_size

# splitting into smaller pieces for mixing and downloading
# todo: make pretty
frs = [fr * piece_size + start for fr in range(pieces)]
ranges = [(fr, fr + piece_size - 1) for fr in frs]
last_pair = ranges[len(ranges) - 1] 
ranges[len(ranges) - 1] = (last_pair[0], finish)

counter = 0

def run(fromm, too, storage):
	global counter
	print "Getting clubs from", fromm, "to", too
	# list: numbers of groups for requests
	ids_chunks = chunk_array(mix(range(fromm, too + 1)), chunk_size)
	for chunk in ids_chunks:
		# getting response from API
		response = urlopen(build_request(chunk)).read()	

		# parsing json		
		loaded = json.loads(response)

		# reporting number of records
		counter += len(loaded['response'])
		print "Loaded:", counter

		# flushing to file
		for record in loaded['response']:
			storage.write(build_json_dump(record) + "\n")	

# todo: well i dunno maybe we should write to different files...
with io.open(argv[3], "w", encoding="utf-8") as storage:
	for fr, to in ranges:	
		run(fr, to, storage)

finish_time = datetime.datetime.now()
print "Done in just", (finish_time - start_time)
print "Loaded", counter,"/", finish - start + 1

