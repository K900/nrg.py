import datetime
import operator
import sys

import requests

API_BASE = "http://api.nrg-tk.ru/api/rest/"

class NrgError(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return "[Error {}] {}".format(code, message)

def _api_call(method, **kwargs):
    params = {"method": method}
    params.update(kwargs)

    response = requests.get(API_BASE, params).json()["rsp"]

    if response["stat"] == "ok":
        return response
    elif response["stat"] == "fail":
        raise NrgError(response["err"]["code"], response["err"]["msg"])

def cities():
    result = {}
    for kv in _api_call("nrg.get.locations")["locations"]:
        result[kv["id"]] = kv["name"]
    return result

def track(document_id, city_id):
    response = _api_call("nrg.get_sending_state", numdoc=document_id, idcity=city_id)['info']

    return {
        "package": {
            "weight": response["weight"],
            "volume": response["volume"],
            "places": response["num_places"]
        },
        "route": {
            "from": response["cityfrom"],
            "to": response["cityto"],
            "sent_date": datetime.datetime.strptime(response["datedoc"], "%Y-%m-%d")
        },
        "state": {
            "date": datetime.datetime.strptime(response["date_state"], "%Y-%m-%d"),
            "message": response["cur_state"]
        }
    }

def _track_main():
    USAGE = """
Отслеживание отправлений ТК "Энергия".

Использование:
    nrg cities - выводит список городов с идентификаторами
    nrg track <номер накладной> <идентификатор города назначения>
""".strip()

    if len(sys.argv) < 2:
        print(USAGE)
        sys.exit(1)

    if sys.argv[1] == "cities":
        for k, v in sorted(cities().items(), key=operator.itemgetter(1)):
            print("{}: {}".format(v, k))
        sys.exit(0)

    elif sys.argv[1] == "track":
        if len(sys.argv) != 4:
            print(USAGE)
            sys.exit(1) 

        t = track(sys.argv[2], sys.argv[3])
        print("""
# Груз:
Масса: {package[weight]} кг
Объем: {package[volume]} м^3
Мест:  {package[places]}

# Отправлен:
Из:    {route[from]}
В:     {route[to]}
Дата:  {route[sent_date]}

# Последнее обновление:
Дата:  {state[date]}
{state[message]}
        """.format(**t).strip())

    else:
        print(USAGE)
        sys.exit(1)

if __name__ == '__main__':
    _track_main()