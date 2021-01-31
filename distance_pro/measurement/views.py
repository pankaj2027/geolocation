from django.shortcuts import render,get_object_or_404
from .models import Measurement
from .forms import MeasurementModelForm
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from .utlis import get_go,get_center_cord,get_zoom,get_ip_address
import folium

# Create your views here.

def calculate_distance_view(request):
    # initial the variable 
    distance = None
    destination = None
    # obj = get_object_or_404(Measurement,id=1)
    form = MeasurementModelForm(request.POST or None)
    geolocator = Nominatim(user_agent='measurement')
   
    # initial map folium
    m = folium.Map(width=500, height=300, zoom_start=8)
    #  location folium marker
    # folium.Marker([l_lat,l_lon], tooltip='click here to more', popup=city['city'],icon=folium.Icon(color='purple')).add_to(m)
    if form.is_valid():
        instance = form.save(commit=False)
        location_ = form.cleaned_data.get('location')
        destination_ = form.cleaned_data.get('destination')
        destination = geolocator.geocode(destination_)

        location = geolocator.geocode(location_)
        # loaction co-ordinate
        l_lat=location.latitude
        l_lon=location.longitude
        pointA = (l_lat,l_lon)
        # desinate co-ordinate
        d_lat = destination.latitude
        d_lon = destination.longitude
        pointB =(d_lat,d_lon)
        # distance calculate
        distance = round(geodesic(pointA,pointB).km,2) 
        # modification map folium
        m = folium.Map(width=500, height=300, location=get_center_cord(l_lat,l_lon,d_lat,d_lon),zoom_start=get_zoom(distance))
        #  location folium marker
        folium.Marker([l_lat,l_lon], tooltip='click here to more', popup=location,icon=folium.Icon(color='purple')).add_to(m)
        #  destination folium marker 
        folium.Marker([d_lat,d_lon], tooltip='click here to more', popup=destination,icon=folium.Icon(color='red',icon='cloud')).add_to(m)
        line = folium.PolyLine(locations=[pointA,pointB],wight=10,color='green')
        m.add_child(line)
        instance.location = location
        instance.distance = distance
        instance.save()
    m = m._repr_html_()

    context = {

        'distance':distance,
        'destination': destination,
        'location':location,
        'form':form,
        'map': m

    }
     
    return render(request,'measurement/main.html',context)