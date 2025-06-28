#PENDING CODE ~~~~~~~~~ STILL NOT COMPLETE 

import swisseph as swe
import datetime

# Setup
swe.set_ephe_path('.')
swe.set_sid_mode(swe.SIDM_LAHIRI)

def jd_to_time(jd):
    y, m, d, ut = swe.revjul(jd)
    h = int(ut)
    m = int((ut % 1) * 60)
    s = int((((ut % 1) * 60) % 1) * 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

# Inputs
date_str = "27-06-2025"
time_str = "01:48"
latitude = float(42.203)
longitude = float(-71.686)
alt = 0.0
tz_offset = 4  # India would be 5.5, adjust as per need

# Convert to UTC
local_dt = datetime.datetime.strptime(f"{date_str} {time_str}", "%d-%m-%Y %H:%M")
dt_utc = local_dt - datetime.timedelta(hours=tz_offset)

# Use UTC midnight for rise/set JD
midnight_utc = datetime.datetime(dt_utc.year, dt_utc.month, dt_utc.day, 0, 0)
jd_midnight_utc = swe.julday(midnight_utc.year, midnight_utc.month, midnight_utc.day, 0.0)

print(f"🌐 Calculating for UTC date: {midnight_utc.strftime('%Y-%m-%d')}, JD: {jd_midnight_utc}")
print(f"📍 Geopos: longitude={longitude}, latitude={latitude}, elevation={alt}")

geopos = [longitude, latitude, alt]

# 🌅 Sunrise
try:
    rise_flag = swe.CALC_RISE | swe.FLG_SWIEPH
    sunrise_result = swe.rise_trans(jd_midnight_utc, swe.SUN, rise_flag, geopos)
    if sunrise_result[0] == 0:
        jd_rise = sunrise_result[1][0]
        print("🌅 Sunrise:", jd_to_time(jd_rise), "UTC")
    else:
        print("🌅 Sunrise error code:", sunrise_result[0])
except Exception as e:
    print("🌅 Sunrise Exception:", e)

# 🌇 Sunset
try:
    set_flag = swe.CALC_SET | swe.FLG_SWIEPH
    sunset_result = swe.rise_trans(jd_midnight_utc, swe.SUN, set_flag, geopos)
    if sunset_result[0] == 0:
        jd_set = sunset_result[1][0]
        print("🌇 Sunset:", jd_to_time(jd_set), "UTC")
    else:
        print("🌇 Sunset error code:", sunset_result[0])
except Exception as e:
    print("🌇 Sunset Exception:", e)
