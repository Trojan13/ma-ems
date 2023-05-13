import asyncio



ADDRESS = "F9:8B:6F:12:EC:AE"
CHARACTERISTICS = "64668730-033f-9393-6ca2-0e9401adeb32"


class BaseBean:
    def __init__(self, b, bArr):
        self.start_byte = 0x5A
        length =  bArr.length
        if length < 5 or bArr[0] != self.start_byte:
            raise ValueError("not lt1102s datas")
        b = bArr[1]
        self.length_byte = b
        self.command_byte = bArr[2]
        i = self.length_byte - 4
        self.info_byte_array = bytearray(i)
        for i2 in range(i):
            self.info_byte_array[i2] = bArr[i2 + 3]
        self.init_checksum()
        bArr2 = self.checksum_byte
        if bArr2[0] != bArr[-2] or bArr2[1] != bArr[-1]:
            raise ValueError("checksum error")
        

    def get_command_byte(self):
        return self.command_byte

    def get_info_byte_array(self):
        return self.info_byte_array

    def byte_array_to_string(self, byte_array):
        return "  ".join("{:02x}".format(b & 255) for b in byte_array)

    def get_all_byte(self):
        length = len(self.info_byte_array) + 5
        byte_array = bytearray(length)
        byte_array[0] = 90
        byte_array[1] = self.length_byte
        byte_array[2] = self.command_byte
        i = 0
        while i < len(self.info_byte_array):
            byte_array[i + 3] = self.info_byte_array[i]
            i += 1
        byte_array[length - 2] = self.checksum_byte[0]
        byte_array[length - 1] = self.checksum_byte[1]
        return byte_array

    def print_all_byte(self):
        byte_array = self.get_all_byte()
        print(" ".join("{:02X}".format(b) for b in byte_array))
        print(byte_array)

    def get_length(self):
        return len(self.get_all_byte())

    def init_checksum(self):
        i = 90 + (self.length_byte & 255) + (self.command_byte & 255)
        if self.info_byte_array is not None:
            for b in self.info_byte_array:
                i += b & 255
        self.checksum_byte[0] = (i >> 8) & 255
        self.checksum_byte[1] = i & 255
class IntensitySetBean:
    COMMAND = 3

    def __init__(self, i: int):
        self._info_byte_array = bytearray([i])

    def get_intensity(self) -> int:
        if not self._info_byte_array or len(self._info_byte_array) <= 0:
            return -1
        return self._info_byte_array[0]


device_state = [0x5a, 0x05, 0x07, 0x00, 0x00, 0x66]

def generate_checksum(length_byte, command_byte, info_byte_array):
    total = 90 + length_byte + command_byte
    for b in info_byte_array:
        total += b

<<<<<<< Updated upstream
print("device_state: {0}".format(list(device_state)))

intensity_set_bean = IntensitySetBean(5)
intensity_set_bean_command_byte = intensity_set_bean.get_command_byte()
base_bean = BaseBean(intensity_set_bean_command_byte,device_state)

        # Create a new IntensitySetBean based on the BaseBean instance with the new intensity value
new_intensity = 5
=======
    checksum_byte_0 = (total >> 8) & 255
    checksum_byte_1 = total & 255

    return (checksum_byte_0, checksum_byte_1)

length_byte = 10
command_byte = 5
info_byte_array = [1, 2, 3, 4, 5, 6, 7, 8]

checksum_byte_0, checksum_byte_1 = generate_checksum(length_byte, command_byte, info_byte_array)
print("Checksum bytes:", checksum_byte_0, checksum_byte_1)
>>>>>>> Stashed changes

print(base_bean.get_command_byte())
print("base_bean: {0}".format(list(base_bean.get_all_byte())))

<<<<<<< Updated upstream
=======
intensity_set_bean = IntensitySetBean(intensity=5)
print(intensity_set_bean.get_command_byte())
print(list(intensity_set_bean.get_all_byte()))
base_bean = BaseBean(intensity_set_bean.get_command_byte(),input_byte_array=device_state)
>>>>>>> Stashed changes

print("Intensity set to 5")


input_byte_array = [90, 5, 3, 5, 0, 103]
i = len(input_byte_array) - 4
info_byte_array = bytearray(i)
for i2 in range(i):
   info_byte_array[i2] = input_byte_array[i2 + 3]

print(list(info_byte_array))

