# Name: Jeremy Golden
# Course: CYBR-260-45
# Date: 5 / 1 / 2020
# Purpose: scan any number of ports on any ip address.
# Scan is timed, makes note of all open ports and saves their response data.
# Data about open ports printed to console, and verbose logs stored as Scanner_Log.txt
import socket
import datetime
import time
import sys


# function: validatePortList
# purpose: Make sure all ports in list are in acceptable range [1-65535]
# inputs: list of ports, in this case from getPorts
# returns: list of ports in acceptable range [1-65535]
def validatePortList(portList):
    for port in portList:
        print("Validating port format...")
        try:
            if int(port) not in range(1, 65535):        # valid port range [1-65535]
                print("There was a problem validating the port list, port not in acceptable range...")
                return None
            else:
                return (portList)
        except:
            print("There was a problem validating the port list, port cannot be converted to int...")
            print("Please enter valid port argument, presets are case sensitive, press enter for default...")
            return None


# function: getPorts
# purpose: Takes user input for ports and checks for preset values
# inputs: list of ports, or value for one of presets
# returns: Validated list of ports (validation happens inside this function via validatePortList)
def getPorts():
    print("   *****  Port Settings  *****\n"
          "For custom list input any number of ports separated by spaces\n"
          "   *****  Presets  *****  \n"
          "DEFAULT - [20,21,22,23,25,53,79,88,389,515]\n"
          "Enter 'LOW' for - ports [1-100]\n"
          "Enter '1k' - ports [1-1000] not recommended\n"
          "Enter 'ALL' - [1-65535] really not recommended\n")
    inputPorts = input("What ports would you like to scan?\n")

    presets = {
        "": [20, 21, 22, 23, 25, 53, 79, 88, 389, 515],
        "DEFAULT": [20, 21, 22, 23, 25, 53, 79, 88, 389, 515],
        "LOW": range(1, 100),
        "1k": range(1, 1000),
        "ALL": range(1, 65535)
    }
    for key in presets:     # check for presets trigger
        if inputPorts == key:
            return presets[key]
    customPorts = validatePortList(inputPorts.split())      # check formatting on non presets
    customPortsList = []
    if customPorts is None:     # None value here means we will loop back until acceptable value input
        pass
    else:
        for port in customPorts:
            customPortsList.append(int(port))
        return customPortsList


# function: validateIp
# purpose: Takes input for Ip, and validates that is an acceptable ip address
# inputs: no inputs, but takes user input inside function
# returns: blank input will return "127.0.0.1", returns acceptably formatted ip
def validateIp():
    print("   *****  Ip settings  *****")
    print("For custom address enter a standard format ip address")
    print("DEFAULT - local host (127.0.0.1)")
    print("Press enter to continue using default settings\n")
    ip = input("Enter ip to scan:\n")
    print("Validating ip format...")
    if ip == "":            # default set to localhost
        ip = "127.0.0.1"
    try:
        parts = ip.split('.')       # verifies 4 numbers separated by '.' in range [1-256].
        if len(parts) == 4 and all(0 <= int(part) < 256 for part in parts) is True:
            return ip
        else:
            print("I'm sorry, that was not a valid ip address...")
    except (ValueError, AttributeError, TypeError):
        print("I'm sorry, that was not a valid ip address...")


# function: getIp
# purpose: Makes sure the validateIp function does not return None value
# inputs: No inputs, validateIp inside the function takes user input
# returns: Returns acceptably formatted ip handled by validateIp
def getIp():
    ip = None
    while ip is None:
        ip = validateIp()
    return ip


# function: portScan
# purpose: scans all ports on ip address, times scan, records all results with timestamps
# inputs: validated ip address and validated list of ports form above functions
# returns: prints data about scan and open ports to console, returns list of lines of log data describing scan
def portScan(ip, ports):
    s = socket.socket()
    input("   *****  press Enter to begin scanning  *****")
    print("Scanning ports...")

    now = time.time()   # Set variables for scan
    log = []
    openPorts = []

    for port in ports:
        print("Scanning at", ip, port)
        try:
            s.connect((ip, port))
            response = s.recv(2048)

            print("   *******")           # Any open port dealt with here
            print("OPEN PORT:", str(port))
            print("DATA: ", str(response))

            timestamp = datetime.datetime.now().time()
            logString = "PORT " + str(port) + " OPEN *** " + " DATA: " + str(response) + " time " + str(timestamp)
            log.append(logString)
            openPorts.append(logString)
            s.close

        except:
            timestamp = datetime.datetime.now().time()      # Closed ports dealt with here
            logString = "PORT " + str(port) + " error connecting time " + str(timestamp)
            log.append(logString)

    elapsedTime = str("{:.2f}".format(time.time() - now))        # Timer formatted to 2 decimal places in seconds
    timeLog = "Scan of " + str(ip) + " took a total of " + elapsedTime + " seconds"
    print(timeLog)

    for port in openPorts:
        print(port)
    log.append(timeLog)

    return log


# function: writeLog
# purpose: Creates/opens Scanner_Log.txt and writes all log information line by line
# inputs: list of lines of log data from portScan
# returns: returns nothing, but creates/writes log data to txt in directory
def writeLog(resultList):
    log = open("Scanner_Log.txt", "w+")
    for line in resultList:
        log.write(str(line)+"\n")
    log.close()


try:
    ports = None    # set port list
    while ports is None:    # Ensures user can enter invalid ports multiple times without causing errors
        ports = getPorts()

    ip = getIp()    # set ip
    print("Target ip set to: " + ip + "\n")
    writeLog(portScan(ip, ports))   # preform scan of ports on ip and log results
except KeyboardInterrupt:
    print("You pressed Ctrl+C")     # This try/except allows user to quit at anytime using ctrl+c
    sys.exit()
