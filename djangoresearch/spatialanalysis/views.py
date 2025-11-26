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
from .models import Posyandubogor
from .serializers import PosyandubogorGeoSerializer
import numpy as np

# from osgeo import gdal
# import pyproj


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoresearch.settings")
django.setup()
db_conf = settings.DATABASES["postgis"]
db_url = f"postgresql://{db_conf['USER']}:{db_conf['PASSWORD']}@{db_conf['HOST']}:{db_conf['PORT']}/{db_conf['NAME']}"

print(db_conf)


# Create your views here.
@api_view(["GET"])
def init(request):
    return Response({"message": "Running."}, status=status.HTTP_200_OK)


@api_view(["POST"])
def upload_data_to_postgis(request):
    request_id = uuid.uuid4()
    data = request.FILES.get("geojsondata")
    table_name = request.data.get("table-name")
    if data:
        try:
            name = data.name
            size = data.size
            gdf = gpd.read_file(data)
            gdf = gdf.to_crs("EPSG:4326")
            engine = create_engine(db_url)
            gdf.to_postgis(table_name, engine, if_exists="replace")
            idx_name = f"{table_name}_geom_gist"
            geom_name = "geom" if "geometry" not in gdf.columns else "geometry"
            with engine.begin() as conn:
                conn.execute(
                    text(
                        f"CREATE INDEX IF NOT EXISTS {idx_name} ON {table_name} USING GIST ({geom_name});"
                    )
                )
            return Response({"message": "Done"})
        except Exception as e:

            return Response({"message": f"unexpected error : {e}"})

    else:
        return Response({"name": None})


@api_view(["GET"])
def get_wadmkc(request):
    wadmkc_list = (
        Posyandubogor.objects.using("postgis")
        .values_list("wadmkc", flat=True)
        .distinct()
    )
    return Response({"data": list(wadmkc_list)})


@api_view(["GET"])
def get_wadmkd(request):
    wadmkc = request.GET.get("wadmkc", "Bogor Tengah")
    wadmkc_list = (
        Posyandubogor.objects.using("postgis")
        .filter(wadmkc__icontains=wadmkc)
        .values_list("wadmkd", flat=True)
        .distinct()
    )
    return Response({"data": list(wadmkc_list)})


@api_view(["GET"])
def get_posyandu_data(request):
    name = request.data.get("name", None)
    address = request.data.get("address", None)
    wadmkd = request.data.get("wadmkd", None)
    wadmkc = request.data.get("wadmkc", None)
    labels = []
    value = []
    query = Posyandubogor.objects.using("postgis")
    kepemilikan_values = (
        query.all().values_list("kepemilikan_class", flat=True).distinct()
    )
    for items in kepemilikan_values:
        if items:
            count_items = query.filter(kepemilikan_class=items).count()
            labels.append(items)
            value.append(count_items)

    chart_matrix = {"label": labels, "values": value}
    return Response(
        {
            "data": PosyandubogorGeoSerializer(query, many=True).data,
            "chart_data": chart_matrix,
        }
    )


@api_view(["GET"])
def get_posyandu_query(request):
    name = request.data.get("name", None)
    address = request.data.get("address", None)
    wadmkd = request.GET.get("wadmkd", None)
    wadmkc = request.GET.get("wadmkc", None)
    labels = []
    value = []
    query = Posyandubogor.objects.using("postgis").filter(
        wadmkc__icontains=wadmkc, wadmkd__icontains=wadmkd
    )
    kepemilikan_values = query.values_list("kepemilikan_class", flat=True).distinct()

    for items in kepemilikan_values:
        if items:
            count_items = query.filter(kepemilikan_class=items).count()
            labels.append(items)
            value.append(count_items)

    chart_matrix = {"label": labels, "values": value}

    return Response(
        {
            "data": PosyandubogorGeoSerializer(query, many=True).data,
            "chart_data": chart_matrix,
        }
    )
