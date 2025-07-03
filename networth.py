# Imports
from matplotlib import pyplot as plt
from datetime import date, timedelta
import sys, json, gzip
import numpy as np

# Classes
class Vividict(dict):
    # Fancy dictionary
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value

# Functions
def networth(items):
    # Calculates networth of a id:count list using a pricing list
    networth = 0
    with open("item_conversions.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    # item_conversions.json is formatted as id:npsf
    # npsf = number per stack of flux
    # Ex. 512 iron per stack of flux, so "1":"512"
    for item in items:
        # Reading item prices
        if data[item] == "NaN":
            print("Test-Only Item. Skipped. id is " + str(item))
        elif data[item] == "inf":
            # starter & debug items have no value
            networth += 0
        elif data[item] == "no value":
            # eternals, I don't have pricing info
            print("Rare Item with no market history. id is " + str(item))
        else:
            networth += int(items[item])/(float(data[item])/16)
    return networth

def formatshiplist(shiplist):
    # Converts a shiplist json into a list of the hex ids
    # filters for ships that haved 'owned' set to "True"
    output = []
    for ship in shiplist['ships']:
        obj = shiplist['ships'][ship]
        if obj['owned']:
            output.append(obj['hex_code'])
    return output

def netstoplottable(days, shiplist):
    # Converts the days object into a plottable object
    # days is the networth of each ship you loaded every day
    # output is the days networth every day you loaded a ship
    latest_networth = Vividict()
    output = Vividict()
    for hex in shiplist:
        latest_networth[hex] = 0
    for day in days:
        count = 0
        for ship in days[day]:
            latest_networth[ship] = days[day][ship]
        for networth in latest_networth:
            count += latest_networth[networth]
        output[day] = count
    return output

def main():
    # EDIT THE DATES BELOW BEFORE RUNNING
    #sys.exit(1)  # Remove < after you have confirmed lines 67 & 68
    start_date = date(2022, 11, 23)
    end_date = date(2025, 7, 1)
    delta = timedelta(days=1)
    # Reading your shiplist
    with open("shiplist.json", "r", encoding="utf-8") as f:
        shiplist = formatshiplist(json.load(f))
    # Iterating through dates
    days = Vividict()
    while start_date <= end_date:
        # Calculating the input filename
        filename = start_date.strftime("%Y-%m-%d_ships.json.gz").replace('-0', '-')
        day = Vividict()
        # Reading and Decompressing the file
        with gzip.open(filename, "rb") as f:
            data = json.load(f)
        for item in data:
            if item['hex_code'] in shiplist:
                day[item['hex_code']] = networth(item['items'])
        days[start_date] = day
        start_date += delta
    # converting the days object into a plottable object
    networths = netstoplottable(days, shiplist)
    # dividing the networths object into x and y values
    times = []
    nets = []
    for worth in networths:
        times.append(worth)
        nets.append(networths[worth])
    # Matplotlib plotting
    plt.plot(times, nets)
    # Axis labels
    plt.xlabel("Date")
    plt.ylabel("Networth (Flux)")
    # Axis scaling (otherwise every day will have a tick mark)
    ax = plt.gca()
    xmin, xmax = ax.get_xlim()
    custom_ticks = np.linspace(xmin, xmax, 5)#, dtype=str)
    ax.set_xticks(custom_ticks)
    # vv uncomment if you want Networth (they y axis) to be shown logarithmically
    #ax.set_yscale('log')
    plt.show()
    print("Completed sucessfully!")
    sys.exit(0)
        
if __name__ == "__main__":
    main()
