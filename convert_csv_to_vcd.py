#!/usr/bin/python
from datetime import datetime
import csv

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

    #$var reg 8 * data [7:0] $end
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

with open('dumpvar.csv') as fh:
    reader = csv.reader(fh, delimiter=',')
    reader.next()
    for row in reader:
        dumpvars.append('#' + str(row[0])) # clock
        dumpvars.append(bin(int(row[1])).lstrip('0') + ' ' + config['led']['sym'])
        dumpvars.append(bin(int(row[2])).lstrip('0') + ' ' + config['count']['sym'])
        
"""
for i in range(100):
    dumpvars.append('#' + str(i)) # clock
    dumpvars.append(str(clock) + ')')
    if clock == 1:
        clock = 0
    else:
        clock = 1
    if i % 10 == 0:
        data += 1
        dumpvars.append(bin(data).lstrip('0') + ' *')
"""    
    
vcd = 'python.vcd'
with open(vcd, 'w') as fh:
    fh.write(header)
    fh.write(module_def)
    for v in dumpvars:
        fh.write(v + "\n")
