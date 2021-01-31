from django.contrib.gis.geoip2 import GeoIP2
import requests
import json

def current_location():
 

    send_url = "http://api.ipstack.com/check?access_key=c8d87ebf9a98cd3f78f0a7cf664e8054"
    geo_req = requests.get(send_url)
    geo_json = json.loads(geo_req.text)
    latitude = geo_json['latitude']
    longitude = geo_json['longitude']
    city = geo_json['city']
    return city


def get_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip=request.META.get('REMOTE_ADDR')
    return ip

def get_go(ip):
    g = GeoIP2()
    country = g.country(ip)
    city  =g.city(ip)
    lat,lon = g.lat_lon(ip)
    return country,city,lat,lon

def get_center_cord(latA,lonA,latB=None,lonB=None):
    cord = (latA,lonA)
    if latB:
        cord = ((latA+latB)/2,(lonA+lonB)/2)

    return cord

def get_zoom(distance):
    if distance <=100:
        return 6
    elif distance >100 and distance<=5000:
        return 3
    else:
        return 1