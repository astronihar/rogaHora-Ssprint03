import math

ZODIAC_SIGNS = [
    "Ari", "Tau", "Gem", "Can", "Leo", "Vir",
    "Lib", "Sco", "Sag", "Cap", "Aqu", "Pis"
]

PLANET_SHORT = {
    "Sun": "Su", "Moon": "Mo", "Mars": "Ma", "Mercury": "Me",
    "Jupiter": "Ju", "Venus": "Ve", "Saturn": "Sa",
    "Rahu": "Ra", "Ketu": "Ke", "Ascendant": "As",
    "Gulika": "Gu", "Mandi": "Mn"
}


def to_float(value):
    try:
        return float(value[0]) if isinstance(value, list) else float(value)
    except:
        return 0.0


def get_sign_and_degree(abs_deg):
    abs_deg = to_float(abs_deg)
    return int(abs_deg // 30), abs_deg % 30


def rotate_chart(mapping, asc_house):
    rotated = {i: {'planets': [], 'zodiac': ''} for i in range(1, 13)}
    for body, house in mapping.items():
        if body == "Ascendant":
            continue
        short = PLANET_SHORT.get(body, body[:2])
        shift = (house - asc_house) % 12
        rotated[shift + 1]['planets'].append(short)
    for i in range(1, 13):
        zodiac_index = (asc_house - 1 + i - 1) % 12
        rotated[i]['zodiac'] = ZODIAC_SIGNS[zodiac_index] + f" ({zodiac_index + 1})"
    return rotated


def get_d1_chart(astro_data):
    def zodiac_index(z): return ZODIAC_SIGNS.index(z[:3])
    asc_index = zodiac_index(astro_data['ascendant']['zodiac'])

    chart = {i: {"zodiac": "", "planets": []} for i in range(1, 13)}
    for i in range(12):
        chart[i + 1]["zodiac"] = ZODIAC_SIGNS[(asc_index + i) % 12] + f" ({(asc_index + i) % 12 + 1})"
    for planet, pdata in astro_data["planets"].items():
        house = ((zodiac_index(pdata["zodiac"]) - asc_index + 12) % 12) + 1
        chart[house]["planets"].append(PLANET_SHORT.get(planet, planet[:2]))
    chart[1]["planets"].insert(0, "As")
    return chart


def generic_chart(planets_raw, asc_deg, transform_fn):
    chart = {}
    for planet, abs_deg in planets_raw.items():
        chart[planet] = transform_fn(to_float(abs_deg))
    chart['Ascendant'] = transform_fn(to_float(asc_deg))
    asc_sign_index = chart['Ascendant'] - 1
    return rotate_chart(chart, asc_sign_index)


# 🔢 Individual Divisional Charts

def get_d3_chart(astro_data):
    def zodiac_index(z): return ZODIAC_SIGNS.index(z[:3])

    def drekkana_zodiac(sign, deg):
        if deg < 10:
            return sign
        elif deg < 20:
            return (sign + 4) % 12
        else:
            return (sign + 8) % 12

    asc_sign = zodiac_index(astro_data['ascendant']['zodiac'])
    asc_deg = to_float(astro_data['ascendant']['degree'])
    asc_drekkana = drekkana_zodiac(asc_sign, asc_deg)

    chart = {i: {"zodiac": "", "planets": []} for i in range(1, 13)}
    for i in range(12):
        sign_num = (asc_drekkana + i) % 12
        chart[i + 1]["zodiac"] = ZODIAC_SIGNS[sign_num] + f" ({sign_num + 1})"

    for planet, pdata in astro_data["planets"].items():
        if planet == "Ascendant":
            continue
        sign = zodiac_index(pdata["zodiac"])
        deg = to_float(pdata["degree"])
        drekkana_sign = drekkana_zodiac(sign, deg)
        house = ((drekkana_sign - asc_drekkana + 12) % 12) + 1
        chart[house]["planets"].append(PLANET_SHORT.get(planet, planet[:2]))

    chart[1]["planets"].insert(0, "As")
    return chart




def get_d6_chart(astro_data):
    def zodiac_index(z): return ZODIAC_SIGNS.index(z[:3])
    asc_deg = to_float(astro_data["ascendant"]["degree"])
    asc_sign, asc_d = get_sign_and_degree(asc_deg)

    # Ascendant transformation
    asc_shashtiamsa = int(asc_d * 2)
    asc_d6_sign = (asc_sign + asc_shashtiamsa) if asc_sign % 2 == 0 else (asc_sign + (59 - asc_shashtiamsa))
    asc_index = asc_d6_sign % 12

    chart = {i: {"zodiac": "", "planets": []} for i in range(1, 13)}
    for i in range(12):
        chart[i + 1]["zodiac"] = ZODIAC_SIGNS[(asc_index + i) % 12] + f" ({(asc_index + i) % 12 + 1})"

    for planet, pdata in astro_data["planets"].items():
        abs_deg = to_float(pdata["degree"])
        sign, deg = get_sign_and_degree(abs_deg)
        shashtiamsa = int(deg * 2)
        d6_sign = (sign + shashtiamsa) if sign % 2 == 0 else (sign + (59 - shashtiamsa))
        house = ((d6_sign % 12 - asc_index + 12) % 12) + 1
        chart[house]["planets"].append(PLANET_SHORT.get(planet, planet[:2]))

    chart[1]["planets"].insert(0, "As")
    return chart



def get_d9_chart(astro_data):
    def zodiac_index(z): return ZODIAC_SIGNS.index(z[:3])

    RASHI_TYPE = {
        0: "Movable", 1: "Fixed", 2: "Dual",
        3: "Movable", 4: "Fixed", 5: "Dual",
        6: "Movable", 7: "Fixed", 8: "Dual",
        9: "Movable", 10: "Fixed", 11: "Dual"
    }

    def get_navamsa_sign(sign, deg):
        navamsa_part = int(deg // 3.3333)
        rtype = RASHI_TYPE[sign]
        if rtype == "Movable":
            start = sign
        elif rtype == "Fixed":
            start = (sign + 8) % 12  # 9th from sign
        elif rtype == "Dual":
            start = (sign + 4) % 12  # 5th from sign
        else:
            start = sign
        return (start + navamsa_part) % 12

    asc_deg = to_float(astro_data["ascendant"]["degree"])
    asc_sign, asc_degree = get_sign_and_degree(asc_deg)
    d9_asc_sign = get_navamsa_sign(asc_sign, asc_degree)

    # ✅ Build Chart like D1
    chart = {i: {"zodiac": "", "planets": []} for i in range(1, 13)}
    for i in range(12):
        chart[i + 1]["zodiac"] = ZODIAC_SIGNS[(d9_asc_sign + i) % 12] + f" ({(d9_asc_sign + i) % 12 + 1})"

    for planet, pdata in astro_data["planets"].items():
        abs_deg = to_float(pdata["degree"])
        sign, deg = get_sign_and_degree(abs_deg)
        d9_sign = get_navamsa_sign(sign, deg)
        house = ((d9_sign - d9_asc_sign + 12) % 12) + 1
        chart[house]["planets"].append(PLANET_SHORT.get(planet, planet[:2]))

    chart[1]["planets"].insert(0, "As")
    return chart








def get_d10_chart(planets_raw, asc_deg):
    def transform(abs_deg):
        sign, deg = get_sign_and_degree(abs_deg)
        return (sign * 10 + int(deg // 3)) % 12
    return generic_chart(planets_raw, asc_deg, transform)


def get_d12_chart(planets_raw, asc_deg):
    def transform(abs_deg):
        sign, deg = get_sign_and_degree(abs_deg)
        return (sign + int(deg * 12 / 30)) % 12
    return generic_chart(planets_raw, asc_deg, transform)


def get_d16_chart(planets_raw, asc_deg):
    def transform(abs_deg):
        sign, deg = get_sign_and_degree(abs_deg)
        return (sign * 16 + int(deg * 16 / 30)) % 12
    return generic_chart(planets_raw, asc_deg, transform)


def get_d20_chart(planets_raw, asc_deg):
    def transform(abs_deg):
        sign, deg = get_sign_and_degree(abs_deg)
        return (sign * 20 + int(deg * 20 / 30)) % 12
    return generic_chart(planets_raw, asc_deg, transform)


# def get_d24_chart(planets_raw, asc_deg):
#     def transform(abs_deg):
#         sign, deg = get_sign_and_degree(abs_deg)
#         return (sign * 24 + int(deg * 24 / 30)) % 12
#     return generic_chart(planets_raw, asc_deg, transform)


def get_d30_chart(planets_raw, asc_deg):
    def transform(abs_deg):
        sign, deg = get_sign_and_degree(abs_deg)
        if sign % 2 == 0:
            return [0, 1, 2, 3, 4][[deg <= 5, deg <= 8, deg <= 16, deg <= 23, deg <= 30].index(True)]
        else:
            return [5, 6, 7, 8, 9][[deg <= 5, deg <= 7, deg <= 15, deg <= 22, deg <= 30].index(True)]
    return generic_chart(planets_raw, asc_deg, transform)


def get_d40_chart(planets_raw, asc_deg):
    def transform(abs_deg):
        sign, deg = get_sign_and_degree(abs_deg)
        return (sign * 40 + int(deg * 40 / 30)) % 12
    return generic_chart(planets_raw, asc_deg, transform)


def get_d45_chart(planets_raw, asc_deg):
    def transform(abs_deg):
        sign, deg = get_sign_and_degree(abs_deg)
        return (sign * 45 + int(deg * 45 / 30)) % 12
    return generic_chart(planets_raw, asc_deg, transform)


def get_d60_chart(planets_raw, asc_deg):
    def transform(abs_deg):
        sign, deg = get_sign_and_degree(abs_deg)
        d60_index = int(deg * 2)
        return (sign + ((d60_index % 12 + 1) % 12)) % 12
    return generic_chart(planets_raw, asc_deg, transform)
