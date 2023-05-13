class BLEDeviceState:
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
                    raise ValueError("Invalid packet length: " + self.lengthByte)
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
