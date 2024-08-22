import json #for parsing json file and sending json response on server
from time import strftime,localtime # to get current time for knowing the correct period
from flask import Flask,render_template,request #required to create a webserver for this app


sr_period_map=["7:40-8:40","8:40-9:10","9:10-9:45","9:45-10:20","10:20-10:55","10:55-11:20","11:20-11:55","11:55-12:25","12:25-12:55","12:55-13:30"] # map for timings of different periods
jr_period_map=["7:40-8:40","8:40-9:10","9:10-9:45","9:45-10:20","10:20-10:45","10:45-11:20","11:20-11:55","11:55-12:25","12:25-12:55","12:55-13:30"] # map for timings of different periods


def getCurrentPeriod(is_sr=True): # function to predict the current period
    c_time=strftime("%w/%H:%M/%p",localtime()).split("/") # getting current week day number, time and AM/PM
    # print(c_time)
    period_map = sr_period_map
    if not is_sr:
        period_map = jr_period_map
    period=0 # setting initial value of period to be 0
    for timing in period_map: # now looping through every time range in map of timings to find the current range of time
        limits=timing.split("-")  # seprating starting time and ending time of period
        p_start=limits[0].split(":") # putting starting time and minutes of this period into a new var
        #print(f"Checking for period {period}")
        #print(f"start time {p_start}")
        p_end=limits[1].split(":")
        #print(f"end time {p_end}")
        #print(c_time[1].split(":")[0])
        #print(c_time[1].split(":")[1])
        if int(c_time[1].split(":")[0])>=int(p_start[0]) and int(c_time[1].split(":")[0])<=int(p_end[0]): # checking if current hour is in thw range of this period
            # print("- True")
            if int(c_time[1].split(":")[0])==int(p_end[0]): # checking if current hour is equal to ending hour
                                                            # if it is equal then we check for minutes to be sure
                # print("True")
                if int(c_time[1].split(":")[1])<=int(p_end[1]):
                    # print("True")
                    return period # if this period matches with current timings then return the period value
                period+=1
                continue
            if int(c_time[1].split(":")[1])>=int(p_start[1]):
                return period
        period+=1
    return 999 # if no period matches then return this


app=Flask(__name__) # used for creating web routes
@app.route('/')
def index(): 
    return render_template('index.html')

@app.route('/search',methods=["POST"])
def search(): # json api route for getting the data of facuilties
    if request.method=="POST":
        f=open('data.json','r') #opening the json file which contains the data for timetable
        data=f.read() # saving contents of above file as text
        f.close()
        timetable=json.loads(data) # parsing the above text as a dictionary
        faculties=timetable.keys() # getting name of every faculty 
        c_time=strftime("%w/%H:%M/%p",localtime()).split("/") # getting current week day number, time and AM/PM
        results=[]
        try:
            query=request.form['query'].lower() # getting the name of the given faculty
           # print("Valid Query")
            if query == None:
                return 'Invalid Parameters'
            #print(f"Searching for {query}")
            for name in faculties: # searching the given query in name of every faculty and if a match occours adding it to a new list
                #print(f"trying to match with {name}")
                i=0
                while len(query)+i<=len(name):
             #       print(name[i:len(query)+i].lower())
                    if query==name[i:len(query)+i].lower():
                        results.append(name)
            #            print("found",name)
                        break
                    i+=1
            data=dict()
            period_no=getCurrentPeriod()
            # print(period_no)
            if period_no==999 or int(c_time[0])==0:
                return '{"No Data for after school hours":["[Not Defined]","None"]}'
            
           # print("most code completed")
            for j in results:
                current_period=timetable[j][int(c_time[0])-1][period_no]
                subject=timetable[j][6]
                data[j]=[current_period,subject] # generating a dictionary for the matched faculties with their current locatino in classes
            
            res = json.dumps(data) # returning response to the cliend in json format
            #print(res)
            return res
        except:
            return 'Error'
            
@app.route('/view',methods=["POST"])
def getData(): # endpoint to get the data of complete timetable for a teacher
   c_time=strftime("%w/%H:%M/%p",localtime()).split("/") # getting current week day number, time and AM/PM
   if request.method == "POST":
        name=request.form['n']
        if name==None or name=="":
            return 'Invalid Parameters'
        f=open('data.json','r') #opening the json file which contains the data for timetable
        data=f.read() # saving contents of above file as text
        f.close()
        timetable=json.loads(data)
        faculties=timetable.keys()
        if name in faculties:
            f_data=timetable[name]
            return json.dumps({"data":f_data,"day":int(c_time[0])-1,"period":getCurrentPeriod()})
        return 'No data'


@app.route('/new',methods=["GET","POST"])
def add():
    if request.method=="GET":
        return render_template("add.html")
    if request.method == "POST":
        f=open('data.json','r') #opening the json file which contains the data for timetable
        data=f.read() # saving contents of above file as text
        f.close()
        timetable=json.loads(data) # parsing the above text as a dictionary
        week_map =["m","t","w","th","f","s"]
        week = []
        is_jr=False # whether teacher is junior or senior
        try:
            if request.form['is_jr']=="on" :# if is junior checkboxe is checked then junior teacher 
                is_jr=True
        except:
            pass
        for i in week_map:
            day=[]
            for j in range(0,9):
               day.append(request.form[f"{i}-{j}"])
            if is_jr:
                day=day[0:4]+["Recess"]+day[4:]
            else:
                day=day[0:5]+["Recess"]+day[5:]
            week.append(day)
        week.append(request.form['t-subj'])
        week.append(is_jr)
        timetable[request.form["t-name"]]=week

        with open('data.json','w') as f: # writing the data received 
            f.write(json.dumps(timetable))
        return 'Done'

app.run(debug=True,port=6600) # starting app
