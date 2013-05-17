# based on recipe from http://code.activestate.com/recipes/577610-decoding-binary-files/

import struct

class BinaryReaderEOFException(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return 'Not enough bytes in file to satisfy read request'

class BinaryReader:
    # Map well-known type names into struct format characters.
    typeNames = {
        'int8'   :'b',
        'uint8'  :'B',
        'int16'  :'h',
        'uint16' :'H',
        'int32'  :'i',
        'uint32' :'I',
        'int64'  :'q',
        'uint64' :'Q',
        'float'  :'f',
        'double' :'d',
        'char'   :'s'}

    def __init__(self, fileName):
        self.file = open(fileName, 'rb')
        
    def read(self, typeName):
        typeFormat = BinaryReader.typeNames[typeName.lower()]
        typeSize = struct.calcsize(typeFormat)
        value = self.file.read(typeSize)
        if typeSize != len(value):
            raise BinaryReaderEOFException
        return struct.unpack(typeFormat, value)[0]
    
    def __del__(self):
        self.file.close()
        
    def BytesRemaining(self):
        """ Get number of bytes left to read, where f_len is the length of the file (probably from f_len=LengthOfFile(f) )"""
        currentPos=self.file.tell()
        return self.LengthOfFile()-currentPos

    def GetNextRecord(self,nbytes):
        """ Get next nbytes bytes, and then reposition to origin point"""
        currentPos=self.file.tell()
        data=self.file.read(nbytes)
        self.file.seek(currentPos, 0) # go back to where we started
        return data
    
    def LengthOfFile(self):
        """ Get the length of the file for a regular file (not a device file)"""
        currentPos=self.file.tell()
        self.file.seek(0, 2)          # move to end of file
        length = self.file.tell()     # get current position
        self.file.seek(currentPos, 0) # go back to where we started
        return length
