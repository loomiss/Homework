
import string as s

def SaveResults(freqs, amplitude, phase) :
    outfile = raw_input('Enter a file name or nothing to skip: ')
    if s.strip(outfile) :
        o = open(outfile, 'w')
        o.write('# frequency in Hz, absolute value of transmission, phase\n\n')
        for i in range(len(freqs)) :
            o.write(str(freqs[i]) + ',' + str(amplitude[i]) + ',' + str(phase[i]) + '\n')
        o.close()
    return

def ReadParametersFile(file_name, validation) :
    # Validation is the name of this program, 'initialize_fg_scope.py'
    error = ''
    warning = ''
    inst = {}
    op = {}
    category = ''
    fin = open(file_name, 'r')
    file_lines = fin.readlines()
    fin.close()
    for aline in file_lines :
        al = s.strip(s.split(aline, '#')[0])     # Ignore comment fields.
        #print al
        if al :    # Ignore comment lines.
            # Check for a change in category indicated by a leading >.
            if al.startswith('>') :
                category = s.strip(s.split(al, '>')[1]).lower()
                inst[category] = {}
                if (category == 'fg') | (category == 'scope') :
                    inst[category]['com'] = []

            elif category == 'validation' :
                if al.lower() != validation.lower() :
                        error = 'The validation argument in ' + file_name + ' does not match the name of this program, ' + validation + '.'
                        return p, error, warning
            elif category == 'instruments' :
                a = s.split(al)
                b = []
                for aa in a :
                    aaa = s.strip(aa)
                    if aaa :
                        b.append(aaa)
                thiskey = b[0]
                inst[b[0]] = {}
                del b[0]
                inst[thiskey]['id'] = b
                inst[thiskey]['com'] = []
            elif (category == 'fg') | (category == 'scope') :
                inst[category]['com'].append(al)
            elif category == 'op' :
                a = s.split(al, '=')
                op[s.strip(a[0])]= s.split(s.strip(a[1]), ',')
            else :
                warning += 'Malformed line: ' + al + '\n'
    if warning : warning = 'Warnings for the following lines in ' + validation + ':\n' + warning
    return inst, op, error, warning

