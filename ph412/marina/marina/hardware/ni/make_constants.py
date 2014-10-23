

include_file = open('NIDAQmx.h', 'r')
cfile = open('nidaqmx_constants.py', 'w')
cfile.write('\n')
cfile.write('class TranslatedConstants() :\n')
cfile.write('\tdef __init__(self) :\n')
cfile.write('\t\t# The dll will be the nidaqmx dll.\n')
number = 0
for line in include_file :
	if line.find('#define DAQ') == 0 :
		pieces = line.split(' ')
		constant = pieces[1].strip()
		for i in range(2, len(pieces)) :
			if len(pieces[i]) > 0 :
				raw_number = pieces[i].strip()
				try :
					if raw_number.lower().find('x') > -1 :
						number = int(raw_number, 16)
					else :
						number = int(raw_number)
					print constant[6:], number
					#cfile.write('\t\tself.' + constant[6:] + ' = dll.' + constant + '\t\t# ' + str(number) + ' = ' + raw_number + '\n')
					cfile.write('\t\tself.' + constant[6:] + ' = ' + str(number) + '\t\t# ' + constant + ' = ' + raw_number + '\n')
					break
				except :
					#print 'Unfathomable number: ' + pieces[i].strip()
					pass
cfile.close()
include_file.close()
