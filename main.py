#
# Overview: Project 1, Programming with sql and python using databases
# Name: Travis Lee
# Class: CS341

import sqlite3
import matplotlib.pyplot as figure
import sys

##################################################################  
#
# percent
#
# Divides the given numbers then multiplies them by 100
# and restricts it to 2 decimal places
#
def percent(partial, total):
    realP = (partial/total) * 100;
    return round(realP,2)

##################################################################  
#
# print_stats
#
# Given a connection to the CTA database, executes various
# SQL queries to retrieve and output basic stats.
#
def print_stats(dbConn):
    dbCursor = dbConn.cursor()
    totalRiders = 0;
    
    print("General stats:")
    
    #Number of stations
    dbCursor.execute("Select count(*) From Stations;")
    row = dbCursor.fetchone();
    print("  # of stations:", f"{row[0]:,}")
    
    #Number of stops
    dbCursor.execute("Select count(Stop_ID) From Stops;")
    row = dbCursor.fetchone();
    print("  # of stops:", f"{row[0]:,}")
    
    #Number of ride entries
    dbCursor.execute("Select count(Num_Riders) From Ridership")
    row = dbCursor.fetchone();
    print("  # of ride entries:", f"{row[0]:,}")
    
    #Date Range
    dbCursor.execute("Select date(Ride_Date) From Ridership")
    row = dbCursor.fetchall();
    print("  date range:", f"{row[0][0]:} - ", end = "")
    dbCursor.execute("Select date(Ride_Date) From Ridership order by Ride_Date desc")
    row = dbCursor.fetchall();
    print(f"{row[0][0]}")
    
    #Total Ridership
    dbCursor.execute("Select sum(Num_Riders) From Ridership")
    row = dbCursor.fetchone();
    totalRiders = row[0];
    print("  Total ridership:", f"{row[0]:,}")
    
    #Weekday Ridership
    dbCursor.execute("Select sum(Num_Riders) From Ridership where Type_of_Day = 'W'")
    row = dbCursor.fetchone();
    print("  Weekday ridership:", f"{row[0]:,}", end = "")
    print(f" ({percent(row[0], totalRiders)}%)")
    
    #Saturday Ridership
    dbCursor.execute("Select sum(Num_Riders) From Ridership where Type_of_Day = 'A'")
    row = dbCursor.fetchone();
    print("  Saturday ridership:", f"{row[0]:,}", end = "")
    print(f" ({percent(row[0], totalRiders)}%)")
    
    #Sunday Ridership
    dbCursor.execute("Select sum(Num_Riders) From Ridership where Type_of_Day = 'U'")
    row = dbCursor.fetchone();
    print("  Sunday/holiday ridership:", f"{row[0]:,}", end = "")
    print(f" ({percent(row[0], totalRiders)}%)")

##################################################################  
#
# command
#
# Takes user input and directs the program to the approriate place
# 
#
def command(dbConn):
    inputCommand = input("Please enter a command (1-9, x to exit): ")
    
    if inputCommand == "1":
        print()
        pName = input("Enter partial station name (wildcards _ and %): ")
        commandOne(pName,dbConn)
    elif inputCommand == "2":
        print("** ridership all stations **")
        commandTwo(dbConn)
    elif inputCommand == "3":
        print("** top-10 stations **")
        commandThree(dbConn)
    elif inputCommand == "4":
        print("** least-10 stations **")
        commandFour(dbConn)
    elif inputCommand == "5":
        print()
        inputColor = input("Enter a line color (e.g. Red or Yellow): ")
        commandFive(inputColor,dbConn)
    elif inputCommand == "6":
        print("** ridership by month **")
        commandSix(dbConn)
    elif inputCommand == "7":
        print("** ridership by year **")
        commandSeven(dbConn)
    elif inputCommand == "8":
        commandEight(dbConn)
    elif inputCommand == "9":
        commandNine(dbConn)
    elif inputCommand == "x":
        sys.exit()
    else:
        print("**Error, unknown command, try again...")

##################################################################  
#
# Command "1"
#
# Takes partial input from user and retrieve stations like the input
# 
#            
def commandOne(pName, dbConn):
    dbCursor = dbConn.cursor()
    
    sql = "Select Station_ID, Station_Name From Stations where Station_Name like ? order by Station_Name asc"
    dbCursor.execute(sql, [pName])
    Stations = dbCursor.fetchall()
    
    if not Stations:
        print("**No stations found...")
    else:
        for row in Stations:
            print(f"{row[0]}",":", f"{row[1]}")

##################################################################  
#
# Command "2"
#
# Prints the ridership at each station in ascending order by
# station name
#  
def commandTwo(dbConn):
    dbCursor = dbConn.cursor()
    
    dbCursor.execute("Select sum(Num_Riders) From Ridership")
    row = dbCursor.fetchone();
    totalRiders = row[0];
    
    dbCursor.execute("""Select Station_Name, sum(Num_Riders)
                        from Stations
                        join Ridership on Stations.Station_ID = Ridership.Station_ID
                        group by Station_Name
                        order by Station_Name asc""")
    stations = dbCursor.fetchall()
    
    for row in stations:
        percentage = (row[1]/totalRiders)*100
        print(f"{row[0]}", ":", f"{row[1]:,}", f"({percentage:.2f}%)")

