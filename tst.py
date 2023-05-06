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


print("device_state: {0}".format(list(device_state)))

intensity_set_bean = IntensitySetBean(5)
intensity_set_bean_command_byte = intensity_set_bean.get_command_byte()
base_bean = BaseBean(intensity_set_bean_command_byte,device_state)

        # Create a new IntensitySetBean based on the BaseBean instance with the new intensity value
new_intensity = 5

print(base_bean.get_command_byte())
print("base_bean: {0}".format(list(base_bean.get_all_byte())))


print("Intensity set to 5")



print("Finish!")

