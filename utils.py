import datetime
import time


def from_ddmmyyyyhhmm_to_unix(date: str) -> int:
    date = datetime.datetime.strptime(date, '%d/%m/%Y %H:%M')
    return int(time.mktime(date.timetuple())) * 1000

def truncate(number: float, decimals: int =2) -> float:
    if decimals < 0:
        raise ValueError("El número de decimales debe ser mayor o igual a cero")
    factor = 10.0 ** decimals
    return int(number * factor) / factor