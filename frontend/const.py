trip_record_start="Start"
trip_record_end="Koniec"
map_true="Tak"
map_false="Nie"
header_names=["ID", "Time", "Driver", "Distance", "Duration", "EV_distance","EV_duration","Consumption", "Consuption per 100km", "Refuel", "Period"]
header_mapping = {
    "ID": "id",
    "Time": "start_time",
    "Driver": "driver",
    "Distance": "distance",
    "Duration": "duration",
    "EV_distance": "ev_distance",
    "EV_duration": "ev_duration",
    "Consumption": "fuel_consumed",
    "Consuption per 100km": "average_fuel_consumed",
    "Refuel": "refuel",
    "Period": "period",
}