# 📁 helper/gul_man.py
import swisseph as swe
import datetime

# Setup
swe.set_ephe_path('./data')
swe.set_sid_mode(swe.SIDM_LAHIRI)

ZODIACS = ["Ari", "Tau", "Gem", "Can", "Leo", "Vir", "Lib", "Sco", "Sag", "Cap", "Aqu", "Pis"]
NAKSHATRAS = [
    "Ash", "Bha", "Kri", "Roh", "Mri", "Ard", "Pun", "Pus", "Ashl",
    "Mag", "PPh", "UPh", "Has", "Chi", "Swa", "Vis", "Anu", "Jye",
    "Mul", "PAs", "UAs", "Shr", "Dha", "Sha", "PBh", "UBh", "Rev"
]

def degree_to_details(deg):
    nak_deg = 360 / 27
    pada_deg = nak_deg / 4
    return {
        "degree": round(deg % 30, 5),
        "zodiac": ZODIACS[int(deg // 30) % 12],
        "nakshatra": NAKSHATRAS[int(deg // nak_deg) % 27],
        "pada": int((deg % nak_deg) // pada_deg) + 1
    }

def get_gulika_mandi(jd_utc, lat, lon, weekday_num):
    try:
        weekday_num = int(weekday_num)

        # 🌅 Sunrise and Sunset
        rs = swe.rise_trans(jd_utc, swe.SUN, lon, lat, rsmi=swe.CALC_RISE | swe.FLG_SWIEPH)
        ss = swe.rise_trans(jd_utc, swe.SUN, lon, lat, rsmi=swe.CALC_SET | swe.FLG_SWIEPH)

        if rs[0] != 0 or ss[0] != 0:
            print("❌ Failed to compute sunrise/sunset.")
            return {}

        sunrise_jd = rs[1]
        sunset_jd = ss[1]
        duration = sunset_jd - sunrise_jd

        # Gulika and Mandi indexes (1-based)
        gulika_periods = [7, 6, 5, 4, 3, 2, 1]  # Sunday=0
        mandi_periods  = [6, 5, 4, 3, 2, 1, 7]

        gulika_index = gulika_periods[weekday_num]
        mandi_index  = mandi_periods[weekday_num]

        def special_lagna_deg(index):
            jd_lagna = sunrise_jd + ((index - 1) * (duration / 8.0))
            cusps, ascmc = swe.houses_ex(jd_lagna, lat, lon, b'A', swe.FLG_SIDEREAL)
            return ascmc[swe.ASC]

        gul_deg = special_lagna_deg(gulika_index)
        man_deg = special_lagna_deg(mandi_index)

        return {
            "Gul": degree_to_details(gul_deg),
            "Man": degree_to_details(man_deg)
        }

    except Exception as e:
        print("⚠️ Gulika/Mandi Error:", e)
        return {}

# ✅ Standalone debug
if __name__ == "__main__":
    date_str = "28-06-2025"
    time_str = "07:00"
    lat = 11.7
    lon = 78.6

    try:
        dt = datetime.datetime.strptime(f"{date_str} {time_str}", "%d-%m-%Y %H:%M")
        dt_utc = dt - datetime.timedelta(hours=5, minutes=30)  # Convert to UTC
        jd_utc = swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, dt_utc.hour + dt_utc.minute / 60)
        weekday_num = dt.weekday()  # Sunday = 6

        result = get_gulika_mandi(jd_utc, lat, lon, weekday_num)
        print("🔍 Gulika & Mandi Debug Output:")
        print(result)

    except Exception as e:
        print("❌ Debugging exception:", e)