##################################################################  
#
# Command "3"
#
# Prints the top 10 busiest stations in terms of rider ship
# in descending order by ridership
#  
def commandThree(dbConn):
    dbCursor = dbConn.cursor()
    
    dbCursor.execute("Select sum(Num_Riders) From Ridership")
    row = dbCursor.fetchone();
    totalRiders = row[0]
    
    dbCursor.execute("""Select Station_Name, sum(Num_Riders)
                        from Stations
                        join Ridership ON Stations.Station_ID = Ridership.Station_ID
                        group by Station_Name
                        order by sum(Num_Riders) desc
                        limit 10""")
    stations = dbCursor.fetchall()
    
    for row in stations:
        percentage = (row[1]/totalRiders)*100
        print(f"{row[0]}", ":", f"{row[1]:,}", f"({percentage:.2f}%)")

##################################################################  
#
# Command "4"
#
# Prints the top 10 least busiest stations in terms of ridership
# in ascending order by ridership
#  
def commandFour(dbConn):
    dbCursor = dbConn.cursor()
    
    dbCursor.execute("Select sum(Num_Riders) From Ridership")
    row = dbCursor.fetchone();
    totalRiders = row[0]
    
    dbCursor.execute("""Select Station_Name, sum(Num_Riders)
                        from Stations
                        join Ridership ON Stations.Station_ID = Ridership.Station_ID
                        group by Station_Name
                        order by sum(Num_Riders) asc
                        limit 10""")
    stations = dbCursor.fetchall()
    
    for row in stations:
        percentage = (row[1]/totalRiders)*100
        print(f"{row[0]}", ":", f"{row[1]:,}", f"({percentage:.2f}%)")

##################################################################  
#
# Command "5"
#
# Input a line color from the user and output all stop names that are
# part of that line in ascending order
# 
def commandFive(inputColor,dbConn):
    dbCursor = dbConn.cursor()
    
    dbCursor.execute("""Select Stop_Name, Direction, ADA, Color
                        from Stops
                        join StopDetails ON Stops.Stop_ID = StopDetails.Stop_ID
                        join Lines ON StopDetails.Line_ID = Lines.Line_ID
                        where Color like ?
                        order by Stop_Name asc""", [inputColor])
    stations = dbCursor.fetchall()
    if not stations:
        print("**No such line...")
    else:
        for row in stations:
            if row[2] == 1:
                print(f"{row[0]}", ": direction =", f"{row[1]}", "(accessible? yes)")
            else:
                print(f"{row[0]}", ": direction =", f"{row[1]}", "(accessible? no)")
        
##################################################################  
#
# Command "6"
#
# Print total ridership by month in ascending order by month
# with option to plot
# 
def commandSix(dbConn):
    dbCursor = dbConn.cursor()
    
    dbCursor.execute("""Select strftime('%m',Ride_Date), sum(Num_Riders)
                        from Ridership
                        group by strftime('%m',Ride_Date)
                        order by strftime('%m',Ride_Date)""")
    stations = dbCursor.fetchall()
    for row in stations:
        print(f"{row[0]}", ":", f"{row[1]:,}")
    
    #plotting starts here v v v 
    print()
    plotQ = input("Plot? (y/n) ")
    print()
    
    if plotQ.upper() == "Y":#makes it case insensitive
        x = []
        y = []
    
        for row in stations:
            x.append(row[0])
            y.append(row[1])
        
        figure.xlabel("month")
        figure.ylabel("number of riders(x * 10^8)")
        figure.title("monthly ridership")
    
        figure.plot(x,y)
        figure.show()
    
##################################################################  
#
# Command "7"
#
# Print total ridership by year in ascending order by year
# With the option to plot
#  
def commandSeven(dbConn):
    dbCursor = dbConn.cursor()
    
    dbCursor.execute("""Select strftime('%Y',Ride_Date), sum(Num_Riders)
                        from Ridership
                        group by strftime('%Y',Ride_Date)
                        order by strftime('Yy',Ride_Date) asc""")
                        
    stations = dbCursor.fetchall()
    
    for row in stations:
        print(f"{row[0]}", ":", f"{row[1]:,}")
    
        
    #plotting starts here v v v
    print()
    plotQ = input("Plot? (y/n) ")
    print()
    
    if plotQ.upper() == "Y":#makes it case insensitive
        x = []
        y = []
        
        for row in stations:
            x.append(row[0][2:4])
            y.append(row[1])
            
        figure.xlabel("year")
        figure.ylabel("number of riders (x * 10^8)")
        figure.title("yearly ridership")
        
        figure.plot(x,y)
        figure.show()
        

