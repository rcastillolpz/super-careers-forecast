#!.*/venv/bin/python

# Importing modules
from flask import Flask
import json
import urllib2
import re
# Importing cfg File
try:
    import cfg
except:
    print("Error: can\'t import cfg.py file")
    raise
else:
    print("cfg.py successfully imported")

# Calling Flask
app = Flask(__name__)


# Class to get and store in Memory the json from OWM
class set_owm_cfg():
    # On Init, creating the dict. to store the data and set the url of json
    def __init__(self):
        # self.owm_info is the dict. which will stores the json data
        self.owm_info = {}
        # self.owm_url is the url which calls the json
        self.owm_url = self.getting_owm_map()
        print("owm_url successfully imported: owm_url = " + self.owm_url +
              "\n")
        print("Object  set_owm_cfg successfully created.")

    # getting_owm_map(self) pareses the cfg.py to get the url of OWM json
    def getting_owm_map(self):
        try:
            if cfg.owm_url == "":
                raise
            else:
                # importing owm_url from cfg.py
                return cfg.owm_url
        except:
            print("Error: owm_url not found on cfg.py, or file is empty. "
                  " >>> NO csv can be imported.")
            raise

    # Function to get data from OWM json
    def import_openweathermap(self):
        # Retrieving the json
        req = urllib2.Request(self.owm_url)
        opener = urllib2.build_opener()
        f = opener.open(req)
        owm_json = json.loads(f.read())
        # Parsing the json
        owm_json_list = (owm_json["list"])
        for d in owm_json_list:
            try:
                # Getting Time
                d_time = d['dt_txt'] if (d['dt_txt'] is not None and d['dt_txt'] != "") else None
                if d_time is None:
                    continue
                d_time = d_time.replace("-","").replace(":","").replace(" ","")[:-2]

                # Getting Pressure
                d_pressure = d['main']['pressure'] if (d['main']['pressure'] is not None and d['main']['pressure'] != "") else None
                if d_pressure is not None:
                    d_pressure = '%.2f' % float(d_pressure)

                # Getting Humidity
                d_humidity = d['main']['humidity'] if (d['main']['humidity'] is not None and d['main']['humidity'] != "") else None
                if d_humidity is not None:
                    d_humidity = str(d_humidity) + "%"

                # Getting Temperature
                d_temp = d['main']['temp'] if (d['main']['temp'] is not None and d['main']['temp'] != "") else None
                if d_temp is not None:
                    d_temp = int(round(float(d_temp)-273.15))
                    d_temp = str(d_temp) + "C"

                # Getting desc
                d_desc = d['weather'][0]['description'] if (d['weather'][0]['description'] is not None and d['weather'][0]['description'] != "") else None

                # Adding item to self.owm_info dict
                self.owm_info[d_time] = {}
                self.owm_info[d_time]['pressure'] = d_pressure
                self.owm_info[d_time]['humidity'] = d_humidity
                self.owm_info[d_time]['temperature'] = d_temp
                self.owm_info[d_time]['description'] = d_desc

            except:
                print("Error: while parsing a json item")


# check_url_arg() Checks if the URL is OK
def check_url_arg(date, time):
    if re.search(r'^([0-9]{8})$', date):
        if re.search(r'^((0[0-9]|1[0-9]|2[0-3])([0-5][0-9]))$', time):
            return 1
    return 0


# get_time() parses the time sent in req.
# we have data of every 3 hours. (00:00, 03:00, ..., 18:00, 21:00)
# we will send the time for the previous time:
# i.e: Customer req. info for 2018-03-02 23:59 > We'll send data of (2018-03-02 21)
def get_time(time):
    hour = int(time[:2])
    rest = hour % 3
    if rest == 0:
        hour = hour
    elif rest == 1:
        hour = hour - 1
    elif rest == 2:
        hour = hour - 2
    hour = str(hour) + "00"
    hour = ("0" + hour) if (len(hour) == 3) else hour
    return (hour)

