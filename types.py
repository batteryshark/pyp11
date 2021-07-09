from ctypes import *

CK_BYTE = c_ubyte
CK_BYTE_PTR = POINTER(CK_BYTE)

CK_LONG = c_long

CK_ULONG_32 = c_uint32
CK_MECHANISM_TYPE = CK_ULONG_32
CK_ULONG = c_ulong
CK_ULONG_PTR = POINTER(CK_ULONG)

CK_OBJECT_HANDLE = CK_ULONG
CK_OBJECT_HANDLE_PTR = POINTER(CK_ULONG)

CK_UTF8CHAR = CK_BYTE
CK_UTF8CHAR_PTR = c_char_p
CK_RV = CK_ULONG

CK_ULONGLONG = c_ulonglong

CK_VOID_PTR = c_void_p
CK_VOID_PTR_PTR = POINTER(CK_VOID_PTR)


CK_FLAGS = CK_ULONG
CK_SLOT_ID = CK_ULONG
CK_SLOT_ID_PTR = POINTER(CK_SLOT_ID)

CK_USHORT = c_ulong
CK_USHORT_PTR = POINTER(CK_USHORT)


CK_CHAR = CK_BYTE
CK_CHAR_PTR = POINTER(CK_CHAR)

CK_BBOOL = CK_BYTE


CK_NOTIFY = CK_VOID_PTR
CK_USER_TYPE = CK_ULONG


CK_ATTRIBUTE_PTR = CK_VOID_PTR
CK_ATTRIBUTE_TYPE = CK_ULONG

CK_SESSION_HANDLE_PTR = CK_VOID_PTR
CK_SESSION_HANDLE = CK_ULONG

class CK_MECHANISM(Structure):
	_pack_ = 1
	_fields_ = [
	('mech_type',CK_MECHANISM_TYPE),
	('attr_value',CK_VOID_PTR),
	('attr_length',CK_ULONG_32)]

CK_MECHANISM_PTR = POINTER(CK_MECHANISM)

class CK_ATTRIBUTE(Structure):
	_pack_ = 1
	_fields_ = [
	('attr_type',c_uint32),
	('attr_value',CK_VOID_PTR),
	('attr_length',c_uint32)]


#class CK_ATTRIBUTE_ARRAY(Structure):
	#_pack=2
#    _fields_ = [('elements', ctypes.c_short),
                #an array of structs
#                ('STRUCT_ARRAY', ctypes.POINTER(CK_ATTRIBUTE))]	

