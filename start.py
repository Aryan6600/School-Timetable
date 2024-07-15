import json #for parsing json file and sending json response on server
from time import gmtime,strftime,localtime # to get current time for knowing the correct period
from flask import Flask,render_template,request #required to create a webserver for this app

f=open('data.json','r') #opening the json file which contains the data for timetable
data=f.read() # saving contents of above file as text
timetable=json.loads(data) # parsing the above text as a dictionary
c_time=strftime("%w/%H:%M/%p",localtime()).split("/") # getting current week day number, time and AM/PM
print(c_time)
period_map=["7:40-8:20","8:20-9:00","9:00-9:40","9:40-10:20","10:20-11:00","11:00-11:40","11:40-12:20","12:20-13:00","13:00-13:40"] # map for timings of different periods

faculties=timetable.keys() # getting name of every faculty 

def getCurrentPeriod(): # function to predict the current period
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
            #print("True")
            if int(c_time[1].split(":")[0])==int(p_end[0]): # checking if current hour is equal to ending hour
                                                            # if it is equal then we check for minutes to be sure
                #print("True")
                if int(c_time[1].split(":")[1])>=int(p_start[1]) and int(c_time[1].split(":")[1])<=int(p_end[1]):
                    #print("True")
                    return period # if this period matches with current timings then return the period value
                period+=1
                continue
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
            #print(period_no)
            if period_no==999 or int(c_time[0])==0:
                return '{"No Data":["[Not Defined]","None"]}'
            
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
            
@app.route('/view')
def getData():
    name=request.args['n']
    if name==None or name=="":
        return 'Invalid Parameters'
    f_data=timetable[name]
    print(f_data)
    return render_template('view.html',data=f_data,name=name)




app.run(debug=True) # starting app
