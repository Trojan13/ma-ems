export enum EMSCommand {
  INTENSITY_ADD = 1,
  INTENSITY_CUT = 2,
  INTENSITY_SET = 3,
  PROGRAM_SET = 4,
  INTENSITY_LOCK = 5,
  PROGRAM_PAUSE = 6,
  DEVICE_STATE_READ = 7,
  VERSION_READ = 8,
  INTENSITY_NOTISE = 11,
  CURE_STOP_NOTISE = 12,
  SHUTDOWN = 13
}

export enum EMSConnectionState {
  BLE_STATE_CONNECT_NONE = 0,
  BLE_STATE_CONNECT_CONNECTING = 1,
  BLE_STATE_CONNECT_CONNECTED = 2,
  BLE_STATE_CONNECT_CONNECT_FAIL = 3,
  BLE_STATE_CONNECT_DISCONNECTED = 4
}

export class BLEDeviceState {
  startByte: number
  lengthByte: number
  checksumByte: number[]
  intensity: number
  program: number
  commandByte: number
  electricOverLoad: boolean = false
  mode: number
  cureTimeMinute: number
  battery: number
  cureState: number
  cureTimeSecound: number
  intensityLock: boolean = false

  constructor(arr: number[]) {
    this.startByte = arr[0]
    this.lengthByte = arr[1]
    this.checksumByte = arr[arr.length - 1]

    this.commandByte = 0
    this.electricOverLoad = false
    this.mode = 0
    this.cureTimeMinute = 0
    this.battery = 0
    this.cureState = 0
    this.cureTimeSecound = 0
    this.intensityLock = false

    // Info bytes handling
    if (this.check_checksum(arr)) {
      if (this.startByte === 90) {
        if (this.lengthByte === 5) {
          // If packet length is 5 bytes
          this.intensity = arr[3]
          this.program = arr[2]
        } else if (this.lengthByte === 12) {
          // If packet length is 12 bytes
          this.commandByte = arr[2]
          this.electricOverLoad = arr[3] === 0
          this.program = arr[4]
          this.mode = arr[5]
          this.intensity = arr[6]
          this.cureTimeMinute = arr[7]
          this.battery = arr[8]
          this.cureState = arr[9]
          this.cureTimeSecound = 60 - arr[10]
          this.intensityLock = arr[11] === 0
        } else {
          console.error(this.lengthByte)
          throw new Error(`Invalid packet length: ${this.lengthByte}`)
        }
      } else {
        throw new Error('Invalid packet')
      }
    } else {
      throw new Error('Invalid checksum')
    }
  }

  toString(): string {
    if (this.lengthByte === 5) {
      return `BLEDeviceState(length=${this.lengthByte}, intensity=${this.intensity}, program=${
        this.program
      }, checksumByte=${this.checksumByte.toString()})`
    } else if (this.lengthByte === 12) {
      return `BLEDeviceState(length=${this.lengthByte}, command=${
        this.commandByte
      }, electricOverLoad=${this.electricOverLoad}, program=${this.program}, mode=${
        this.mode
      }, intensity=${this.intensity}, cureTimeMinute=${this.cureTimeMinute}, battery=${
        this.battery
      }, cureState=${this.cureState}, cureTimeSecound=${this.cureTimeSecound}, intensityLock=${
        this.intensityLock
      }, checksumByte=${this.checksumByte.toString()})`
    } else {
      return 'Invalid packet length!'
    }
  }

  private check_checksum(arr: number[]): boolean {
    if (this.checksumByte === undefined) {
      return false
    }
    let checksum_calc = this.startByte + this.lengthByte + this.commandByte
    for (let b of arr) {
      checksum_calc += b
    }

    let checksum_calc_byte1 = (checksum_calc >> 8) & 0xff
    let checksum_calc_byte2 = checksum_calc & 0xff

    if (
      checksum_calc_byte1 !== this.checksumByte[0] &&
      checksum_calc_byte2 !== this.checksumByte[1]
    ) {
      return false
    }
    return true
  }
}
