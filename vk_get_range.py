from urllib2 import *
from sys import argv
from random import shuffle
import yaml
import datetime

# random shuffling
def mix(array):
	def wrap(array):
		return chunk(array, 1)
	def unwrap(wrapped_array):
		return [one_element_array[0] for one_element_array in wrapped_array]
	wrapped_array = wrap(array) 	
	shuffle(wrapped_array)
	return unwrap(wrapped_array)

# chunking array to chunks with n elements each (i love one-liners)
def chunk(array, n):
	return [array[start: start + n] for start in [n * i for i in range(len(array) / n + 1)] if start <> len(array)]

# nice printing for dict
def convert(input):
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

#==================================================================================================

start_time = datetime.datetime.now()

# ids chunk size for submitting to API
chunk_size = 500

# list arg0..arg1
ids_chunks = chunk(mix(range(int(argv[1]), int(argv[2]) + 1)), chunk_size)

counter = 0
url_pattern = "http://api.vk.com/method/groups.getById?fields=members_count&group_ids="

storage = open(argv[3], "w+")

for chunk in ids_chunks:
	# todo: change User-Agent header
	response = urlopen(url_pattern + ",".join([str(index) for index in chunk])).read()
	loaded = yaml.load(response.replace("\/", "/"))
	counter += len(loaded['response'])
	print "Loaded:", counter
	for record in loaded['response']:
		print record
		storage.write(str((record)) + "\n")	
storage.close()


finish_time = datetime.datetime.now()
print "Done in just", (finish_time - start_time)

