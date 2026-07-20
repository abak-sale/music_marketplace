from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('gitar/', views.daftar_gitar, name='daftar_gitar'),
    path('gitar/tambah/', views.tambah_gitar, name='tambah_gitar'),
    path('gitar/jual/<int:pk>/', views.jual_gitar, name='jual_gitar'),
    path('laporan/', views.laporan_bulanan, name='laporan'),
]