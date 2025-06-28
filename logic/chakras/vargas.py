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
        if isinstance(value, list):
            value = value[0]
        return float(value)
    except:
        return 0.0


def get_sign_and_degree(abs_deg):
    abs_deg = to_float(abs_deg)
    sign = int(abs_deg // 30)
    deg = abs_deg % 30
    return sign, deg


def rotate_chart(mapping, asc_house):
    rotated = {i: {'planets': [], 'zodiac': ''} for i in range(1, 13)}
    for body, house in mapping.items():
        if body == "Ascendant":
            continue
        short = PLANET_SHORT.get(body, body[:2])
        shift = (house - asc_house) % 12
        new_house = shift + 1
        rotated[new_house]['planets'].append(short)

    for i in range(1, 13):
        zodiac_index = (asc_house - 1 + i - 1) % 12
        rotated[i]['zodiac'] = ZODIAC_SIGNS[zodiac_index] + f" ({zodiac_index + 1})"

    return rotated


def get_d1_chart(astro_data):
    zodiac_index = lambda z: ZODIAC_SIGNS.index(z[:3])
    asc_zodiac = astro_data['ascendant']['zodiac'][:3]
    asc_index = zodiac_index(asc_zodiac)

    chart = {i: {"zodiac": "", "planets": []} for i in range(1, 13)}

    for i in range(12):
        house_num = i + 1
        zodiac_num = (asc_index + i) % 12
        chart[house_num]["zodiac"] = ZODIAC_SIGNS[zodiac_num] + f" ({zodiac_num + 1})"

    for planet, pdata in astro_data["planets"].items():
        zodiac = pdata["zodiac"][:3]
        zodiac_idx = zodiac_index(zodiac)
        house_pos = (zodiac_idx - asc_index) % 12 + 1
        short = PLANET_SHORT.get(planet, planet[:2])
        chart[house_pos]["planets"].append(short)

    chart[1]["planets"].insert(0, "As")
    return chart


def generic_chart(planets_raw, asc_deg, transform_fn):
    chart = {}
    for planet, abs_deg in planets_raw.items():
        chart[planet] = transform_fn(to_float(abs_deg))
    chart['Ascendant'] = transform_fn(to_float(asc_deg))
    asc_sign_index = chart['Ascendant'] - 1
    return rotate_chart(chart, asc_sign_index)


def get_d3_chart(planets_raw, asc_deg):
    def drekkana_transform(abs_deg):
        sign, deg = get_sign_and_degree(abs_deg)
        if deg < 10:
            return sign
        elif deg < 20:
            return (sign + 4) % 12
        else:
            return (sign + 8) % 12

    asc_deg = to_float(asc_deg)
    asc_sign = drekkana_transform(asc_deg)

    chart = {i: {"zodiac": "", "planets": []} for i in range(1, 13)}
    for planet, abs_deg in planets_raw.items():
        if planet == "Ascendant":
            continue
        transformed = drekkana_transform(to_float(abs_deg))
        house = ((transformed - asc_sign + 12) % 12) + 1
        chart[house]["planets"].append(PLANET_SHORT.get(planet, planet[:2]))

    chart[1]["planets"].insert(0, "As")
    for i in range(1, 13):
        chart[i]["zodiac"] = ZODIAC_SIGNS[(asc_sign + i - 1) % 12] + f" ({(asc_sign + i - 1) % 12 + 1})"

    return chart


def get_d6_chart(planets_raw, asc_deg):
    def transform(abs_deg):
        sign, deg = get_sign_and_degree(abs_deg)
        is_even = (sign % 2 == 0)
        shashtiamsa = int(deg * 2)
        return ((sign + shashtiamsa) if is_even else (sign + (59 - shashtiamsa))) % 12 + 1

    return generic_chart(planets_raw, asc_deg, transform)


def get_d9_chart(d1_planets_raw, d1_asc_deg):
    def get_navamsa_start(sign):
        return {0: 0, 4: 0, 8: 0, 1: 9, 5: 9, 9: 9, 2: 6, 6: 6, 10: 6}.get(sign, 3)

    def navamsa_transform(abs_deg):
        sign, deg = get_sign_and_degree(abs_deg)
        navamsa_idx = math.ceil((deg * 9) / 30)
        return (get_navamsa_start(sign) + navamsa_idx - 1) % 12

    asc_sign_index = navamsa_transform(to_float(d1_asc_deg))
    chart = {}
    for planet, abs_deg in d1_planets_raw.items():
        if planet != 'Ascendant':
            transformed = navamsa_transform(to_float(abs_deg))
            house = ((transformed - asc_sign_index) % 12) + 1
            chart[planet] = house
    chart['Ascendant'] = 1
    return rotate_chart(chart, asc_sign_index)


def get_d30_chart(d1_planets_raw, d1_asc_deg):
    def trimsamsa_transform(abs_deg):
        sign, deg = get_sign_and_degree(abs_deg)
        if sign % 2 == 0:  # Even
            if deg <= 5:
                return 0
            elif deg <= 8:
                return 1
            elif deg <= 16:
                return 2
            elif deg <= 23:
                return 3
            elif deg <= 30:
                return 4
        else:  # Odd
            if deg <= 5:
                return 5
            elif deg <= 7:
                return 6
            elif deg <= 15:
                return 7
            elif deg <= 22:
                return 8
            elif deg <= 30:
                return 9

    asc_sign_index = trimsamsa_transform(to_float(d1_asc_deg))
    chart = {}
    for planet, abs_deg in d1_planets_raw.items():
        if planet != 'Ascendant':
            transformed = trimsamsa_transform(to_float(abs_deg))
            house = ((transformed - asc_sign_index) % 12) + 1
            chart[planet] = house
    chart['Ascendant'] = 1
    return rotate_chart(chart, asc_sign_index)


def get_d60_chart(d1_planets_raw, d1_asc_deg):
    def d60_shifted_sign(abs_deg):
        sign, deg = get_sign_and_degree(abs_deg)
        d60_index = int(deg * 2)
        return (sign + (d60_index % 12 + 1) % 12) % 12

    asc_sign_index = d60_shifted_sign(to_float(d1_asc_deg))
    chart = {}
    for planet, abs_deg in d1_planets_raw.items():
        if planet != 'Ascendant':
            transformed = d60_shifted_sign(to_float(abs_deg))
            house = ((transformed - asc_sign_index) % 12) + 1
            chart[planet] = house
    chart['Ascendant'] = 1
    return rotate_chart(chart, asc_sign_index)
