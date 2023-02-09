from datetime import datetime, timedelta
import http.client
import base64
import json
from final.models import Vehicle, API


def veh_data(username, password):
    def correct_date(date):
        if len(str(date)) == 1:
            res = f'0{str(date)}'
        else:
            res = date
        return res

    credentials = base64.b64encode(f"{username}:{password}".encode())

    headers = {"authorization": f"Basic {credentials.decode()}",
               'accept': "application/vnd.fmsstandard.com.Vehiclestatuses.v2.1+json"
               }

    now = datetime.now() - timedelta(days=7)
    end = now - timedelta(days=1)

    now_month, end_month = correct_date(now.month), correct_date(end.month)
    now_day, end_day = correct_date(now.day), correct_date(end.day)

    conn = http.client.HTTPSConnection("rfms.volvotrucks.com", timeout=10)
    conn.request("GET", f"/rfms/vehiclestatuses?starttime={end.year}-{end_month}-{end_day}T23%3A00%3A00.000Z"
                        f"&stoptime={now.year}-{now_month}-{now_day}T23%3A00%3A00.000Z&"
                        f"datetype=received&contentFilter=ACCUMULATED&"
                        f"triggerFilter=DISTANCE_TRAVELLED%2CENGINE_ON%2CIGNITION_ON&"
                        f"latestOnly=false", headers=headers)
    res = conn.getresponse()
    data = res.read()
    conn.close()
    a = data.decode("utf-8")
    dict = json.loads(a)
    vehicle_data = dict['VehicleStatus']
    return vehicle_data, now


def veh_update(V):
    def correct_date(date):
        if len(str(date)) == 1:
            res = f'0{str(date)}'
        else:
            res = date
        return res

    A = API.objects.get(vehicle_id=V.id)
    username = A.username
    password = A.password

    credentials = base64.b64encode(f"{username}:{password}".encode())

    headers = {"authorization": f"Basic {credentials.decode()}",
               'accept': "application/vnd.fmsstandard.com.Vehiclestatuses.v2.1+json"
               }

    now = datetime.now()
    end = datetime.now() - timedelta(days=1)
    if now.day > end.day or now.month > end.month:
        now_month, end_month = correct_date(now.month), correct_date(end.month)
        now_day, end_day = correct_date(now.day), correct_date(end.day)

        conn = http.client.HTTPSConnection("rfms.volvotrucks.com", timeout=1)
        conn.request("GET", f"/rfms/vehiclestatuses?starttime={end.year}-{end_month}-{end_day}T23%3A00%3A00.000Z"
                            f"&stoptime={now.year}-{now_month}-{now_day}T23%3A00%3A00.000Z&"
                            f"datetype=received&contentFilter=ACCUMULATED&"
                            f"triggerFilter=DISTANCE_TRAVELLED%2CENGINE_ON%2CIGNITION_ON&"
                            f"latestOnly=false", headers=headers)

        res = conn.getresponse()
        data = res.read()
        conn.close()
        last_milage = V.distance_traveled
        last_fuel = V.fuel_consumed
        a = data.decode("utf-8")
        dict = json.loads(a)
        no_data = True
        for veh in dict['VehicleStatus']:
            if veh['Vin'] == V.vin:
                update_milage = veh['HRTotalVehicleDistance'] - last_milage
                update_fuel = veh['EngineTotalFuelUsed'] - last_fuel
                today = datetime.now().date()
                last_update = V.last_data_upload.date()
                time_update = today - last_update
                fuel_consumption = round(update_fuel / update_milage * 100, 2)
                return update_milage, update_fuel, fuel_consumption, time_update.days
        if no_data:
            return False
    else:
        return "up to date"



