import urllib.request, sys, json, lz4
import zstandard as zstd

# Essential Variables
zones = ['Falcon', 'Canary', 'Finch', 'The Pits', 'Raven', 'Vulture', 'Sparrow', 'Hummingbird']
sources = ['Shield Helper', 'The Lazer Enthusiast', 'Yellow Hunter', 'block - vault', 'giant rubber ball', 'Blue Rusher', 'block - flux node', 'Orange Fool', 'The Shield Master', 'The Coward', 'block - treasure diamond', 'block - iron mine', 'Red Sniper', 'bot - zombie', 'Red Sentry', 'Yellow Mine Guard', 'Aqua Shielder', 'bot - zombie boss', 'bot - zombie hunter', 'bot - zombie tank']
url = "https://pub.drednot.io/prod/econ/2022_11_23/summary.json"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
input_filename = "2022-11-23_summary.bin"
output_filename = "output_test.json"

# Modifications
sys.set_int_max_str_digits(15000)

# Classes
class Vividict(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value

# Functions
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

def readsectionformat(sections):
    decoded = {}
    for section in sections:
        id = int(section[:9],2)
        len = int(section[9:15],2)
        count = int(section[15:len+15],2)
        decoded[str(id)] = count
    return decoded

def readheaders(summary):
    len_ships = int(summary[:4],2)
    ships = int(summary[4:len_ships+4],2)
    len_logs = int(summary[len_ships+4:len_ships+9],2)
    index_final_len = len_ships+9+len_logs
    logs = int(summary[len_ships+9:index_final_len],2)
    return(ships, logs, index_final_len)

def readexisters(summary, start_index):
    # Read held items and transferred (moved) items
    chunk_len_1 = int(summary[start_index:start_index+15],2)
    final_index_1 = start_index + chunk_len_1
    items_held_b = summary[start_index+15:final_index_1]
    items_held = readsectionformat(splitbinsummary(items_held_b))
    chunk_len_2 = int(summary[final_index_1:final_index_1+15],2)
    final_index_2 = final_index_1 + chunk_len_2
    items_moved_b = summary[final_index_1+15:final_index_2]
    items_moved = readsectionformat(splitbinsummary(items_moved_b))
    return items_held, items_moved, final_index_2

def newsplitsections(summary, end_index):
    i = 0
    sections = []
    while i<end_index:
        section = ""
        # Add zone, src, length
        section += summary[i:i+25]
        len_binary = summary[i+9:i+25]
        #section += len_binary
        len_decimal = int(len_binary,2)
        section += summary[i+25:i+25+len_decimal]
        sections.append(section)
        i = i+25+len_decimal
    return sections

def readnewsectionformat(sections):
    items_new = Vividict()
    for section in sections:
        i = 0
        #id_tuple = Vividict()
        # read zone and src
        zone = zones[int(section[:4],2)]
        src = sources[int(section[4:9],2)]
        # remove zone, src, and length aka section header
        section = section[25:]
        len_section = len(section)
        while i < len_section:
            id = int(section[i:i+9],2)
            len_total = int(section[i+9:i+14],2)
            total = int(section[i+14:i+14+len_total],2)
            len_grabbed = int(section[i+14+len_total:i+19+len_total],2)
            grabbed = int(section[i+19+len_total:i+19+len_total+len_grabbed],2)
            items_new[zone][src][id] = (total, grabbed)
            #id_tuple[id] = (total, grabbed)
            i = i+19+len_total+len_grabbed
        #items_new[zone][src] = id_tuple
        #id_tuple.clear()
    return items_new

def outputfilename(input_filename):
    return input_filename[:-3] + "json"

def main():
    print("Enter the filename you would like to decompress: ")
    input_file = input()
    # Uses a Function to generate the output filename
    output_file = outputfilename(input_filename)
    print("Decompressing: " + input_file)
    with open(input_file, "rb") as file:
        zstd_summary = file.read()
    # Compressed with Zstandard
    summary = zstd.decompress(zstd_summary)
    # Converting from bytes-like object to binary bits string
    summary = ''.join(f'{byte:08b}' for byte in summary)
    # Reads upper level schema
    headers = readheaders(summary)
    # Remove headers from summary
    summary = summary[headers[2]:]
    # Reads items_held
    len_held = int(summary[:16],2)
    held_b = summary[16:len_held+16]
    held = readsectionformat(splitbinsummary(held_b))
    summary = summary[len_held+16:]
    # Reads items_moved
    len_moved = int(summary[:16],2)
    moved_b = summary[16:len_moved+16]
    moved = readsectionformat(splitbinsummary(moved_b))
    summary = summary[len_moved+16:]
    # Reads items_new
    len_new = int(summary[:15],2)
    summary = summary[15:]
    new = readnewsectionformat(newsplitsections(summary, len_new))
    # Creates a special dict that doesnt throw an error when
    # I try to nest dicts at keys that dont exist!
    decompressed = Vividict()
    decompressed['count_ships'] = headers[0]
    decompressed['count_logs'] = headers[1]
    decompressed['items_held'] = held
    decompressed['items_moved'] = moved
    decompressed['items_new'] = new
    # Convert dict to json
    decompressed_json = json.dumps(decompressed)
    # Final output
    print("decompression sucess!")
    print("saving output to: " + output_file)
    with open(output_file, "w") as file:
        file.write(decompressed_json)
    print("saved!")
    sys.exit(0)

if __name__ == '__main__':
    main()
