# logic/karakas.py

def assign_karakas(planets):
    karaka_order = ['AK', 'AmK', 'BK', 'MK', 'PuK', 'GnK', 'DK']

    candidates = {
        planet: float(data['degree'])
        for planet, data in planets.items()
        if planet in ['Sun', 'Mon', 'Mer', 'Mar', 'Ven', 'Jup', 'Sat']
    }

    sorted_planets = sorted(candidates.items(), key=lambda x: x[1], reverse=True)

    karakas = {}
    for i, (planet, _) in enumerate(sorted_planets):
        if i < len(karaka_order):
            karaka = karaka_order[i]
            planets[planet]['karaka'] = karaka
            karakas[karaka] = planet

    return planets, karakas
