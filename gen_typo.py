import operator
import os
import sys
import re

def build_dict(dict_file, dict_obj):
	f = open(dict_file, 'r')
	for word in f.readlines():
		word = re.sub('[^a-z]+', '', word)
		dict_obj[word] = 1
	f.close()

def build_new_typo_dict(typo_file, dict_obj, new_typo_dict):
	f = open(typo_file, 'r')
	for line in f.readlines():
		if line.startswith('#') == False:
			pair = re.split('\|\|', line)
			pair[1] = re.sub('[^a-z]+', '', pair[1])
			min_len = min(len(pair[0]), len(pair[1]))
			idx = 0
			ret_typo = ''
			ret_correct = ''

			if len(pair[0]) < len(pair[1]):
				continue

			for i in range(min_len):
				if pair[0][i] != pair[1][i]:
					idx = i
					break

			if len(pair[1][idx:]) < 4:
				# correction
				while True:
					if idx <= 1:
						break
					idx = idx -1
					substr = pair[1][idx:]
					try:
						value = dict_obj[substr]
						ret_correct = substr
						ret_typo = pair[0][idx:]
					except KeyError:
						continue
			else:
				ret_correct = pair[1][idx:]
				ret_typo = pair[0][idx:]

			if len(ret_correct) > 0 and len(ret_typo) > 0:
				try:
					value = dict_obj[ret_typo]
				except KeyError:
					new_typo_dict[ret_correct] = ret_typo
	f.close()

def build_kernel_word(typo_file, kernel_word):
	f = open(typo_file, 'r')
	idx = 0
	for line in f.readlines():
		if line.startswith('#') == False:
			pair = re.split('\|\|', line)
			pair[1] = re.sub('[^a-z]+', '', pair[1])
			if len(pair[0]) > 0 and len(pair[1]) > 0:
				kernel_word.append(pair[1])
		idx = idx + 1
	f.close()

def gen_new_typo_file(typo_file, kernel_word, new_typo_dict, ret_file):
	tf = open(typo_file, 'r')
	f = open(ret_file, 'w')
	buf = tf.read()

	for i in range(len(kernel_word)):
		for kn, vn in new_typo_dict.iteritems():
			if kn in kernel_word[i]:
				tmpstr = str(kernel_word[i])
				tmpstr = tmpstr.replace(kn, vn)
				if tmpstr not in buf:
					if tmpstr != 'enames' and tmpstr != 'eenabled':		# filter false positive typo
						f.write(tmpstr + '||' + kernel_word[i] + '\n')
	f.close()
	tf.close()

def gen_typo(dict_file, typo_file, ret_file):
	dict_obj = dict()
	new_typo_dict = dict()
	kernel_word = []

	build_dict(dict_file, dict_obj)
	build_new_typo_dict(typo_file, dict_obj, new_typo_dict)

	del dict_obj
	build_kernel_word(typo_file, kernel_word)
	gen_new_typo_file(typo_file, kernel_word, new_typo_dict, ret_file)

if __name__ == '__main__' :
	if len(sys.argv) != 4:
		print 'USAGE : gen_typo.py [dictionary file] [typo file] [result file]'
	else:
		gen_typo(sys.argv[1], sys.argv[2], sys.argv[3])