# api forecast
@app.route('/weather/london/<date>/<time>/', methods=['GET'])
def return_all(date, time):
    # req_time is the time with format suitable for the response
    req_time = date[:4] + "-" + date[4:6] + "-" + date[6:8] + " " + time[:2] + ":" + time[2:]
    # Checking url arg.
    OK = check_url_arg(date, time)

    if OK != 1:
        return "Not Valid URL  -- Time could be not valid"

    # getting time
    # time_m is the time for the correct group of hours.
    time_m = get_time(time)
    # time_s is date + time_m, which is the key for the dict. with data.
    time_s = date + time_m

    print(time_s)
    try:
        # Searching the item
        time_d_item = owm_cfg.owm_info[time_s]
    except KeyError:
        print("Error: Date given doesn't exit")
        msg = "No data for " + req_time
        data_item_d = {'status': "error", 'message': msg}
        data_json = json.dumps(data_item_d)
        return data_json
    except:
        print("Error: Something was wrong while searching date '" +
              req_time + "'")
        msg = "Something was wrong while searching '" + req_time + "'"
        data_item_d = {'id': req_time, 'Error': "ERR_UNKNOWN", 'msg': msg}
        data_json = json.dumps(data_item_d)
        return data_json

    # Wrapping the info in a dictonary
    data_owm_d = {'description': time_d_item['description'],
                  'temperature': time_d_item['temperature'],
                  'pressure': time_d_item['pressure'],
                  'humidity': time_d_item['humidity']
                  }

    # Converting dict. data_item_d  in a json and sending it out
    data_json = json.dumps(data_owm_d)
    return data_json

# api forecast
@app.route('/weather/london/<date>/<time>/<extra>', methods=['GET'])
def return_extra(date, time, extra):
    # req_time is the time with format suitable for the response
    req_time = date[:4] + "-" + date[4:6] + "-" + date[6:8] + " " + time[:2] + ":" + time[2:]
    # Checking url arg.
    OK = check_url_arg(date, time)

    if OK != 1:
        return "Not Valid URL  -- Time could be not valid"

    # getting time
    # time_m is the time for the correct group of hours.
    time_m = get_time(time)
    # time_s is date + time_m, which is the key for the dict. with data.
    time_s = date + time_m

    print(time_s)
    try:
        # Searching the item
        time_d_item = owm_cfg.owm_info[time_s]
    except KeyError:
        print("Error: Date given doesn't exit")
        msg = "No data for " + req_time
        data_item_d = {'status': "error", 'message': msg}
        data_json = json.dumps(data_item_d)
        return data_json
    except:
        print("Error: Something was wrong while searching date '" +
              req_time + "'")
        msg = "Something was wrong while searching '" + req_time + "'"
        data_item_d = {'id': req_time, 'Error': "ERR_UNKNOWN", 'msg': msg}
        data_json = json.dumps(data_item_d)
        return data_json

    try:
        # Wrapping the info in a dictonary
        data_owm_d = {extra: time_d_item[extra]}
    except KeyError:
        print("Error: Date given doesn't exit")
        msg = "No ''" + extra + "' field for " + req_time
        data_item_d = {'status': "error", 'message': msg}
        data_json = json.dumps(data_item_d)
        return data_json
    except:
        print("Error: Something was wrong while searching date '" +
              req_time + "'")
        msg = "Something was wrong while searching '" + extra + "' field for " + req_time
        data_item_d = {'id': req_time, 'Error': "ERR_UNKNOWN", 'msg': msg}
        data_json = json.dumps(data_item_d)
        return data_json

    # Converting dict. data_item_d  in a json and sending it out
    data_json = json.dumps(data_owm_d)
    return data_json


if __name__ == "__main__":
    print("****************************")
    print("Starting pricesearch.py ....")
    print("****************************")

    # Setting cfg variables
    print("****************************")
    print("Setting cfg variables ....")
    print("****************************")
    owm_cfg = set_owm_cfg()
    print(owm_cfg.owm_url)
    print("****************************")
    print("cfg variables successfuly set")
    print("****************************")

    # Getting the info from http://www.openweathermap.org/forecast5
    print("****************************")
    print("Starting to Import csv file ....")
    print("****************************")
    owm_cfg.import_openweathermap()
    print("****************************")
    print("csv successfully imported")
    print("****************************")
    print(owm_cfg.owm_info)


    # Start the API
    app.run(host='0.0.0.0', debug=True)
