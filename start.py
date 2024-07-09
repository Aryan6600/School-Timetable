import json
from time import gmtime,strftime

f=open('data.json','r')
data=f.read()
timetable=json.loads(data)
c_time=strftime("%w/%I:%M/%p",gmtime()).split("/")
"""
if c_time[2]=="PM" :
    clock=c_time[1].split(":")
    if int(clock[0])==1:
        if int(clock[1])>=45:
            print("Programme not usuable after school hours ")
    if int(clock[0])>=2:
        print("Programme not usuable after school hours ")
"""

query=input("Enter Faculty Name :")
if query in timetable:
    print(timetable[query][int(c_time[0])])
else:
    print("No Data Availaible for This Faculty")

