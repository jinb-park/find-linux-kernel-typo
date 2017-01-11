import operator
import sys
import re
import os

def write_result_file(ret_dict, ret_file):
	f = open(ret_file, 'w')

	f.write('[ detected typo list ]\n')
	for k, v in ret_dict.iteritems():
		f.write(k + '\n')
	f.write('\n\n')

	f.write('[ rank ]\n')
	sorted_ret = sorted(ret_dict.iteritems(), key=operator.itemgetter(1), reverse=True)
	for i in range(len(sorted_ret)):
		f.write(str(sorted_ret[i][1]) + ' ' + sorted_ret[i][0] + '\n')
	f.close()

def search_typo(kernel_path, typo_file, ret_file):
	ret_dict = dict()
	for subdir, dirs, files in os.walk(kernel_path):
		for file in files:
			filepath = subdir + os.sep + file
			if "/." in filepath:
				continue
	
			fp = open(filepath, 'r')
			tf = open(typo_file, 'r')

			buf = fp.read()
			for line in tf.readlines():
				if line.startswith('#') == False:
					pair = re.split('\|\|', line)
					if pair[0] in buf:
						print '[' + pair[0] + '] ' + filepath
						try:
							ret_dict[pair[0]] = ret_dict[pair[0]] + 1
						except KeyError:
							ret_dict[pair[0]] = 1
			tf.close()
			fp.close()
	write_result_file(ret_dict, ret_file)

if __name__ == '__main__' :
	if len(sys.argv) != 4:
		print 'USAGE : search_typo.py [kernel path] [new typo file] [result file]'
	else:
		search_typo(sys.argv[1], sys.argv[2], sys.argv[3])