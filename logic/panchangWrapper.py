from logic.panchang import get_panchang

def prepare_panchang_payload(date_str, time_str, ampm, lat, lon, tz_offset=5.5):
    """
    Convert 12hr time to 24hr, then call get_panchang
    """
    # Convert to 24-hour time
    h, m = map(int, time_str.split(":"))
    if ampm == "PM" and h != 12:
        h += 12
    elif ampm == "AM" and h == 12:
        h = 0
    time_24 = f"{h:02d}:{m:02d}"

    # Call Panchang engine
    return get_panchang(date_str, time_24, lat, lon, tz_offset)
