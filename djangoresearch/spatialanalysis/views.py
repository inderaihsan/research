import django
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework import status
import uuid
import geopandas as gpd
from sqlalchemy import create_engine, text
from django.conf import settings
import os
from . models import Posyandubogor
from .serializers import PosyandubogorGeoSerializer


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoresearch.settings")
django.setup()
db_conf = settings.DATABASES['postgis']
db_url = f"postgresql://{db_conf['USER']}:{db_conf['PASSWORD']}@{db_conf['HOST']}:{db_conf['PORT']}/{db_conf['NAME']}"

print(db_conf)
# Create your views here.
@api_view(['GET']) 
def init(request) : 
    return Response({'message' : 'Running.'}, status = status.HTTP_200_OK) 

@api_view(['POST']) 
def upload_data_to_postgis(request) : 
    request_id = uuid.uuid4()
    data = request.FILES.get("geojsondata") 
    table_name = request.data.get("table-name")
    if data : 
        try :  
            name = data.name
            size = data.size 
            gdf = gpd.read_file(data)
            gdf = gdf.to_crs("EPSG:4326")
            engine = create_engine(db_url) 
            gdf.to_postgis(table_name, engine, if_exists = "replace") 
            idx_name = f"{table_name}_geom_gist" 
            geom_name = "geom" if "geometry" not in gdf.columns else "geometry"
            with engine.begin() as conn:
                conn.execute(text(f"CREATE INDEX IF NOT EXISTS {idx_name} ON {table_name} USING GIST ({geom_name});"))
            return Response({'message' : 'Done'})
        except Exception as e: 
            
            return Response({'message' : f'unexpected error : {e}'})

    else : 
        return Response({'name' : None}) 
    
@api_view(['GET']) 
def get_posyandu_data(request) : 
    name = request.data.get('name', "Posyandu")
    address = request.data.get('address', "Bukit")
    # name = request.data.get('name', None) 
    # sort_by = request.data.get("sort_parameter", None) 
    return Response({'data' : PosyandubogorGeoSerializer(Posyandubogor.objects.using("postgis").filter(nama_penerima__icontains = name, alamat_lengkap__icontains=address), many = True).data})
    
 
    
