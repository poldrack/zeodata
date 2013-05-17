"""
defines a class to store a ZEO raw data record
- based heavily upon java code from http://zeodecoderview.sourceforge.net/

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

import pytz
import datetime
import numpy
import time

IDENTIFIER_SIZE = 6
VERSION_SIZE    = 2
HEADER_SIZE     = IDENTIFIER_SIZE + VERSION_SIZE
EVENTS_SAVED=4
ASSERT_NAME_MAX = 20
HEADBAND_IMPEDANCE_SIZE = 144
HEADBAND_PACKETS_SIZE = 144
HEADBAND_RSSI_SIZE = 144
HEADBAND_STATUS_SIZE = 36

def timestamp_to_calendar(timestamp):
    
    central = pytz.timezone('US/Central')
    d= datetime.datetime.fromtimestamp(timestamp)+datetime.timedelta(hours=5)

    return d.strftime('%Y-%m-%d %H:%M:%S')
    #return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(timestamp))


def time_to_hrmins(secs):
    # convert from floating mins to hours/mins
    time=float(secs)/120.0
    hrs=numpy.floor(time)
    mins=(time - hrs)*60.0
    return '%d:%02.0f'%(hrs,mins)

def sleep_length(start_time,finish_time):
    return []

class ZeoRecord:

    def __init__(self):
        self.checksum=[]
	self.identifier=[]
        self.version=[]
        self.timestamp=[]
        self.crc=[]
        self.history=[]
        self.airplane_off=[]
        self.airplane_on=[]
        self.change_time=[]
        self.change_value=[]
        self.assert_function_name=[]
        self.assert_line_number=[]
        self.factory_reset=[]
        self.headband_id=[]
        self.hb_imp=[]
        self.hb_pkt=[]
        self.hb_rssi=[]
        self.hb_status=[]
        self.id_hw=[]
        self.id_sw=[]
        self.sensor_life_reset=[]
        self.sleep_stat_reset=[]
        self.alarm_events=[]
        self.snooze_events=[]
        self.alarm_off=[]
        
        self.awakenings            = []
        self.awakenings_average    = []
        self.end_of_night          = []
        self.start_of_night        = []
        self.length_of_night=[]
        self.time_in_deep          = []
        self.time_in_deep_average  = []
        self.time_in_deep_best     = []
        self.time_in_light         = []
        self.time_in_light_average = []
        self.time_in_rem           = []
        self.time_in_rem_average   = []
        self.time_in_rem_best      = []
        self.time_in_wake          = []
        self.time_in_wake_average  = []
        self.time_to_z             = []
        self.time_to_z_average     = []
        self.total_z               = []
        self.total_z_average       = []
        self.total_z_best          = []
        self.zq_score              = []
        self.zq_score_average      = []
        self.zq_score_best         = []
        self.display_hypnogram_forced_index = []
        self.display_hypnogram_forced_stage =[]
        self.hypnogram_start_time=[]
        self.sleep_rating=[]
        self.base_hypnogram_count=[]
        self.base_hypnogram=[]
        self.display_hypnogram=[]
        


    def getRecordData(self,binaryReader):
        # takes binary record with header removed

        self.version=binaryReader.read('int16')
        self.timestamp=binaryReader.read('uint32')
        self.crc=binaryReader.read('uint32')
#        if self.crc != checksum:
#            print 'MISMATCH',crc,checksum

        self.history=binaryReader.read('uint32')

        self.airplane_off=binaryReader.read('uint32')
        self.airplane_on=binaryReader.read('uint32')

        for i in range(EVENTS_SAVED):
            self.change_time.append(binaryReader.read('uint32'))

        for i in range(EVENTS_SAVED):
            self.change_value.append(binaryReader.read('uint32'))

        for i in range(ASSERT_NAME_MAX):
            self.assert_function_name.append(binaryReader.read('char'))
        self.assert_line_number=binaryReader.read('int32')

        self.factory_reset=binaryReader.read('int32')
        self.headband_id=binaryReader.read('int32')

        for i in range(HEADBAND_IMPEDANCE_SIZE):
            self.hb_imp.append(binaryReader.read('uint8'))

        for i in range(HEADBAND_PACKETS_SIZE):
            self.hb_pkt.append(binaryReader.read('uint8'))

        for i in range(HEADBAND_RSSI_SIZE):
            self.hb_rssi.append(binaryReader.read('uint8'))

        for i in range(HEADBAND_STATUS_SIZE):
            self.hb_rssi.append(binaryReader.read('uint8'))

        self.id_hw=binaryReader.read('uint16')
        #print 'id_hw:',id_hw
        self.id_sw=binaryReader.read('uint16')

        for i in range(EVENTS_SAVED):
            self.change_time.append(binaryReader.read('uint32'))

        for i in range(EVENTS_SAVED):
            self.change_value.append(binaryReader.read('uint32'))

        self.sensor_life_reset=binaryReader.read('uint32')
        self.sleep_stat_reset=binaryReader.read('uint32')

        ALARM_EVENTS_SAVED = 2

        self.alarm_ring_count = ALARM_EVENTS_SAVED

        for i in range(self.alarm_ring_count):
            self.alarm_events.append(binaryReader.read('uint32'))

        SNOOZE_EVENTS_SAVED = 9
        for i in range(SNOOZE_EVENTS_SAVED):
          self.snooze_events.append(binaryReader.read('uint32'))

        self.alarm_off=binaryReader.read('uint32')

        self.awakenings            = binaryReader.read('uint16')
        self.awakenings_average    = binaryReader.read('uint16')
        self.end_of_night_timestamp          = binaryReader.read('uint32')
        self.end_of_night=timestamp_to_calendar(self.end_of_night_timestamp)
        self.start_of_night_timestamp        = binaryReader.read('uint32')
        self.start_of_night        = timestamp_to_calendar(self.start_of_night_timestamp)
        self.length_of_night=self.end_of_night_timestamp - self.start_of_night_timestamp
        self.time_in_deep          = binaryReader.read('uint16')
        self.time_in_deep_average  = binaryReader.read('uint16')
        self.time_in_deep_best     = binaryReader.read('uint16')
        self.time_in_light         = binaryReader.read('uint16')
        self.time_in_light_average = binaryReader.read('uint16')
        self.time_in_rem           = binaryReader.read('uint16')
        self.time_in_rem_average   = binaryReader.read('uint16')
        self.time_in_rem_best      = binaryReader.read('uint16')
        self.time_in_wake          = binaryReader.read('uint16')
        self.time_in_wake_average  = binaryReader.read('uint16')
        self.time_to_z             = binaryReader.read('uint16')
        self.time_to_z_average     = binaryReader.read('uint16')
        self.total_z               = binaryReader.read('uint16')
        self.total_z_average       = binaryReader.read('uint16')
        self.total_z_best          = binaryReader.read('uint16')
        self.zq_score              = binaryReader.read('uint16')
        self.zq_score_average      = binaryReader.read('uint16')
        self.zq_score_best         = binaryReader.read('uint16')

        self.display_hypnogram_forced_index = binaryReader.read('uint16')
        self.display_hypnogram_forced_stage =binaryReader.read('uint16')
        self.hypnogram_start_time = timestamp_to_calendar(binaryReader.read('uint32'));
        self.sleep_rating =binaryReader.read('uint8')
        # get padding
        binaryReader.read('uint8')
        binaryReader.read('uint8')
        binaryReader.read('uint8')
        binaryReader.read('uint32')

        # read hypnogram
        self.base_hypnogram_count = binaryReader.read('uint32')


        SECONDS_PER_EPOCH  = 30
        SECONDS_PER_HOUR   = 3600
        HYP_SECONDS_MAX      = (16 * SECONDS_PER_HOUR)
        HYP_BASE_STEP        = (SECONDS_PER_EPOCH)
        HYP_BASE_LENGTH      = (HYP_SECONDS_MAX/HYP_BASE_STEP)

        for i in range(0,HYP_BASE_LENGTH,2):
            input=binaryReader.read('uint8')
            self.base_hypnogram.append( input & 0xf)
            self.base_hypnogram.append(input >> 4)
        
    def printSummary(self):
        print 'timestamp:',timestamp_to_calendar(self.timestamp)
        print 'start time:',self.start_of_night
        print 'end time:',self.end_of_night
        print 'length of recording:%0.2f'%float(self.length_of_night/3600.0)
        print 'Total Z',time_to_hrmins(self.total_z)
        print 'REM',time_to_hrmins(self.time_in_rem)
        print 'Light',time_to_hrmins(self.time_in_light)
        print 'Deep',time_to_hrmins(self.time_in_deep)
        print 'Wake',time_to_hrmins(self.time_in_wake)
        print 'hypogram start time:',self.hypnogram_start_time
        print 'hypnogram count',self.base_hypnogram_count
        print 'ZQ:',self.zq_score
        print 'Time to Z:',time_to_hrmins(self.time_to_z)

    def make_display_hypnogram(self):
        # make the displayable hypnogram from the base
        # 0=unkonwn
        # 1=deep
        # 2=light
        # 3=REM
        # 4=wake
        zeoSleepStates={'unknown':0,'deep':4,'light':3,'REM':2,'wake':1,'deep2':6}
        
        HYP_BASE_STEP = 30
        HYP_DISPLAY_STEP=5.0*60.0
        HYP_SECONDS_MAX      = 16.0*3600.0
        HYP_DISPLAY_LENGTH   = HYP_SECONDS_MAX /HYP_DISPLAY_STEP
        HYP_BASE_PER_DISPLAY = int(HYP_DISPLAY_STEP / HYP_BASE_STEP)
        
        # ignore empty bins
        n_display = numpy.floor(self.base_hypnogram_count / HYP_BASE_PER_DISPLAY).astype('int')

        for i in range(n_display):
            i_base=i*HYP_BASE_PER_DISPLAY
            for j in range(HYP_BASE_PER_DISPLAY):
                if self.base_hypnogram[i_base]==zeoSleepStates['deep'] or self.base_hypnogram[i_base]==zeoSleepStates['deep2']:
                    stage=1
                elif  self.base_hypnogram[i_base]==zeoSleepStates['light']:
                    stage=2
                elif  self.base_hypnogram[i_base]==zeoSleepStates['REM']:
                    stage=3
                elif  self.base_hypnogram[i_base]==zeoSleepStates['wake']:
                    stage=4
                else:
                    stage=0
                self.display_hypnogram.append(stage)
                i_base+=1
                
