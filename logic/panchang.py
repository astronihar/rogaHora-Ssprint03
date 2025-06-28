import swisseph as swe
import datetime

# 📁 Setup
swe.set_ephe_path('./data')  # Ensure ephemeris files (e.g., sepl_18.se1) are in ./data
swe.set_sid_mode(swe.SIDM_LAHIRI)

# ♈ Constants
ZODIACS = ["Ari", "Tau", "Gem", "Can", "Leo", "Vir", "Lib", "Sco", "Sag", "Cap", "Aqu", "Pis"]
NAKSHATRAS = [
    "Ash", "Bha", "Kri", "Roh", "Mri", "Ard", "Pun", "Pus", "Ashl",
    "Mag", "PPh", "UPh", "Has", "Chi", "Swa", "Vis", "Anu", "Jye",
    "Mul", "PAs", "UAs", "Shr", "Dha", "Sha", "PBh", "UBh", "Rev"
]
TITHIS = [
    "Pratipat", "Dwitiya", "Tritiya", "Chaturthi", "Panchami", "Shashti",
    "Saptami", "Ashtami", "Navami", "Dashami", "Ekadashi", "Dwadashi",
    "Trayodashi", "Chaturdashi", "Purnima/Amavasya"
]
KARANAS = [
    "Kimstughna", "Bava", "Balava", "Kaulava", "Taitila", "Garija",
    "Vanija", "Vishti", "Shakuni", "Chatushpada", "Naga"
]
YOGAS = [
    "Vishkambha", "Priti", "Ayushman", "Saubhagya", "Shobhana", "Atiganda",
    "Sukarman", "Dhriti", "Shoola", "Ganda", "Vriddhi", "Dhruva",
    "Vyaghata", "Harshana", "Vajra", "Siddhi", "Vyatipata", "Variyana",
    "Parigha", "Shiva", "Siddha", "Sadhya", "Shubha", "Shukla",
    "Brahma", "Indra", "Vaidhriti"
]
WEEKDAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
LORDS = ["Sun", "Mon", "Mar", "Mer", "Jup", "Ven", "Sat"]

def mod360(val):
    return val % 360

def jd_to_time(jd):
    if not jd:
        return "N/A"
    y, m, d, ut = swe.revjul(jd)
    h = int(ut)
    m = int((ut % 1) * 60)
    s = int((((ut % 1) * 60) % 1) * 60)
    return f"{h:02d}:{m:02d}:{s:02d}"

