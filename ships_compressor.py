#!/usr/bin/env python
import json
import zstandard as zstd
url = ""
def utf8tobin(u):
    # format as 8-digit binary, join each byte with space
    return ''.join([f'{i:08b}' for i in u.encode()])
def bitstring_to_bytes(b): 
    remainder = 8-(len(b)+3)%8
    #print(remainder)
    b=(bin(remainder)[2:].zfill(3)+b) + remainder * "0"
    return int(b.ljust((len(b) + 7) // 8 * 8, '0'), 2).to_bytes((len(b) + 7) // 8, 'big')
def converttobinsection(section):
    #3b hex len, 5b name len, 24b color, items:
    #9b of id count 9b id, 5b count len
    output = ""
    hexa = section['hex_code']
    hexa_b = bin(int(hexa,16))[2:].zfill(len(hexa)*4)
    output += bin(len(hexa)-4)[2:].zfill(3) + hexa_b
    name = section['name']
    name_b = utf8tobin(name)
    color_b = bin(section['color'])[2:].zfill(24)
    output+=bin(int(len(name_b)/8))[2:].zfill(7)+name_b+color_b
    items = []
    count_ids=0
    for id in section['items']:
        id_b = bin(int(id))[2:].zfill(9)
        count_b = bin(section['items'][id])[2:]
        items.append((id_b+bin(len(count_b))[2:].zfill(5)+count_b))
        count_ids+=1
    output += bin(count_ids)[2:].zfill(9)
    for item in items:
        output+=item
    return output
def compressdata(data, compression_level, quiet):
    final = ""
    for section in data:
        final+=converttobinsection(section)
    final_bytes = bitstring_to_bytes(final)
    summary_size = len(final_bytes)
    cctx = zstd.ZstdCompressor(level=compression_level)  # 1–22, higher = better compression
    zstd_ships = cctx.compress(final_bytes)
    if not quiet:
        zstd_size = len(zstd_ships)
        zstd_compression_ratio = zstd_size / summary_size
        zstd_compression_saving = 100 * (1 - zstd_compression_ratio)
        print(f"Compression ratio: {zstd_compression_ratio:.2f}")
        print(f"Saved: {zstd_compression_saving:.2f}%")
    return zstd_ships
def main(input_filename, compressed_filename):
    with open(input_filename, "r", encoding="utf-8") as file: # READ SHIPS JSON
        data = json.loads(file.read())
    with open(compressed_filename, "wb") as file: # WRITE BINARY
        file.write(compressdata(data, 19, quiet=False))

if __name__ == "__main__":
    main()