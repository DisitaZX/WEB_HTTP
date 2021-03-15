def map_refract(toponym):
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    low1, low2 = toponym["boundedBy"]["Envelope"]["lowerCorner"].split(" ")
    up1, up2 = toponym["boundedBy"]["Envelope"]["upperCorner"].split(" ")
    delta = [str((float(up1) - float(low1)) / 2),
             str((float(up2) - float(low2)) / 2)]
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([delta[0], delta[1]]),
        "pt": ",".join([toponym_longitude, toponym_lattitude]),
        "l": "map"
    }
    return map_params
