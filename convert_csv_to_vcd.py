#!/usr/bin/python
from datetime import datetime
import csv

# the header
timescale = '1s'
date = datetime.today()
header = '''$date
	%s
$end
$version
	Python
$end
$timescale
    %s	
$end
''' % (date, timescale)

config = { 
    'led'   : { 'type': 'reg', 'num': 4, 'sym': '+'},
    'count' : { 'type': 'reg', 'num': 8, 'sym': '*'}
    }

defs = ''
for key in config.keys():
    defs += "$var %s %d %s %s [%d:0] $end\n" % (config[key]['type'], config[key]['num'], config[key]['sym'], key, config[key]['num'] - 1)

module_def = '''$scope module test $end
%s
$upscope $end
$enddefinitions $end
#2
$dumpvars
''' % defs

clock = 0
data = 0
dumpvars = []

# the variables
with open('dumpvar.csv') as fh:
    reader = csv.reader(fh, delimiter=',')
    reader.next()
    for row in reader:
        # hard coded: time is column 1, led is 2 and count is 3
        dumpvars.append('#' + str(row[0])) # clock
        dumpvars.append(bin(int(row[1])).lstrip('0') + ' ' + config['led']['sym'])
        dumpvars.append(bin(int(row[2])).lstrip('0') + ' ' + config['count']['sym'])
        
# put it all together into the vcd
vcd = 'python.vcd'
with open(vcd, 'w') as fh:
    fh.write(header)
    fh.write(module_def)
    for v in dumpvars:
        fh.write(v + "\n")
