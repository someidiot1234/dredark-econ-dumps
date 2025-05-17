# Imports
import sys
#sys.path.append(r'C:\Users\unide\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\LocalCache\local-packages\Python313\site-packages')

import urllib.request, json, ast, sys, urllib.error
import zstandard as zstd
from datetime import date, timedelta

# Essential Variables
zones = ['Falcon', 'Canary', 'Finch', 'The Pits', 'Raven', 'Vulture', 'Sparrow', 'Hummingbird']
sources = ['Shield Helper', 'The Lazer Enthusiast', 'Yellow Hunter', 'block - vault', 'giant rubber ball', 'Blue Rusher', 'block - flux node', 'Orange Fool', 'The Shield Master', 'The Coward', 'block - treasure diamond', 'block - iron mine', 'Red Sniper', 'bot - zombie', 'Red Sentry', 'Yellow Mine Guard', 'Aqua Shielder', 'bot - zombie boss', 'bot - zombie hunter', 'bot - zombie tank']
url = "https://pub.drednot.io/prod/econ/2025_4_6/summary.json"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})

# Modifications
sys.set_int_max_str_digits(15000)

# Classes
class Vividict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value

# Functions
def getfilename(url):
    # gets the index of "econ" in the url
    info = url.index("econ")
    unformatted = (url[(info)+5:])[:-5]
    # removes the econ part and the link before it
    # formats name to use underscore instead of slash
    unformatted = unformatted.replace("_", "-")
    formatted = unformatted.replace("/", "_") + ".bin"
    return formatted

def formattobinsection(id, count):
    #format: id, length of count, count
    #format: 9b, 6b, var b
    section = ""
    section += bin(id)[2:].zfill(9)
    countb = bin(count)[2:]
    lenb = bin(len(countb))[2:].zfill(6)
    section += lenb + countb
    return section

def splitbinsummary(summary):
    i = 0
    sections = []
    while i<len(summary):
        section = ""
        section += summary[i:i+9]
        len_binary = summary[i+9:i+15]
        section += len_binary
        len_decimal = int(len_binary, 2)
        section += summary[(i+15):(i+15+len_decimal)]
        sections.append(section)
        i = i+15+len_decimal
    return sections

def ConvertBotToBinSection(bot):
    # convert the bot id tuple set into a binary section
    # section length, id, len total + total, len grabbed + grabbed
    # 16b, 9b, 5b + var b, 5b + var b
    section = ""
    for item in bot:
        # id
        section += bin(item)[2:].zfill(9)
        # total
        total = bin(bot[item][0])[2:]
        # length of total
        len_total_b = bin(len(total))[2:].zfill(5)
        section += len_total_b + total
        # grabbed
        grabbed = bin(bot[item][1])[2:]
        # length of grabbed
        len_grabbed_b = bin(len(grabbed))[2:].zfill(5)
        section += len_grabbed_b + grabbed
    # Get length of the section
    len_section_b = bin(len(section))[2:].zfill(16)
    # pad the section with a 16b long length for decoding
    section = len_section_b + section
    return section

def FormatItemsNew(items_new):
    sorted_new = Vividict()
    for i in range(len(items_new)):
        # for each zone
        for a in range(len(zones)):
            # if that zone is in the item in items new
            if zones[a] == items_new[i]['zone']:          
                # for each source in sources
                for b in range(len(sources)):
                    # if that source is in the item in items new
                    if sources[b] == items_new[i]['src']:
                        # assign to new dict
                        sorted_new[zones[a]][sources[b]][items_new[i]['item']] = (items_new[i]['total'], items_new[i]['grabbed'])
    return sorted_new

def encodeheader(content):
    summary = ""
    # Adds the ship count in format: len of count ships + count ships; 4b + var b
    # Adds log count same way but with 5b for len of count
    ships_binary = bin(content['count_ships'])[2:]
    len_ships_binary = bin(len(ships_binary))[2:].zfill(4)
    summary += (len_ships_binary + ships_binary)
    logs_binary = bin(content['count_logs'])[2:]
    len_logs_binary = bin(len(logs_binary))[2:].zfill(5)
    summary += (len_logs_binary + logs_binary)
    return summary

def bitstring_to_bytes(binary_string):
    if len(binary_string) % 8 != 0:
        padding_length = 8 - (len(binary_string) % 8)
        binary_string += '0' * padding_length
    return bytes(int(binary_string[i:i+8], 2) for i in range(0, len(binary_string), 8))
def compressor(content, compression_level, quiet):
    summary = ""
    # write headers: total ships, logs
    summary += encodeheader(content)

    held = ""
    for item in content['items_held']:
        held += formattobinsection(int(item), content['items_held'][item])
    # add the length of held
    held = bin(len(held))[2:].zfill(16) + held
    summary += held

    moved = ""
    for item in content['items_moved']:
        moved += formattobinsection(int(item), content['items_moved'][item])
    # add the length of moved
    moved = bin(len(moved))[2:].zfill(16) + moved
    summary += moved

    items_new = FormatItemsNew(content['items_new'])
    items_new_summary = ""
    for zone in items_new:
        for bot in items_new[zone]:
            items_new_summary += bin(zones.index(zone))[2:].zfill(4)
            items_new_summary += bin(sources.index(bot))[2:].zfill(5)
            items_new_summary += ConvertBotToBinSection(items_new[zone][bot])
    len_INS = bin(len(items_new_summary))[2:].zfill(15)
    items_new_summary = len_INS + items_new_summary
    summary += items_new_summary
    final_bytes = bitstring_to_bytes(summary)

    summary_size = len(final_bytes)
    cctx = zstd.ZstdCompressor(level=compression_level)  # 1–22, higher = better compression
    zstd_summary = cctx.compress(final_bytes)
    if not quiet:
        zstd_size = len(zstd_summary)
        zstd_compression_ratio = zstd_size / summary_size
        zstd_compression_saving = 100 * (1 - zstd_compression_ratio)
        print(f"Compression ratio: {zstd_compression_ratio:.2f}")
        print(f"Saved: {zstd_compression_saving:.2f}%")
    return zstd_summary
def downloadfile(url, req):
    output_filename = getfilename(url)
    with urllib.request.urlopen(req) as response:
        print("Downloading " + output_filename + " from " + url)
        data = response.read()
        content = json.loads(data)
    zstd_summary = compressor(content, 22, quiet=False)
    with open(output_filename, "wb") as file:
        file.write(zstd_summary)

def main():
    failed_links = ""
    # EDIT THE DATES BELOW BEFORE RUNNING
    sys.exit(1)  # Remove < after you have confirmed lines 170 & 171
    start_date = date(2023, 4, 30)
    end_date = date(2025, 5, 10)
    delta = timedelta(days=1)
    while start_date <= end_date:
        try:
            url = start_date.strftime("https://pub.drednot.io/prod/econ/%Y_%m_%d/summary.json")
            url = url.replace('_0', '_')
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
            downloadfile(url, req)
        except (urllib.error.HTTPError, urllib.error.URLError):
            failed_links += url + "\n"
        start_date += delta
    with open("failed_links.txt", "w", encoding="utf-8") as file:
        file.write(failed_links)
    #url = "https://pub.drednot.io/prod/econ/2025_4_6/summary.json"

    
    #print(summary)
    print("completed sucessfully!")
    sys.exit(0)

if __name__ == '__main__':
    main()