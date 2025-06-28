import swisseph as swe
import datetime
from helper.gul_man import get_gulika_mandi  # 🔁 New import

# ✅ Short Zodiac Names
ZODIAC_SIGNS = [
    'Ari', 'Tau', 'Gem', 'Can', 'Leo', 'Vir',
    'Lib', 'Sco', 'Sag', 'Cap', 'Aqu', 'Pis'
]

# ✅ Short Nakshatra Names (27)
NAKSHATRAS = [
    "Ash", "Bha", "Kri", "Roh", "Mri", "Ard", "Pun",
    "Pus", "Ashl", "Mag", "PPh", "UPh", "Has",
    "Chi", "Swa", "Vis", "Anu", "Jye", "Mul", "PAs",
    "UAs", "Shr", "Dha", "Sha", "PBh", "UBh", "Rev"
]

# ✅ Degree → Zodiac, Nakshatra, Pada
def degree_to_details(deg):
    zodiac_index = int(deg // 30)
    nak_index = int((deg % 360) // (360 / 27))
    pada = int(((deg % (360 / 27)) / (13.333333 / 4))) + 1

    return {
        'degree': round(deg % 30, 5),
        'zodiac': ZODIAC_SIGNS[zodiac_index],
        'nakshatra': NAKSHATRAS[nak_index],
        'pada': pada
    }

# ✅ Used by external GUI to get chart data
def get_astro_data(date_str, time_str, lat, lon):
    try:
        full_str = f"{date_str} {time_str}".strip()
        has_am_pm = "AM" in full_str.upper() or "PM" in full_str.upper()

        if has_am_pm:
            try:
                dt = datetime.datetime.strptime(full_str, "%d-%m-%Y %I:%M %p")
            except ValueError:
                clean_time = time_str.replace("AM", "").replace("PM", "").strip()
                dt = datetime.datetime.strptime(f"{date_str} {clean_time}", "%d-%m-%Y %H:%M")
        else:
            dt = datetime.datetime.strptime(full_str, "%d-%m-%Y %H:%M")

        # 🔄 Convert from IST to UTC manually (no double localization)
        dt_utc = dt - datetime.timedelta(hours=5, minutes=30)

        return calculate_chart(dt_utc, lat, lon)

    except Exception as e:
        print(f"[ERROR] get_astro_data failed: {e}")
        return None

# ✅ Live chart for testing/demos
def get_live_chart():
    latitude = 28.6139
    longitude = 77.2090
    now = datetime.datetime.now()
    dt_utc = now - datetime.timedelta(hours=5, minutes=30)
    return calculate_chart(dt_utc, latitude, longitude)

# ✅ Internal Chart Generator
def calculate_chart(dt_utc, lat, lon):
    try:
        swe.set_ephe_path('./data')
        swe.set_sid_mode(swe.SIDM_LAHIRI)

        jd = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day,
                        dt_utc.hour + dt_utc.minute / 60 + dt_utc.second / 3600)

        # 🧭 Ascendant
        cusps, ascmc = swe.houses_ex(jd, lat, lon, b'P', swe.FLG_SIDEREAL)
        asc_deg = ascmc[swe.ASC]
        asc_data = degree_to_details(asc_deg)

        # ✅ Short Planet Labels
        planets = {
            swe.SUN: 'Sun',
            swe.MOON: 'Mon',
            swe.MERCURY: 'Mer',
            swe.VENUS: 'Ven',
            swe.MARS: 'Mar',
            swe.JUPITER: 'Jup',
            swe.SATURN: 'Sat',
            swe.MEAN_NODE: 'Rah'
        }

        planet_data = {}
        planets_raw = {}
        rahu_deg = 0

        for code, shortname in planets.items():
            pos, _ = swe.calc(jd, code, swe.FLG_SIDEREAL)
            planet_data[shortname] = degree_to_details(pos[0])
            planets_raw[shortname] = pos[0]
            if shortname == 'Rah':
                rahu_deg = pos[0]

        # 🌓 Ketu = 180° opposite of Rahu
        ketu_deg = (rahu_deg + 180) % 360
        planet_data['Ket'] = degree_to_details(ketu_deg)
        planets_raw['Ket'] = ketu_deg

        planets_raw['Ascendant'] = asc_deg

        # # ✅ Add Ascendant
        # planet_data['Asc'] = asc_data

        # ✅ Gulika & Mandi
        weekday_num = (dt_utc.weekday() + 1) % 7  # Sunday = 0
        gulman = get_gulika_mandi(jd, lat, lon, weekday_num)

        for key in gulman:
            planet_data[key] = gulman[key]
            planets_raw[key] = gulman[key]['degree'] + ZODIAC_SIGNS.index(gulman[key]['zodiac']) * 30

        return {
            'timestamp': dt_utc.strftime("%Y-%m-%d %I:%M %p UTC"),
            'ascendant': asc_data,
            'planets': planet_data,
            'planets_raw': planets_raw
        }

    except Exception as e:
        print(f"[ERROR] Chart calculation failed: {e}")
        return None
