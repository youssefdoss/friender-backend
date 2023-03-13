import pgeocode

def get_distance(zip1, zip2):
    '''Given two zipcodes, returns the distance between them in miles'''
    dist = pgeocode.GeoDistance('us')
    return dist.query_postal_code(str(zip1), str(zip2))