from django.contrib.gis.db import models

# Create your models here.

class Posyandubogor(models.Model):
  
    nama_penerima = models.TextField(db_column='nama penerima', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    data_sasaran_jumlah_kk_field = models.FloatField(db_column='data sasaran (jumlah kk)', blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    jumlah_kader_sesuai_sk = models.FloatField(db_column='jumlah kader sesuai sk', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    alamat_lengkap = models.TextField(db_column='alamat lengkap', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    kepemilikan_gedung = models.TextField(db_column='kepemilikan gedung', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    keterangan_tambahan = models.TextField(db_column='keterangan tambahan', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    kepemilikan_class = models.TextField(blank=True, null=True)
    pkm = models.TextField(blank=True, null=True)
    alamat_ordered = models.TextField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    wadmpr = models.TextField() 
    wadmkk = models.TextField() 
    wadmkc = models.TextField() 
    wadmkd = models.TextField() 
    geometry = models.PointField(srid = 4326)
    

    class Meta:
        managed = False
        db_table = 'posyandu_bogor_mapid'