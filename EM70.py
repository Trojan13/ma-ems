import json


class ConnectionState():
    BLE_STATE_CONNECT_NONE = 0
    BLE_STATE_CONNECT_CONNECTING = 1
    BLE_STATE_CONNECT_CONNECTED = 2
    BLE_STATE_CONNECT_CONNECT_FAIL = 3
    BLE_STATE_CONNECT_DISCONNECTED = 4


class Command():
    INTENSITY_ADD = 1
    INTENSITY_CUT = 2
    INTENSITY_SET = 3
    PROGRAM_SET = 4
    INTENSITY_LOCK = 5
    PROGRAM_PAUSE = 6
    DEVICE_STATE_READ = 7
    VERSION_READ = 8
    INTENSITY_NOTISE = 11
    CURE_STOP_NOTISE = 12
    SHUTDOWN = 13


class DeviceState:
    def __init__(self, arr):
        self.startByte = arr[0]
        self.lengthByte = arr[1]
        self.checksumByte = arr[-1]

        # Info bytes handling
        if self.check_checksum:
            if self.startByte == 90:
                if self.lengthByte == 5:  # If packet length is 5 bytes
                    self.intensity = arr[3]
                    self.program = arr[2]
                elif self.lengthByte == 12:  # If packet length is 12 bytes
                    self.commandByte = arr[2]
                    self.electricOverLoad = arr[3] == 0
                    self.program = arr[4]
                    self.mode = arr[5]
                    self.intensity = arr[6]
                    self.cureTimeMinute = arr[7]
                    self.battery = arr[8]
                    self.cureState = arr[9]
                    self.cureTimeSecound = 60 - arr[10]
                    self.intensityLock = arr[11] == 0
                else:
                    print(self.lengthByte)
                    raise ValueError(
                        "Invalid packet length: " + self.lengthByte)
            else:
                raise ValueError("Invalid packet!")
        else:
            raise ValueError("Invalid checksum!")

    def __str__(self):
        if self.lengthByte == 5:
            return f"BLEDeviceState(length={self.lengthByte}, intensity={self.intensity}, program={self.program}, checksumByte={hex(self.checksumByte)})"
        elif self.lengthByte == 12:
            return f"BLEDeviceStatelength={self.lengthByte}, command={self.commandByte}, electricOverLoad={self.electricOverLoad}, program={self.program}, mode={self.mode}, intensity={self.intensity}, cureTimeMinute={self.cureTimeMinute}, battery={self.battery}, cureState={self.cureState}, cureTimeSecound={self.cureTimeSecound}, intensityLock={self.intensityLock}, checksumByte={hex(self.checksumByte)})"
        else:
            return "Invalid packet length!"

    def check_checksum(self):
        checksum_calc = self.start_byte + self.length_byte + self.command_byte
        for b in self.info_bytes:
            checksum_calc += b

        checksum_calc_byte1 = (checksum_calc >> 8) & 0xFF
        checksum_calc_byte2 = checksum_calc & 0xFF

        if [checksum_calc_byte1, checksum_calc_byte2] != self.checksum_bytes:
            print("Warning: Checksum does not match calculated value.")
            return False
        return True

    def get_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def set_electriy_over_load(self, value):
        self.electricOverLoad = value

    def set_program(self, program):
        self.program = program

    def set_mode(self, mode):
        self.mode = mode

    def set_intensity(self, intensity):
        self.intensity = intensity

    def set_cure_time_minute(self, cure_time_minute):
        self.cureTimeMinute = cure_time_minute

    def set_battery(self, battery):
        self.battery = battery

    def set_cure_state(self, cure_state):
        self.cureState = cure_state

    def set_cure_time_secound(self, cure_time_secound):
        self.cureTimeSecound = cure_time_secound

    def set_intensity_lock(self, intensity_lock):
        self.intensityLock = intensity_lock


# command_bytes = 0x02
# info_bytes = [0x00]
# packet = generate_packet(command_bytes, info_bytes)
# print(packet)
def generate_packet(command_byte, info_bytes, debug=False):
    start_byte = 0x5a
    # Include start_byte, length_byte, command_byte in length
    length_byte = len(info_bytes) + 4
    checksum_calc = start_byte + length_byte + command_byte

    for byte in info_bytes:
        checksum_calc += byte

    checksum_bytes = [(checksum_calc >> 8) & 0xFF, checksum_calc & 0xFF]

    packet = [start_byte, length_byte, command_byte] + \
        info_bytes + checksum_bytes

    if debug:
        print_packet = ["0x{:02x}".format(byte) for byte in packet]
        print(", ".join(print_packet))

    return bytearray(packet)


def validate_packet(packet: str) -> bool:
    # Split the packet into bytes
    bytes_list = packet.split(" ")

    # Check if the packet starts with "5A"
    if bytes_list[0] != "5A":
        return False

    # Check if the packet has a minimum length of 6 bytes
    if len(bytes_list) < 6:
        return False

    # Check if the length byte matches the number of info bytes
    length_byte = int(bytes_list[1], 16)
    # Exclude start byte, length byte, command byte, and two checksum bytes
    info_bytes = bytes_list[3:-2]
    if length_byte != len(info_bytes):
        return False

    # If all checks pass, the packet is valid
    return True
