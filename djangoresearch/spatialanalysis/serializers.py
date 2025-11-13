from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
from django.core.exceptions import ValidationError
from . models import Posyandubogor


class PosyandubogorGeoSerializer(GeoFeatureModelSerializer):
    """
    GeoFeatureModelSerializer will output GeoJSON Feature objects:
    {
        "type": "Feature",
        "geometry": { ... },
        "properties": { ... }
    }
    """
    class Meta:
        model = Posyandubogor
        geo_field = "geometry"
        # properties become the feature properties
        properties = [
            "id",
            "nama_penerima",
            "data_sasaran_jumlah_kk_field",
            "jumlah_kader_sesuai_sk",
            "alamat_lengkap",
            "kepemilikan_gedung",
            "keterangan_tambahan",
            "pkm",
            "alamat_ordered",
            "longitude",
            "latitude",
        ]
        fields = '__all__'
        read_only_fields = ["id"]

    # re-use the latitude/longitude validators from the other serializer if desired
    def validate_longitude(self, value):
        if value is None:
            return value
        if value < -180 or value > 180:
            raise serializers.ValidationError("Longitude must be between -180 and 180.")
        return value

    def validate_latitude(self, value):
        if value is None:
            return value
        if value < -90 or value > 90:
            raise serializers.ValidationError("Latitude must be between -90 and 90.")
        return value

