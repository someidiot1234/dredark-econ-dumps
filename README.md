# shipsgz-reader
MD5: 0eb114325e7e7de1a7103e1ea21332b3\
SHA256: 0eecbe0741ee9e73c47f591512a1c49ff57da14f727110f14ba8bcebf57c308c\
Downloads the shipsgz file at inputted date and returns the information of a specified hex code.
if not working, make sure that the days and months inputted have no leading zeros.

# shipsgz-compressor
MD5: 9687db76128aebb1975a6e04e773caad\
SHA256: 8ec6d0850db3ddacbd0ecf2341d84abacfbade2ab1a3104a0d2fb5405f9f407c\
Compressing and Decompressing https://pub.drednot.io/econ/prod/DAY_MONTH_YEAR/ships.json.gz \
input filename, compressed filename, output filename are NOT specified.\
filename function I made:\
def getfilename(url):\
    # gets the index of "econ" in the url\
    info = url.index("econ")\
    unformatted = (url[(info)+5:])[:-5]\
    # removes the econ part and the link before it formats the name to use underscore instead of slash\
    unformatted = unformatted.replace("\_", "-")\
    formatted = unformatted.replace("/", "_") + ".bin"\
    return formatted
    
# summary downloader/compressor
MD5: 6d7d02d2138f89f2d264f162b7f6e3a3\
SHA256: faa534e7b8d002b023a8e36163491813c7b055d22f75ce9457919b4dc4f5a0ac\
Downloading and Compressing https://pub.drednot.io/econ/prod/DAY_MONTH_YEAR/summary.json \
PLEASE specify the date range you would like to download on lines 170 & 171

# summary reader
MD5: 0edae08638862e3530a8e0c52e157b9f\
SHA256: 70a46c9225aa8a1ea25dac0ec3408c76239729eff73960a3fbf8fba9810e3c57\
Decompresses the files made by the summary compressor.\
Takes input as filename in terminal. Saves output as json.\
Schema:\
total_ships - 15 bit integer\
total_logs - 31 bit integer\
items_held - an object that stores all new items created during that day.\
Maps id (9 bit integer stored as string) to count (63 bit integer)\
____items_grabbed - same as items_held\
items_new - an object that stores zone, source, and id:[total, grabbed]\
____"Zone":{"Bot":{"id":[total,grabbed]}}\
____id is a 9 bit integer, total/grabbed are 31 bit integers

# summary files
MD5: b960dc16d45fb0029173acc8246e441b\
SHA256: 2b609263d0513751580ce2c86dbe9446c9d7a7b589be8e43f7a04c604ca06855\
A folder that contains all summary files from November 23rd 2022 to May 10th 2025

# networth grapher
MD5: 9f99e1e672446683880d58d46cfb0d2b\
SHA256: 9859c03e7bcc04bc070908b439fcb675246fe5dd0e9ddcac09dad90a124e1b67\
Graphs the combined networth of ships you own over a time period.\
Defaults Nov. 23, 2022 to Jul. 1st, 2025.\
Make a file titled 'shiplist.json' and paste your shiplist into it.\
Shiplist link: https://drednot.io/shiplist?server=0 \
PLEASE specify the date range you would like to download on lines 67 & 68\
Dependencies:
shiplist.json, item_conversions.json, YYYY-MM-DD_ships.json.gz (leading zeros must be ommited).

# item conversions
MD5: c42e53ce012d482412e04f588009b378\
SHA256: 1f464330aeb7a0ff1acdbc7f34fca149990130d3467ede87a0082ed861290a69\
A json file that maps item ids to how many of that item will be worth 16 flux (npsf).\
The npsf column will also contain 'inf' aka 0 value for starters, and 'no value' for certain rares.\
Required to use the networth grapher.

# ships downloader
MD5: 456803aa91cb4b4ce733d3474ef98095\
SHA256: 3d96681f64b5bed3becea10af0ab4b01f9212bef58c49dcce8c586c34a522ec6\
Downloads all ships.json.gz files over a time period.\
Defaults Nov. 23, 2022 to Jul. 1st, 2025.\
Can be configured to download any econ dumps file. To do this, edit the link on line 34.\
PLEASE specify the date range you would like to download on lines 29 & 30

# shipsgz files (backup- please download from drednot.io directly)
A folder that contains folders of all ships files from November 23rd 2022 to Jul. 1st 2025.\
Seperated by Quarter and Year.\
Q1: Jan. 1st to Mar. 31st\
Q2: May 1st to Jun. 30th\
Q3: Jul. 1st to Sep. 30th\
Q4: Oct. 1st to Dec. 31st
### shipsgz_2022-Q4.zip
MD5: 53b0608126029904bcf700531733167c\
SHA256: 87049c835adaddc7cb5447e8073d7a64e8a524987f536d40ebd4a2c2a28fd43c
### shipsgz_2023-Q1.zip
MD5: 7d18ca9ffcfb24d1f9c906d94f65badf\
SHA256: 758743c5b96b21ae778eac4b846b675ea360658ee238f7c21bea6bd85db9c17f
### shipsgz_2023-Q2.zip
MD5: c34185192a95bf0011549b041f84bc70\
SHA256: 6569ee2bce0131598f72eef18f4445ffd64b89452b6b82a4ce245adc6772f091
### shipsgz_2023-Q3.zip
MD5: eaf91ee88da3ee5ec113f307101b20c7\
SHA256: fe8cf2a2271ebba31d345fbdec45cbc1c65b7b6b64ec03a4c81a3ff4b23ef2c7
### shipsgz_2023-Q4.zip
MD5: 5b20ded649dc81e84a16dabe58e8d022\
SHA256: 9a68ea10da40fd9028800b78e066784000c9fda48f856c81cbd173f66176d417
### shipsgz_2024-Q1.zip
MD5: 5c6355aa1b6527f5ecd7107a01902551\
SHA256: 58dae306d1b320488e67256f36f68088df2e6d39c919efa36c4852fdbba0b611
### shipsgz_2024-Q2.zip
MD5: f06b7291c88c4a1b9d6142f57ea34c9d\
SHA256: 69aa750be7d9805c73d30f580086ac4ea9524a5a55b1f82f6a0c051604403a66
### shipsgz_2024-Q3.zip
MD5: 0a45b0f67a0e91bb9f15ff815d585e78\
SHA256: 36fc5d75091c041b5afa7db95814be0f7c5bcb1b902240f5dda3959716f63181
### shipsgz_2024-Q4.zip
MD5: b64e5c22d056cc17e51cb911b0ac94e8\
SHA256: 559a49a5f85c861c9350cb79b1bdf8e8bc253b42ea2b440cdf6b0fdb731bfd0b
### shipsgz_2025-Q1.zip
MD5: fa529773647222e05efffb9c1593e0a7\
SHA256: 00d453609f984521d35fd45dbc193d6600137469cfaee096253d6fed5f667afc
### shipsgz_2025-Q2.zip
MD5: e23c385022f62e913de10b10867d86d6\
SHA256: 9cbc0c2594944515a38212db40cb718dab590b08ef829b4dd26d6f5bce1463c3
### shipsgz_2025-Q3.zip
MD5: c380386d521b02bc6aed4385568f1974\
SHA256: edc887421f558415c7826ccc7801e984b7802273adc1d7f07853259ef85d3d34

\
Have fun!
