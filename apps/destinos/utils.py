from math import radians, cos, sin, asin, sqrt


def haversine(lat1, lon1, lat2, lon2):
    """Calcula distância em km entre dois pontos geográficos."""
    R = 6371
    lat1, lon1, lat2, lon2 = map(radians, [float(lat1), float(lon1), float(lat2), float(lon2)])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 2 * R * asin(sqrt(a))


def destinos_proximos(queryset, lat, lon, raio_km=50):
    """Filtra queryset de Destino pelo raio usando Haversine."""
    ids_proximos = []
    for destino in queryset:
        dist = haversine(lat, lon, destino.latitude, destino.longitude)
        if dist <= raio_km:
            ids_proximos.append((destino.id, dist))
    ids_proximos.sort(key=lambda x: x[1])
    return ids_proximos
