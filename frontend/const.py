trip_record_start="Start"
trip_record_end="Koniec"
trip_record_start_address="Adres startowy"
trip_record_end_address="Adres końcowy"
map_true="Tak"
map_false="Nie"
header_names=["ID", "Time", "Driver", "Distance", "Duration", "EV_distance","EV_duration","Consumption", "Consuption per 100km", "Refuel", "Period", "Start Address", "End Address"]
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
    "Start Address": "start_address",
    "End Address": "end_address",
}
CreateUserDialogTitle="Utwórz nowego użytkownika"
user_fields=["Imię", "Nazwisko", "Email"]
user_delete_dialog = lambda val: "Czy na pewno chcesz usunąć użytkownika "+val+"? Spowoduje to trwałe usunięcie go z historii."
create_user_button = "Dodaj użytkownika"
