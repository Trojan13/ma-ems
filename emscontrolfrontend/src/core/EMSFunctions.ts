export function generatePacket(
  startByte: number,
  lengthByte: number,
  commandByte: number,
  infoBytes: number[]
): number[] {
  let checksumCalc = startByte + (lengthByte & 255) + (commandByte & 255);

  for (const byte of infoBytes) {
    checksumCalc += byte & 255;
  }

  const checksumBytes = [(checksumCalc >> 8) & 0xff, checksumCalc & 0xff];

  return checksumBytes;
}

export function generateHexPacket(
  startByte: number,
  lengthByte: number,
  commandByte: number,
  infoBytes: number[],
  checksumBytes: number[]
): string {
  const packet = [startByte, lengthByte, commandByte, ...infoBytes, ...checksumBytes];
  console.log(packet);
  return packet.map((byte) => Number(byte).toString(16).padStart(2, '0')).join(' ');
}
