import platform
sos = platform.uname()
message = 'Operating system : ' + sos[0] + ' ' + sos[2]
print message

