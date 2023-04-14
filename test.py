class BaseBean:
    def __init__(self, command_byte, info_byte_array=None, input_byte_array=None):
        self.start_byte = 90
        self.checksum_byte = bytearray(2)
        if input_byte_array is not None:
            if len(input_byte_array) < 5 or input_byte_array[0] != 90:
                raise ValueError("not lt1102s datas")

            self.length_byte = input_byte_array[1]
            self.command_byte = input_byte_array[2]
            i = self.length_byte - 4
            self.info_byte_array = bytearray(i)
            for i2 in range(i):
                self.info_byte_array[i2] = input_byte_array[i2 + 3]

            self.init_checksum()
            if (self.checksum_byte[0] != input_byte_array[-2] or
                    self.checksum_byte[1] != input_byte_array[-1]):
                raise ValueError("checksum error")

        else:
            self.command_byte = command_byte
            self.info_byte_array = bytearray(info_byte_array) if info_byte_array else None
            self.length_byte = len(self.info_byte_array) + 4
            self.init_checksum()

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

class IntensitySetBean(BaseBean):
    COMMAND = 3

    def __init__(self, intensity):
        super().__init__(command_byte=self.COMMAND, info_byte_array=[intensity])

    def get_intensity(self):
        info_byte_array = self.get_info_byte_array()
        if info_byte_array is None or len(info_byte_array) <= 0:
            return -1
        return info_byte_array[0]
    


def main():
    # Create an IntensitySetBean instance
    intensity_set_bean = IntensitySetBean(intensity=5)

    # Get and print the command byte
    command_byte = intensity_set_bean.get_command_byte()
    print(f"Command byte: {command_byte:02X}")

    # Get and print the intensity value
    intensity = intensity_set_bean.get_intensity()
    print(f"Intensity: {intensity}")

    # Print the entire byte array
    intensity_set_bean.print_all_byte()


if __name__ == "__main__":
    main()    