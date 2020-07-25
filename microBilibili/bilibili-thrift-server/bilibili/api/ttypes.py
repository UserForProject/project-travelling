#
# Autogenerated by Thrift Compiler (0.13.0)
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#
#  options string: py
#

from thrift.Thrift import TType, TMessageType, TFrozenDict, TException, TApplicationException
from thrift.protocol.TProtocol import TProtocolException
from thrift.TRecursive import fix_spec

import sys

from thrift.transport import TTransport
all_structs = []


class UserInfo(object):
    """
    Attributes:
     - name
     - uid
     - fans
     - face

    """


    def __init__(self, name=None, uid=None, fans=None, face=None,):
        self.name = name
        self.uid = uid
        self.fans = fans
        self.face = face

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.name = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.I32:
                    self.uid = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.I32:
                    self.fans = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.STRING:
                    self.face = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('UserInfo')
        if self.name is not None:
            oprot.writeFieldBegin('name', TType.STRING, 1)
            oprot.writeString(self.name.encode('utf-8') if sys.version_info[0] == 2 else self.name)
            oprot.writeFieldEnd()
        if self.uid is not None:
            oprot.writeFieldBegin('uid', TType.I32, 2)
            oprot.writeI32(self.uid)
            oprot.writeFieldEnd()
        if self.fans is not None:
            oprot.writeFieldBegin('fans', TType.I32, 3)
            oprot.writeI32(self.fans)
            oprot.writeFieldEnd()
        if self.face is not None:
            oprot.writeFieldBegin('face', TType.STRING, 4)
            oprot.writeString(self.face.encode('utf-8') if sys.version_info[0] == 2 else self.face)
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)


