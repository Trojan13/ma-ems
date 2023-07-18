t = "5a 05 01 00 00 60"

print(bytes.fromhex(t))
byte_array = bytearray.fromhex(t.replace(" ", ""))
print(byte_array)
print(bytearray([0x5a, 0x05, 0x01, 0x00, 0x00, 0x60]))
print(bytearray(int(x, 16) for x in t.split()))