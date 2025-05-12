import json, gzip, sys, urllib, urllib.error
import urllib.request
def main():
    print("Enter the date of the file you want:")
    print("Format: YYYY_M_D")
    date = input()
    with urllib.request.urlopen(urllib.request.Request("https://pub.drednot.io/prod/econ/"+date+"/ships.json.gz", headers={"User-Agent": "_ANY_USER"})) as response:
        file = gzip.decompress(response.read())
        data = json.loads(file)
    print("Target ID: ")
    target_id = input()
    for ship in data:
        if ship['hex_code'] == target_id:
            print(ship)
    sys.exit(0)
if __name__ == "__main__":
    main()