#!/usr/bin/env python
import json
import zstandard as zstd
url = ""
# Classes
class Vividict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value
def bin_to_utf8(b): 
    return int(b, 2).to_bytes(len(b) // 8, 'big').decode('utf-8')
def bytes_to_bitstring(data):
    data = ''.join(format(byte, '08b') for byte in data)
    remainder = int(data[:3],2)
    data = data[3:]
    data = data[:-remainder]
    return data
def decodesection(sectiona, i):
    #3b hex len, 5b name len, 24b color, items:
    #9b id lens, 9b id, 5b count len
    output = {}
    hex_len = 4*(int(sectiona[i:i+3],2)+4)
    #print(hex_len)
    i+=3
    hexa = "{"+hex(int(sectiona[i:i+hex_len],2))[2:].upper() + "}"
    #print(hexa)
    i+=hex_len
    #print(sectiona[:3])
    #print(hexa)
    name = bin_to_utf8(sectiona[i+7:i+7+int(sectiona[i:i+7],2)*8])
    i+=7+int(sectiona[i:i+7],2)*8
    color = int(sectiona[i:i+24],2)
    output['hex_code'] = hexa
    output['name'] = name
    output['color'] = color
    i+=24
    len_items = int(sectiona[i:i+9],2)
    i+=9
    item_counter = 0
    while item_counter<len_items:
        id = int(sectiona[i:i+9],2)
        len_count = int(sectiona[i+9:i+14],2)
        count = int(sectiona[i+14:i+14+len_count],2)
        output[str(id)] = count
        i+=14+len_count
        item_counter+=1
    return output, i
def decompressdata(data):
    dctx = zstd.ZstdDecompressor()
    decompressed = dctx.decompress(data)
    data = bytes_to_bitstring(decompressed)
    ships = Vividict()
    i=0
    number = 0
    while i<len(data):
        part = decodesection(data, i)
        i=part[1]
        ships[number] = part[0]
        number += 1
    return ships
def main(compressed_filename, output_filename):
    #"comp_ships_04_06_2025.bin" "badname.json"
    with open(compressed_filename, "rb") as file: # READ BINARY
        data = file.read()
    with open(output_filename, "w", encoding="utf-8") as file: # WRITE SHIPS JSON
        file.write(json.dumps(decompressdata(data), ensure_ascii=False))

if __name__ == "__main__":
    main()