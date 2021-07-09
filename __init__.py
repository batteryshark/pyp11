from .types import *
from .defs import *
from .bindings import *


# TEST CODE
if __name__ == "__main__":
    import ctypes,binascii

    USER_PIN = b"000000"
    USER_PIN_LENGTH = len(USER_PIN)    
    # Init The Library [Once Per Application]
    res = plib.C_Initialize(None)
    print(f"C_Initialize Result: {res:#04x}")

    num_slots = CK_ULONG(0)
    res = plib.C_GetSlotList(1,None,byref(num_slots))
    print(f"C_GetSlotList Result: {res} num slots: {num_slots.value}")

    slot_ids = (CK_ULONG * num_slots.value)(0)
    res = plib.C_GetSlotList(1,slot_ids,byref(num_slots))
    print(f"C_GetSlotList Result: {res} slot 0 index: {slot_ids[0]}")

    # Init the Session [Generally Once]
    h_session = ctypes.c_ulong(0)
    res = plib.C_OpenSession(slot_ids[0],CKF_SERIAL_SESSION | CKF_RW_SESSION,None,None,ctypes.byref(h_session))
    print(f"C_OpenSession Result: {res}, h_session {h_session.value:#04x}")

    # Log into our session as a user
    res = plib.C_Login(h_session,CKU_USER,USER_PIN,USER_PIN_LENGTH)
    print(f"C_Login Result: {res}")
    
    # Get some random
    #rdata = (ctypes.c_ubyte * 32)()
    #res = plib.C_GenerateRandom(h_session,rdata,32)
    #print(f"C_GenerateRandom Result: {res:#04x} Data: {len(rdata)} bytes: {binascii.hexlify(rdata)}")

    """
    yes = CK_BBOOL(1)
    no  = CK_BBOOL(0)
    s_key_label = b"RFX_HMK"
    key_label = (CK_BYTE * len(s_key_label)).from_buffer_copy(s_key_label)
    value_len = CK_ULONG_32(32)
    key_class = CK_ULONG_32(CKO_SECRET_KEY)
    key_type = CK_ULONG_32(CKK_AES)
    alst = [0x10, 0x11, 0x18, 0x99]
    algo_lst = (CK_BYTE * len(alst)).from_buffer_copy(bytes(alst))

    attrs_table = [
        [CKA_CLASS,byref(key_class),sizeof(CK_ULONG_32)],
        [CKA_KEY_TYPE,byref(key_type),sizeof(CK_ULONG_32)],	
        [CKA_TOKEN,byref(yes),sizeof(CK_BBOOL)],
        [CKA_PRIVATE,byref(yes),sizeof(CK_BBOOL)],
        [CKA_LABEL,byref(key_label),len(key_label)],
        [CKA_ENCRYPT,byref(yes),sizeof(CK_BBOOL)],
        [CKA_DECRYPT,byref(yes),sizeof(CK_BBOOL)],
        [CKA_DERIVE,byref(yes),sizeof(CK_BBOOL)],
        [CKA_SC_HSM_ALGORITHM_LIST,byref(algo_lst),len(alst)],
        [CKA_VALUE_LEN,byref(value_len),sizeof(CK_ULONG_32)],
    ]

    pmech =  CK_ATTRIBUTE()
    pmech.attr_type = CKM_AES_KEY_GEN
    pmech.attr_value = c_void_p(0)
    pmech.attr_length = 0



    attrs = (CK_ATTRIBUTE * len(attrs_table))()
    sa = ctypes.cast(attrs,ctypes.POINTER(CK_ATTRIBUTE))

    for i in range(0,len(attrs_table)):
        sa[i].attr_type = attrs_table[i][0]
        sa[i].attr_value = cast(attrs_table[i][1],c_void_p)
        sa[i].attr_length = attrs_table[i][2]
        print(bytearray(sa[i]))

    # Create Our Key
    h_object = ctypes.c_ulong(0)
    res = plib.C_GenerateKey(h_session,byref(pmech),attrs,len(attrs_table),byref(h_object))
    print(f"C_GenerateKey Result: {res}, h_object {h_object.value:#04x}")
    """

    def bchr(s):
        return bytes([s])
    def bord(s):
        return s	

    def unpad_data(indata,block_size=16):
        pdata_len = len(indata)
        padding_len = bord(indata[-1])
        return indata[:-padding_len]

    def pad_data(indata,block_size=16):
        padding_len = block_size-len(indata)%block_size
        padding = bchr(padding_len)*padding_len
        return indata + padding

    res = plib.C_FindObjectsInit(h_session,None,0)
    print(f"C_FindObjectsInit Result: {res}")

    max_count = 256
    found_count = CK_ULONG(0)
    ph_object = (CK_OBJECT_HANDLE * max_count)()
    res = plib.C_FindObjects(h_session,ph_object,max_count,byref(found_count))
    print(f"C_FindObjects res: {res} found: {found_count.value}")

    for i in range(0,found_count.value):
        p_labl = (c_char_p * 32)()
        p_labl_len = 32
        ptmp_table = [
        [CKA_LABEL,byref(p_labl),p_labl_len]
        ]
        ptmp = (CK_ATTRIBUTE * len(ptmp_table))()
        for j in range(0,len(ptmp_table)):
            ptmp[j].attr_type = ptmp_table[j][0]
            ptmp[j].attr_value = cast(ptmp_table[j][1],c_void_p)
            ptmp[j].attr_length = ptmp_table[j][2]		
        res = plib.C_GetAttributeValue(h_session,ph_object[i],ptmp,len(ptmp_table))
        label = cast(ptmp[0].attr_value,c_char_p).value
        print(f"C_GetAttributeValue res: {res} Label: {label}")

    # AES Encrypt
    iv_data = b"\x00\x01\x00\x01\x00\x02\x00\x02\x03\x04\x05\x03\x02\x01\x01\x00"
    c_iv_data = (CK_BYTE * len(iv_data)).from_buffer_copy(iv_data)

    pmech = CK_MECHANISM(CKM_AES_CBC,cast(c_iv_data,c_void_p),16)
    res = plib.C_EncryptInit(h_session,byref(pmech),3)
    print(f"C_EncryptInit Result: {res}")

    in_data = b"HELLO WORLD!"
    in_data = pad_data(in_data)
    c_in_data = (CK_BYTE * len(in_data)).from_buffer_copy(in_data)

    c_out_data = (CK_BYTE * len(in_data))()
    out_len = CK_ULONG(len(c_out_data))
    res = plib.C_Encrypt(h_session, c_in_data,len(in_data),c_out_data,byref(out_len))
    print(f" C_Encrypt res: {res:#04x} out_data: {binascii.hexlify(bytearray(c_out_data)[:out_len.value])}")

    res = plib.C_DecryptInit(h_session,byref(pmech),3)
    print(f"C_DecryptInit Result: {res}")

    c_pt_data = (CK_BYTE * len(in_data))()
    pt_len = CK_ULONG(len(c_pt_data))
    res = plib.C_Decrypt(h_session, c_out_data,out_len.value,c_pt_data,byref(pt_len))
    pt_data = unpad_data(bytearray(c_pt_data))
    print(f" C_Decrypt res: {res:#04x} pt_data: {binascii.hexlify(pt_data)}")
    print(pt_data)

    # Log out of our session
    res = plib.C_Logout(h_session)
    print(f"C_Logout Result: {res}")

    # Close the Session [Generally Once]
    res = plib.C_CloseSession(h_session)
    print(f"C_CloseSession Result: {res}")


    # Finalize the Library [Once Per Application]
    res = plib.C_Finalize(None)
    print(f"C_Finalize Result: {res:#04x}")    