import json
from time import gmtime,strftime
from flask import Flask,render_template,request

f=open('data.json','r')
data=f.read()
timetable=json.loads(data)
c_time=strftime("%w/%H:%M/%p",gmtime()).split("/")

period_map=["7:40-8:20","8:20-9:00","9:00-9:40","9:40-10:20","10:20-11:00","11:00-11:40","11:40-12:20","12:20-13:00","13:00-17:40"]
"""
if c_time[2]=="PM" :
    clock=c_time[1].split(":")
    if int(clock[0])==1:
        if int(clock[1])>=45:
            print("Programme not usuable after school hours ")
    if int(clock[0])>=2:
        print("Programme not usuable after school hours ")
"""
faculties=timetable.keys()

def getCurrentPeriod():
    period=0
    for timing in period_map:
        limits=timing.split("-")
        p_start=limits[0].split(":")
        print(f"Checking for period {period}")
        print(f"start time {p_start}")
        p_end=limits[1].split(":")
        print(f"end time {p_end}")
        print(c_time[1].split(":")[0])
        print(c_time[1].split(":")[1])
        if int(c_time[1].split(":")[0])>=int(p_start[0]) and int(c_time[1].split(":")[0])<=int(p_end[0]):
            print("True")
            if int(c_time[1].split(":")[0])==int(p_end[0]):
                print("True")
                if int(c_time[1].split(":")[1])>=int(p_start[1]) and int(c_time[1].split(":")[1])<=int(p_end[1]):
                    print("True")
                    return period
            return period
        period+=1
    return 999


app=Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search',methods=["GET"])
def search():
    if request.method=="GET":
        results=[]
        query=request.args['query'].lower()
        print(f"Searching for {query}")
        for name in faculties:
            print(f"trying to match with {name}")
            i=0
            while len(query)+i<=len(name):
                print(name[i:len(query)+i].lower())
                if query==name[i:len(query)+i].lower():
                    results.append(name)
                    break
                i+=1
        data=dict()
        for j in results:
            data[j]=timetable[j][int(c_time[0])][getCurrentPeriod()]
        return data




app.run(debug=True)