def get_panchang(date_str, time_str, lat, lon, tz_offset):
    local_dt = datetime.datetime.strptime(f"{date_str} {time_str}", "%d-%m-%Y %H:%M")
    jd_local = swe.julday(local_dt.year, local_dt.month, local_dt.day,
                          local_dt.hour + local_dt.minute / 60.0)
    dt_utc = local_dt - datetime.timedelta(hours=tz_offset)
    jd_utc = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day,
                        dt_utc.hour + dt_utc.minute / 60.0)

    # ☀️ Sun & 🌙 Moon Sidereal Longitudes
    sun_long = swe.calc_ut(jd_local, swe.SUN)[0][0]
    moon_long = swe.calc_ut(jd_local, swe.MOON)[0][0]
    ayanamsa = swe.get_ayanamsa(jd_local)
    sun_sidereal = mod360(sun_long - ayanamsa)
    moon_sidereal = mod360(moon_long - ayanamsa)

    # 🌓 Tithi
    diff = mod360(moon_sidereal - sun_sidereal)
    tithi_num = int(diff // 12)
    tithi_frac = (diff % 12) / 12
    tithi_name = TITHIS[tithi_num % 15]
    tithi_pct_left = round((1 - tithi_frac) * 100, 2)
    paksha = "Shukla" if tithi_num < 15 else "Krishna"

    # 🌌 Nakshatra
    nak_num = int(moon_sidereal // (360 / 27))
    nak_frac = (moon_sidereal % (360 / 27)) / (360 / 27)
    nak_name = NAKSHATRAS[nak_num]
    nak_pct_left = round((1 - nak_frac) * 100, 2)

        # 🌅 Sunrise & Nakshatra at Sunrise
    try:
        rs_flag = swe.CALC_RISE | swe.FLG_SWIEPH
        sunrise_result = swe.rise_trans(jd_utc, swe.SUN, lon, lat, 0.0, rs_flag)
        if sunrise_result[0] == 0:
            sunrise_jd = sunrise_result[1]
            sunrise_time = jd_to_time(sunrise_jd)
            moon_at_sunrise = swe.calc_ut(sunrise_jd, swe.MOON)[0][0]
            moon_sunrise_sidereal = mod360(moon_at_sunrise - swe.get_ayanamsa(sunrise_jd))
            nak_sunrise_num = int(moon_sunrise_sidereal // (360 / 27))
            nakshatra_at_sunrise = NAKSHATRAS[nak_sunrise_num]
        else:
            print("☀️ Sunrise error code:", sunrise_result[0])
            sunrise_time = "N/A"
            nakshatra_at_sunrise = "N/A"
    except Exception as e:
        print("☀️ Sunrise exception:", e)
        sunrise_time = "N/A"
        nakshatra_at_sunrise = "N/A"

    # 🌇 Sunset
    try:
        ss_flag = swe.CALC_SET | swe.FLG_SWIEPH
        sunset_result = swe.rise_trans(jd_utc, swe.SUN, lon, lat, 0.0, ss_flag)
        if sunset_result[0] == 0:
            sunset_jd = sunset_result[1]
            sunset_time = jd_to_time(sunset_jd)
        else:
            print("🌇 Sunset error code:", sunset_result[0])
            sunset_time = "N/A"
    except Exception as e:
        print("🌇 Sunset exception:", e)
        sunset_time = "N/A"


    # 🌇 Sunset
    try:
        set_result = swe.rise_trans(jd_utc, swe.SUN, lon, lat, rsmi=swe.CALC_SET | swe.FLG_SWIEPH)
        if set_result[0] == 0:
            sunset_jd = set_result[1]
            sunset_time = jd_to_time(sunset_jd)
        else:
            sunset_time = "N/A"
    except Exception as e:
        print("🌇 Sunset error:", e)
        sunset_time = "N/A"

    # 🧘 Yoga
    total = mod360(sun_sidereal + moon_sidereal)
    yoga_num = int(total // (360 / 27))
    yoga_frac = (total % (360 / 27)) / (360 / 27)
    yoga_name = YOGAS[yoga_num]
    yoga_pct_left = round((1 - yoga_frac) * 100, 2)

    # 🔗 Karana
    karana_num = int((diff % 60) // 6)
    karana_name = KARANAS[karana_num % len(KARANAS)]
    karana_frac = (diff % 6) / 6
    karana_pct_left = round((1 - karana_frac) * 100, 2)

    # 🕉 Weekday
    weekday_num = (local_dt.weekday() + 1) % 7
    weekday_name = WEEKDAYS[weekday_num]
    weekday_lord = LORDS[weekday_num]

    # 🕰 Hora Lord
    hora_index = (weekday_num * 24 + dt_utc.hour) % 7
    hora_lord = LORDS[hora_index % 7]

    # 📿 Mahakala Hora
    mahakala_lord = LORDS[((weekday_num + 1) * 3) % 7]

    return {
        "input_date": date_str,
        "input_time": time_str,
        "latitude": lat,
        "longitude": lon,
        "timezone_offset": tz_offset,
        "tithi": f"{tithi_name} ({tithi_pct_left}% left)",
        "paksha": paksha,
        "nakshatra": f"{nak_name} ({nak_pct_left}% left)",
        "nakshatra_at_sunrise": nakshatra_at_sunrise,
        "yoga": f"{yoga_name} ({yoga_pct_left}% left)",
        "karana": f"{karana_name} ({karana_pct_left}% left)",
        "weekday": f"{weekday_name} ({weekday_lord})",
        "hora_lord": f"{hora_lord}",
        "mahakala_hora": f"{mahakala_lord}",
        "kaala_lord": f"{mahakala_lord}",
        "sunrise": sunrise_time,
        "sunset": sunset_time,
        "ayanamsa": f"{ayanamsa:.5f}",
        "sidereal_time": f"{swe.sidtime(jd_local):.2f}"
    }

# 🔍 Test
if __name__ == "__main__":
    result = get_panchang("27-06-2025", "01:48", 42.203, -71.686, 4)
    for k, v in result.items():
        print(f"{k}: {v}")
