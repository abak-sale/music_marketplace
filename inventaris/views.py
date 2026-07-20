from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import GitarForm, JualGitarForm
from .models import Gitar


@login_required(login_url='/admin/login/')
def dashboard(request):
  # 3 Kartu Besar
  total_modal_aktif = (
      Gitar.objects.filter(status='Tersedia').aggregate(Sum('total_modal'))[
          'total_modal__sum'
      ]
      or 0
  )

  bulan_ini = timezone.now().month
  tahun_ini = timezone.now().year

  gitar_terjual_bulan_ini = Gitar.objects.filter(
      status='Terjual',
      tanggal_terjual__month=bulan_ini,
      tanggal_terjual__year=tahun_ini,
  )

  omset_bulan_ini = (
      gitar_terjual_bulan_ini.aggregate(Sum('harga_jual'))['harga_jual__sum']
      or 0
  )

  # Hitung laba bulan ini manual dari properti model
  laba_bulan_ini = sum(g.laba for g in gitar_terjual_bulan_ini)

  context = {
      'total_modal_aktif': total_modal_aktif,
      'omset_bulan_ini': omset_bulan_ini,
      'laba_bulan_ini': laba_bulan_ini,
  }
  return render(request, 'inventaris/dashboard.html', context)


@login_required(login_url='/admin/login/')
def daftar_gitar(request):
  query = request.GET.get('q', '')
  gitars = Gitar.objects.filter(status='Tersedia').order_by('-tanggal_masuk')

  if query:
    gitars = gitars.filter(
        Q(nama_gitar__icontains=query) | Q(brand_model__icontains=query)
    )

  return render(
      request, 'inventaris/daftar_gitar.html', {'gitars': gitars, 'query': query}
  )


@login_required(login_url='/admin/login/')
def tambah_gitar(request):
  if request.method == 'POST':
    form = GitarForm(request.POST)
    if form.is_valid():
      form.save()
      return redirect('daftar_gitar')
  else:
    form = GitarForm()
  return render(request, 'inventaris/tambah_gitar.html', {'form': form})


@login_required(login_url='/admin/login/')
def jual_gitar(request, pk):
  gitar = get_object_or_404(Gitar, pk=pk)

  if request.method == 'POST':
    form = JualGitarForm(request.POST, instance=gitar)
    if form.is_valid():
      # Ambil data dari form tanpa langsung commit ke database
      gitar_terjual = form.save(commit=False)

      # Pastikan harga jual terisi
      if gitar_terjual.harga_jual is not None:
        gitar_terjual.status = 'Terjual'
        gitar_terjual.tanggal_terjual = (
            timezone.now().date()
        )  # Tanggal terjual diisi hari ini saat konfirmasi
        gitar_terjual.save()
        return redirect('daftar_gitar')
  else:
    # Saat pertama kali klik 'Jual / Laku', pastikan harga jual dikosongkan dulu di form
    gitar.harga_jual = None
    form = JualGitarForm(instance=gitar)

  return render(request, 'inventaris/jual_gitar.html', {'form': form, 'gitar': gitar})


@login_required(login_url='/admin/login/')
def laporan_bulanan(request):
  # Ambil filter dari URL, default ke bulan/tahun sekarang
  sekarang = timezone.now()
  bulan = int(request.GET.get('bulan', sekarang.month))
  tahun = int(request.GET.get('tahun', sekarang.year))

  # Tabel 1: Gitar Masuk (Pembelian) di bulan itu
  gitar_masuk = Gitar.objects.filter(
      tanggal_masuk__month=bulan, tanggal_masuk__year=tahun
  ).order_by('-tanggal_masuk')

  # Tabel 2: Gitar Terjual di bulan itu
  gitar_terjual = Gitar.objects.filter(
      status='Terjual',
      tanggal_terjual__month=bulan,
      tanggal_terjual__year=tahun,
  ).order_by('-tanggal_terjual')

  # Total di laporan
  grand_total_modal_aktif = (
      Gitar.objects.filter(status='Tersedia').aggregate(Sum('total_modal'))[
          'total_modal__sum'
      ]
      or 0
  )
  total_omset = (
      gitar_terjual.aggregate(Sum('harga_jual'))['harga_jual__sum'] or 0
  )
  total_laba = sum(g.laba for g in gitar_terjual)

  context = {
      'gitar_masuk': gitar_masuk,
      'gitar_terjual': gitar_terjual,
      'grand_total_modal_aktif': grand_total_modal_aktif,
      'total_omset': total_omset,
      'total_laba': total_laba,
      'bulan': bulan,
      'tahun': tahun,
      'list_bulan': range(1, 13),
  }
  return render(request, 'inventaris/laporan.html', context)