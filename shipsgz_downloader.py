import urllib.request, sys, os, math, urllib.error
from datetime import date, timedelta

def getfilename(url):
    # gets the index of "econ" in the url
    info = url.index("econ")
    # removes the econ part and the link before it
    unformatted = (url[(info)+5:])
    # formats name to use underscore instead of slash
    unformatted = unformatted.replace("_", "-")
    formatted = unformatted.replace("/", "_")
    return formatted

def getsize(path):
   size_bytes = os.path.getsize(path)
   if size_bytes == 0:
       return "0 B"
   size_name = ("","k","m","g","t","p","e","z","y","r","q")
   i = int(math.floor(math.log(size_bytes, 1000)))
   p = math.pow(1000, i)
   s = round(size_bytes / p, 1)
   output = str(s) + " " + size_name[i] + "B"
   return output

def main():
    failed_links = ""
    # EDIT THE DATES BELOW BEFORE RUNNING
    #sys.exit(1)  # Remove < after you have confirmed lines 29 & 30
    start_date = date(2022, 11, 23)
    end_date = date(2025, 7, 1)
    delta = timedelta(days=1)
    counter = 1
    while start_date <= end_date:
        url = start_date.strftime("https://pub.drednot.io/prod/econ/%Y_%m_%d/ships.json.gz")
        url = url.replace('_0', '_')
        output_filename = getfilename(url)
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
            with urllib.request.urlopen(req) as response:
                data = response.read()
            with open(output_filename, "wb") as f:
                f.write(data)
            print("Get:" + str(counter) + " " + url + " " + output_filename + " [" + getsize(output_filename) + "]")
        except (urllib.error.HTTPError, urllib.error.URLError):
            failed_links += url + "\n"
            print("Miss:" + str(counter) + " " + url + " " + output_filename)
        start_date += delta
        counter += 1
    with open("failed_links.txt", "w", encoding="utf-8") as file:
        file.write(failed_links)
    print("Completed sucessfully!")
    sys.exit(0)

if __name__ == "__main__":
    main()
