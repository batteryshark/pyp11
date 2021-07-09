from ctypes import *
from .types import *

#plib = CDLL("./opensc-pkcs11.dll")
plib = CDLL("./sc_hsm_pkcs11_64.dll")

plib.C_Initialize.argtypes = [CK_VOID_PTR]
plib.C_Initialize.restype = CK_RV

plib.C_OpenSession.argtypes = [CK_SLOT_ID, CK_FLAGS, CK_VOID_PTR, CK_NOTIFY, CK_SESSION_HANDLE_PTR]
plib.C_OpenSession.restype = CK_RV

plib.C_Login.argtypes = [CK_SESSION_HANDLE,CK_USER_TYPE,CK_UTF8CHAR_PTR,CK_ULONG]
plib.C_Login.restype = CK_RV

plib.C_GenerateRandom.argtypes = [CK_SESSION_HANDLE,CK_BYTE_PTR,CK_ULONG]
plib.C_GenerateRandom.restype = CK_RV

plib.C_Logout.argtypes = [CK_SESSION_HANDLE]
plib.C_Logout.restype = CK_RV

plib.C_CloseSession.argtypes = [CK_SESSION_HANDLE]
plib.C_CloseSession.restype = CK_RV

plib.C_Finalize.argtypes = [CK_VOID_PTR]
plib.C_Finalize.restype = CK_RV


plib.C_GetSlotList.argtypes = [CK_BBOOL,CK_SLOT_ID_PTR,CK_ULONG_PTR]
plib.C_GetSlotList.restype = CK_RV

plib.C_GenerateKey.restype = CK_RV
plib.C_GenerateKey.argtypes = [CK_SESSION_HANDLE,CK_MECHANISM_PTR, CK_ATTRIBUTE_PTR,CK_ULONG, CK_OBJECT_HANDLE_PTR]


plib.C_FindObjectsInit.restype = CK_RV
plib.C_FindObjectsInit.argtypes = [CK_SESSION_HANDLE, CK_ATTRIBUTE_PTR, CK_ULONG]

plib.C_FindObjects.restype = CK_RV
plib.C_FindObjects.argtypes = [CK_SESSION_HANDLE, CK_OBJECT_HANDLE_PTR, CK_ULONG, CK_ULONG_PTR]

plib.C_FindObjectsFinal.restype = CK_RV
plib.C_FindObjectsFinal.argtypes = [CK_SESSION_HANDLE]

plib.C_GetAttributeValue.restype = CK_RV
plib.C_GetAttributeValue.argtypes = [CK_SESSION_HANDLE, CK_OBJECT_HANDLE, CK_ATTRIBUTE_PTR,CK_ULONG]

plib.C_EncryptInit.restype = CK_RV
plib.C_EncryptInit.argtypes = [CK_SESSION_HANDLE, CK_MECHANISM_PTR, CK_OBJECT_HANDLE]

plib.C_Encrypt.restype = CK_RV
plib.C_Encrypt.argtypes = [CK_SESSION_HANDLE, CK_BYTE_PTR, CK_ULONG, CK_BYTE_PTR, CK_ULONG_PTR]

plib.C_DecryptInit.restype = CK_RV
plib.C_DecryptInit.argtypes = [CK_SESSION_HANDLE, CK_MECHANISM_PTR, CK_OBJECT_HANDLE]

plib.C_Decrypt.restype = CK_RV
plib.C_Decrypt.argtypes = [CK_SESSION_HANDLE, CK_BYTE_PTR, CK_ULONG, CK_BYTE_PTR, CK_ULONG_PTR]
