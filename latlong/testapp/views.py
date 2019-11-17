from django.shortcuts import render
from tablib import Dataset
from geopy.geocoders import Nominatim
import pandas as pd


def simple_upload(request):
    if request.method == 'POST':
        dataset = Dataset()
        new_loc = request.FILES['myfile']
        imported_data = dataset.load(new_loc.read())
        geolocator = Nominatim(user_agent="Gmaps")
        address = []
        latitude = []
        longitude = []
        for loc in imported_data:
            location = geolocator.geocode(loc)
            if location is not None :
                if location.latitude is not None:
                    # latlang1 =  str(location.latitude) + ',' + str(location.longitude)
                    # print('latlang1',latlang1)
                    address.append(loc[0])
                    latitude.append(location.latitude)
                    longitude.append(location.longitude)
                else:
                    return HttpResponse('Not Available')

        #print(address,latitude,longitude)


        data = pd.DataFrame({
            'Address': address,
            'Latitude': latitude,
            'Longitude': longitude,

        })

        data.to_excel('E:\\Tsak_django\\latlong\\newdata.xlsx')

    return render(request,'upload.html')

# def files_list(request):
#     return render('files_list.html',{'total_files':os.listdir(settings.MEDIA_ROOT),'path':settings.MEDIA_ROOT},context=request(request))


import os
from django.http import HttpResponse, Http404

def download(request):
    file_path = 'E:\\Tsak_django\\latlong\\newdata.xlsx'#os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404
