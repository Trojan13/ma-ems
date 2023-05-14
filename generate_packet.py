
def generate_packet(command_byte, info_bytes,debug=False):
    start_byte = 0x5a
    length_byte = len(info_bytes) + 4  # Include start_byte, length_byte, command_byte in length
    checksum_calc = start_byte + length_byte + command_byte

    for byte in info_bytes:
        checksum_calc += byte

    checksum_bytes = [(checksum_calc >> 8) & 0xFF, checksum_calc & 0xFF]

    packet = [start_byte, length_byte, command_byte] + info_bytes + checksum_bytes

    if debug:
        print_packet = ["0x{:02x}".format(byte) for byte in packet]
        print(", ".join(print_packet))

    return bytearray(packet)

#command_bytes = 0x02
#info_bytes = [0x00]
#packet = generate_packet(command_bytes, info_bytes)
#print(packet)