"""
load data from zeo binary file and process

"""

## Copyright 2013, Russell Poldrack. All rights reserved.

## Redistribution and use in source and binary forms, with or without modification, are
## permitted provided that the following conditions are met:

##    1. Redistributions of source code must retain the above copyright notice, this list of
##       conditions and the following disclaimer.

##    2. Redistributions in binary form must reproduce the above copyright notice, this list
##       of conditions and the following disclaimer in the documentation and/or other materials
##       provided with the distribution.

## THIS SOFTWARE IS PROVIDED BY RUSSELL POLDRACK ``AS IS'' AND ANY EXPRESS OR IMPLIED
## WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
## FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL RUSSELL POLDRACK OR
## CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
## CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
## SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
## ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
## NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
## ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from BinaryReader import BinaryReader
import matplotlib.pyplot as plt
import numpy
import pytz
import datetime
from zeoRecord import ZeoRecord
import sys,os

def time_to_hrmins(secs):
    # convert from floating mins to hours/mins
    time=float(secs)/120.0
    hrs=numpy.floor(time)
    mins=(time - hrs)*60.0
    return '%d:%02.0f'%(hrs,mins)


if len(sys.argv)<2:
	print 'USAGE: process_zeodata.py <dat file>'
	sys.exit(1)
else:
	datafile=sys.argv[1]
	if not os.path.exists(datafile):
		print '%s does not exist:'%datafile
		print 'USAGE: process_zeodata.py <dat file>'
                sys.exit(1)
		
IDENTIFIER_SIZE = 6
VERSION_SIZE    = 2
HEADER_SIZE     = IDENTIFIER_SIZE + VERSION_SIZE
EVENTS_SAVED=4
ASSERT_NAME_MAX = 20
HEADBAND_IMPEDANCE_SIZE = 144
HEADBAND_PACKETS_SIZE = 144
HEADBAND_RSSI_SIZE = 144
HEADBAND_STATUS_SIZE = 36



binaryReader=BinaryReader(datafile)

alldata={}
good_session=1
record_length=[]
hypnogram_count=[]
start_of_night=[]

ctr=0
while good_session:
  #print binaryReader.BytesRemaining(),'bytes remaining'
  if  binaryReader.BytesRemaining()<1680:
      #print ''
      #print 'breaking: no records remaining'
      good_session=0
  else:
    
    identifier=[]
    while not identifier:
        # yank header
        tmp=[]
        for i in range(IDENTIFIER_SIZE):
            tmp.append(binaryReader.read('char'))
        if ''.join(tmp).find('SLEEP')>-1:
            identifier=tmp
            

    record=ZeoRecord()
    #print ''
    #print 'Reading Session %d:'%int(ctr+1)
    record.getRecordData(binaryReader)
    # check for empty start/finish times
    if record.start_of_night_timestamp>0 and record.end_of_night_timestamp>0 and record.base_hypnogram_count>0:
        record.make_display_hypnogram()
        alldata[ctr]=record
        #record.printSummary()
        record_length.append(record.length_of_night)
        hypnogram_count.append(record.base_hypnogram_count)
        start_of_night.append(record.start_of_night_timestamp)
        ctr+=1
    else:
        continue
        #print 'skipping bad record'
        #record.printSummary()

    #if not (crc in CRC16_TABLE):
    #    print 'BAD CRC'
        
#  except:
#      good_session=0


# get unique nights
unique_nights=list(set(start_of_night))
unique_nights.sort()

chosen_record={}
for u in unique_nights:
    matching_records=[i for i in alldata.iterkeys() if alldata[i].start_of_night_timestamp==u]
    #print u,matching_records
    sleeplen=0
    for r in matching_records:
        if alldata[r].length_of_night>sleeplen:
            sleeplen=alldata[r].length_of_night
            chosen_record[u]=r
            #print 'choosing',chosen_record[u]
    
#plt.plot(numpy.array(base_hypnogram))
print ''
print 'Found %d good records'%len(unique_nights)

if os.path.exists('zeodata.txt'):
	print 'appending data to zeodata.txt'
else:
	print 'writing data to zeodata.txt'
f=open('zeodata.txt','a')

f.write('startDate\tstartTime\twakeDate\twakeTime\tTotalZ\tZQ\tTimeInDeep\tTimeInLight\tTimeInREM\tTimeInWake\tTimeToZ\tHypnogramData\n')

for u in unique_nights:
    d=alldata[chosen_record[u]]
    d.printSummary()
    print ''
    f.write('%s\t'%d.start_of_night.replace(' ','\t'))
    f.write('%s\t'%d.end_of_night.replace(' ','\t'))
    f.write('%s\t'%time_to_hrmins(d.total_z))
    f.write('%d\t'%d.zq_score)
    f.write('%s\t'%time_to_hrmins(d.time_in_deep))
    f.write('%s\t'%time_to_hrmins(d.time_in_light))
    f.write('%s\t'%time_to_hrmins(d.time_in_rem))
    f.write('%s\t'%time_to_hrmins(d.time_in_wake))
    f.write('%s\t'%time_to_hrmins(d.time_to_z))
    for i in d.display_hypnogram:
	    f.write('%d\t'%i)

    f.write('\n')

f.close()
