

include_file = open('NIDAQmx.h', 'r')
cfile = open('nidaqmx_functions.py', 'w')
cfile.write('\n')
cfile.write('class TranslatedFunctions() :\n')
cfile.write('\tdef __init__(self, dll) :\n')
cfile.write('\t\t# The dll will be the nidaqmx dll.\n')
for line in include_file :
	if line.find('int32 __CFUNC') == 0 :
		begin = line.find('DAQ')
		end = line.find('(')
		func = line[begin:end]
		usage = line[end:].strip()
		#usage.replace(' ', '')
		#usage.replace('\t', '')
		usage = ''.join(usage.split('\t'))
		outline = '\t\tself.' + func[5:].strip() + ' = dll.' + func + '\t# ' + usage +'\n'
		cfile.write(outline)
cfile.close()
include_file.close()