##################################################################  
#
# Command "8"
#
# Inputs a year and names of two stations then outputs the daily
# ridership at each station for that year. With the option to plot
#  
def commandEight(dbConn):
    dbCursor = dbConn.cursor()
    print()
    year = input("Year to compare against? ")
    print()
    choiceOne = input("Enter station 1 (wildcards _ and %): ")
    
    sql ="""select Station_ID, Station_Name
                      from Stations
                      where Station_Name like ?"""
    dbCursor.execute(sql,[choiceOne])
    stationOne = dbCursor.fetchall()
    
    if not stationOne:
        print("**No station found...")
        return
    elif len(stationOne) > 1:
        print("**Multiple stations found...")
        return
    
    print()    
    choiceTwo = input("Enter station 2 (wildcards _ and %): ")
    dbCursor.execute(sql,[choiceTwo])
    stationTwo = dbCursor.fetchall()
    
    if not stationTwo:
        print("**No station found...")
        return
    elif len(stationTwo) > 1:
        print("**Multiple stations found...")
        return
    
    topLastFive = """select date(Ride_Date), Num_Riders, Station_ID 
                 from Ridership
                 where Station_ID = ? AND strftime('%Y', Ride_Date) = ?
                 order by strftime('%D',Ride_Date) asc"""
    args = (stationOne[0][0], year) #created this and the line below to fill out the ?'s in topLastFive
    argsTwo = (stationTwo[0][0], year)
    dbCursor.execute(topLastFive,args)
    sOnefive = dbCursor.fetchall()#sOneTfive = stationOne five
    
    dbCursor.execute(topLastFive, argsTwo)
    sTwofive = dbCursor.fetchall()#sTwofive = stationTwo five
    
    print("Station 1:", stationOne[0][0],stationOne[0][1])
    for row in sOnefive[:5]:
        print(f"{row[0]}", f"{row[1]}")
    for row in sOnefive[-5:]:
        print(f"{row[0]}", f"{row[1]}")
        
    print("Station 2:", stationTwo[0][0],stationTwo[0][1])
    for row in sTwofive[:5]:
        print(f"{row[0]}", f"{row[1]}")
    for row in sTwofive[-5:]:
        print(f"{row[0]}", f"{row[1]}")
    
    
    #Plotting starts here v v v
    print()
    plotQ = input("Plot? (y/n) ")
    print()
    
    if plotQ.upper() == "Y":#makes it case insensitive
        x = []
        y = []
        xTwo = []
        yTwo = []
        day = 1
        
        for row in sOnefive:
            x.append(day)
            y.append(row[1])
            day = day + 1       
    
        day = 1
        for row in sTwofive:
            xTwo.append(day)
            yTwo.append(row[1])
            day = day + 1
    
        figure.xlabel("day")
        figure.ylabel("number of riders")
        figure.title("riders each day of " + year)
        figure.plot(x,y)
        figure.plot(xTwo,yTwo)
        figure.legend([stationOne[0][1], stationTwo[0][1]])
        figure.show()
    
##################################################################  
#
# Command "9"
#
# Input a line color from user and output all station names that are part of 
# that line in ascending order, along with their longitude and latitude
# and the option to plot
def commandNine(dbConn):
    dbCursor = dbConn.cursor()
    print()
    inputColor = input("Enter a line color (e.g. Red or Yellow): ")
    
    dbCursor.execute("""select distinct Station_Name, Latitude, Longitude
                        from Stops
                        join StopDetails ON Stops.Stop_ID = StopDetails.Stop_ID
                        join Stations ON Stops.Station_ID = Stations.Station_ID
                        join Lines ON StopDetails.Line_ID = Lines.Line_ID
                        where Color like ?
                        order by Station_Name asc""", [inputColor])
    stations = dbCursor.fetchall()
    
    if not stations:
        print("**No such line...")
        return
    else:
        for row in stations:
            print(f"{row[0]}" , ":" , f"({row[1]}, {row[2]})")
    
    #Plotting starts here v v v
    print()
    plotQ = input("Plot? (y/n) ")
    print()
    
    if plotQ.upper() == "Y":
        x = []
        y = []
        
        for row in stations:
            x.append(row[2])
            y.append(row[1])
        
        image = figure.imread("chicago.png")
        xydims = [-87.9277, -87.5569, 41.7012, 42.0868]
        figure.imshow(image, extent = xydims)
        
        figure.title(inputColor + " line")
        
        if (inputColor.lower() == "purple-express"):
            inputColor = "Purple"
            
        figure.plot(x, y, "o", c = inputColor)
        
        for row in stations:
            figure.annotate(row[0], (row[2],row[1]))
        
        figure.xlim([-87.9277, -87.5569])
        figure.ylim([41.7012, 42.0868])
        figure.show()


##################################################################  
#
# main
#
print('** Welcome to CTA L analysis app **')
print()

dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')

print_stats(dbConn)
while True:
    command(dbConn)

#
# done
#