class UserDetailedInfo(object):
    """
    Attributes:
     - name
     - uid
     - level
     - follower
     - follow
     - likes
     - playAmount
     - readingAmount
     - videos
     - face
     - fansData

    """


    def __init__(self, name=None, uid=None, level=None, follower=None, follow=None, likes=None, playAmount=None, readingAmount=None, videos=None, face=None, fansData=None,):
        self.name = name
        self.uid = uid
        self.level = level
        self.follower = follower
        self.follow = follow
        self.likes = likes
        self.playAmount = playAmount
        self.readingAmount = readingAmount
        self.videos = videos
        self.face = face
        self.fansData = fansData

    def read(self, iprot):
        if iprot._fast_decode is not None and isinstance(iprot.trans, TTransport.CReadableTransport) and self.thrift_spec is not None:
            iprot._fast_decode(self, iprot, [self.__class__, self.thrift_spec])
            return
        iprot.readStructBegin()
        while True:
            (fname, ftype, fid) = iprot.readFieldBegin()
            if ftype == TType.STOP:
                break
            if fid == 1:
                if ftype == TType.STRING:
                    self.name = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 2:
                if ftype == TType.I32:
                    self.uid = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 3:
                if ftype == TType.I32:
                    self.level = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 4:
                if ftype == TType.I32:
                    self.follower = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 5:
                if ftype == TType.I32:
                    self.follow = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 6:
                if ftype == TType.I32:
                    self.likes = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 7:
                if ftype == TType.I32:
                    self.playAmount = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 8:
                if ftype == TType.I32:
                    self.readingAmount = iprot.readI32()
                else:
                    iprot.skip(ftype)
            elif fid == 9:
                if ftype == TType.LIST:
                    self.videos = []
                    (_etype3, _size0) = iprot.readListBegin()
                    for _i4 in range(_size0):
                        _elem5 = {}
                        (_ktype7, _vtype8, _size6) = iprot.readMapBegin()
                        for _i10 in range(_size6):
                            _key11 = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                            _val12 = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                            _elem5[_key11] = _val12
                        iprot.readMapEnd()
                        self.videos.append(_elem5)
                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            elif fid == 10:
                if ftype == TType.STRING:
                    self.face = iprot.readString().decode('utf-8') if sys.version_info[0] == 2 else iprot.readString()
                else:
                    iprot.skip(ftype)
            elif fid == 11:
                if ftype == TType.LIST:
                    self.fansData = []
                    (_etype16, _size13) = iprot.readListBegin()
                    for _i17 in range(_size13):
                        _elem18 = iprot.readI32()
                        self.fansData.append(_elem18)
                    iprot.readListEnd()
                else:
                    iprot.skip(ftype)
            else:
                iprot.skip(ftype)
            iprot.readFieldEnd()
        iprot.readStructEnd()

    def write(self, oprot):
        if oprot._fast_encode is not None and self.thrift_spec is not None:
            oprot.trans.write(oprot._fast_encode(self, [self.__class__, self.thrift_spec]))
            return
        oprot.writeStructBegin('UserDetailedInfo')
        if self.name is not None:
            oprot.writeFieldBegin('name', TType.STRING, 1)
            oprot.writeString(self.name.encode('utf-8') if sys.version_info[0] == 2 else self.name)
            oprot.writeFieldEnd()
        if self.uid is not None:
            oprot.writeFieldBegin('uid', TType.I32, 2)
            oprot.writeI32(self.uid)
            oprot.writeFieldEnd()
        if self.level is not None:
            oprot.writeFieldBegin('level', TType.I32, 3)
            oprot.writeI32(self.level)
            oprot.writeFieldEnd()
        if self.follower is not None:
            oprot.writeFieldBegin('follower', TType.I32, 4)
            oprot.writeI32(self.follower)
            oprot.writeFieldEnd()
        if self.follow is not None:
            oprot.writeFieldBegin('follow', TType.I32, 5)
            oprot.writeI32(self.follow)
            oprot.writeFieldEnd()
        if self.likes is not None:
            oprot.writeFieldBegin('likes', TType.I32, 6)
            oprot.writeI32(self.likes)
            oprot.writeFieldEnd()
        if self.playAmount is not None:
            oprot.writeFieldBegin('playAmount', TType.I32, 7)
            oprot.writeI32(self.playAmount)
            oprot.writeFieldEnd()
        if self.readingAmount is not None:
            oprot.writeFieldBegin('readingAmount', TType.I32, 8)
            oprot.writeI32(self.readingAmount)
            oprot.writeFieldEnd()
        if self.videos is not None:
            oprot.writeFieldBegin('videos', TType.LIST, 9)
            oprot.writeListBegin(TType.MAP, len(self.videos))
            for iter19 in self.videos:
                oprot.writeMapBegin(TType.STRING, TType.STRING, len(iter19))
                for kiter20, viter21 in iter19.items():
                    oprot.writeString(kiter20.encode('utf-8') if sys.version_info[0] == 2 else kiter20)
                    oprot.writeString(viter21.encode('utf-8') if sys.version_info[0] == 2 else viter21)
                oprot.writeMapEnd()
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        if self.face is not None:
            oprot.writeFieldBegin('face', TType.STRING, 10)
            oprot.writeString(self.face.encode('utf-8') if sys.version_info[0] == 2 else self.face)
            oprot.writeFieldEnd()
        if self.fansData is not None:
            oprot.writeFieldBegin('fansData', TType.LIST, 11)
            oprot.writeListBegin(TType.I32, len(self.fansData))
            for iter22 in self.fansData:
                oprot.writeI32(iter22)
            oprot.writeListEnd()
            oprot.writeFieldEnd()
        oprot.writeFieldStop()
        oprot.writeStructEnd()

    def validate(self):
        return

    def __repr__(self):
        L = ['%s=%r' % (key, value)
             for key, value in self.__dict__.items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(L))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not (self == other)
all_structs.append(UserInfo)
UserInfo.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'name', 'UTF8', None, ),  # 1
    (2, TType.I32, 'uid', None, None, ),  # 2
    (3, TType.I32, 'fans', None, None, ),  # 3
    (4, TType.STRING, 'face', 'UTF8', None, ),  # 4
)
all_structs.append(UserDetailedInfo)
UserDetailedInfo.thrift_spec = (
    None,  # 0
    (1, TType.STRING, 'name', 'UTF8', None, ),  # 1
    (2, TType.I32, 'uid', None, None, ),  # 2
    (3, TType.I32, 'level', None, None, ),  # 3
    (4, TType.I32, 'follower', None, None, ),  # 4
    (5, TType.I32, 'follow', None, None, ),  # 5
    (6, TType.I32, 'likes', None, None, ),  # 6
    (7, TType.I32, 'playAmount', None, None, ),  # 7
    (8, TType.I32, 'readingAmount', None, None, ),  # 8
    (9, TType.LIST, 'videos', (TType.MAP, (TType.STRING, 'UTF8', TType.STRING, 'UTF8', False), False), None, ),  # 9
    (10, TType.STRING, 'face', 'UTF8', None, ),  # 10
    (11, TType.LIST, 'fansData', (TType.I32, None, False), None, ),  # 11
)
fix_spec(all_structs)
del all_structs
