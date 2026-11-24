#!/usr/bin/env python3
# networkFileRW.py
# Original author: Pamela Brauda
# Original date: March 3, 2022
# Modified by: Carlos G Rodriguez
# Modified date: November 24, 2026
# Course: CIS3534C
# Assignment: GPA 9 - Git and GitHub
#
# Update routers and switches;
# read equipment from a file, write updates & errors to file.
#
# Summary of changes:
# Added JSON import with exception handling.
# Created file name constants.
# Implemented reading router and switch data files.
# Implemented writing updated equipment to updated.txt.
# Implemented writing invalid IP addresses to errors.txt.

##---->>>> Use a try/except clause to import the JSON module
try:
    import json
except ImportError:
    print("Could not import the JSON module.")
    raise SystemExit(1)


##---->>>> Create file constants for the file names; file constants can be reused
##         There are 2 files to read this program: equip_r.txt and equip_s.txt
##         There are 2 files to write in this program: updated.txt and errors.txt

ROUTER_FILE = "equip_r.txt"
SWITCH_FILE = "equip_s.txt"
UPDATED_FILE = "updated.txt"
ERROR_FILE = "errors.txt"

#prompt constants
UPDATE = "\nWhich device would you like to update "
QUIT = "(enter x to quit)? "
NEW_IP = "What is the new IP address (111.111.111.111) "
SORRY = "Sorry, that is not a valid IP address\n"

#function to get valid device
def getValidDevice(routers, switches):
    validDevice = False
    while not validDevice:
        #prompt for device to update
        device = input(UPDATE + QUIT).lower()
        if device in routers.keys():
            return device
        elif device in switches.keys():
            return device
        elif device == 'x':
            return device  
        else:
            print("That device is not in the network inventory.")

#function to get valid IP address
def getValidIP(invalidIPCount, invalidIPAddresses):
    validIP = False
    while not validIP:
        ipAddress = input(NEW_IP)
        octets = ipAddress.split('.')
        #print("octets", octets)
        for byte in octets:
            byte = int(byte)
            if byte < 0 or byte > 255:
                invalidIPCount += 1
                invalidIPAddresses.append(ipAddress)
                print(SORRY)
                break
        else:
            #validIP = True
                return ipAddress, invalidIPCount
                #don't need to return invalidIPAddresses list - it's an object
        
def main():

    ##---->>>> open files here
    
    routerFile = open(ROUTER_FILE, "r")
    switchFile = open(SWITCH_FILE, "r")



    
    #dictionaries
    ##---->>>> read the routers and addresses into the router dictionary

    routers = json.load(routerFile)
    routerFile.close()


    ##---->>>> read the switches and addresses into the switches dictionary

    switches = json.load(switchFile)
    switchFile.close()


    #the updated dictionary holds the device name and new ip address
    updated = {}

    #list of bad addresses entered by the user
    invalidIPAddresses = []

    #accumulator variables
    devicesUpdatedCount = 0
    invalidIPCount = 0

    #flags and sentinels
    quitNow = False
    validIP = False

    print("Network Equipment Inventory\n")
    print("\tequipment name\tIP address")
    for router, ipa in routers.items(): 
        print("\t" + router + "\t\t" + ipa)
    for switch, ipa in switches.items():
        print("\t" + switch + "\t\t" + ipa)

    while not quitNow:

        #function call to get valid device
        device = getValidDevice(routers, switches)
        
        if device == 'x':
            quitNow = True
            break
        
        #function call to get valid IP address
        #python lets you return two or more values at one time
        ipAddress, invalidIPCount = getValidIP(invalidIPCount, invalidIPAddresses)
  
        #update device
        if 'r' in device:
            #modify the value associated with the key
            routers[device] = ipAddress 
            #print("routers", routers)
            
        else:
            switches[device] = ipAddress

        devicesUpdatedCount += 1
        #add the device and ipAddress to the dictionary
        updated[device] = ipAddress

        print(device, "was updated; the new IP address is", ipAddress)
        #loop back to the beginning

    #user finished updating devices
    print("\nSummary:")
    print()
    print("Number of devices updated:", devicesUpdatedCount)

    ##---->>>> write the updated equipment dictionary to a file
    with open(UPDATED_FILE, "w") as updatedFile:
        json.dump(updated, updatedFile)

    
    print("Updated equipment written to file 'updated.txt'")
    print()
    print("\nNumber of invalid addresses attempted:", invalidIPCount)

    ##---->>>> write the list of invalid addresses to a file
    with open(ERROR_FILE, "w") as errorFile:
        json.dump(invalidIPAddresses, errorFile)

    print("List of invalid addresses written to file 'errors.txt'")

#top-level scope check
if __name__ == "__main__":
    main()




