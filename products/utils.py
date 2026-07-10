from PIL import Image


def optimize_image(image_field, max_dimension=1600, quality=85):
    """
    Optimasi gambar yang sudah tersimpan di disk:
    - Resize jika sisi terpanjang melebihi max_dimension (px)
    - Compress kualitas JPEG untuk memperkecil ukuran file
    - Convert mode RGBA/P (misal PNG transparan) ke RGB,
      karena format JPEG tidak mendukung transparansi

    PENTING: fungsi ini bekerja LANGSUNG di file yang sudah ada
    di disk (image_field.path) — jadi WAJIB dipanggil SETELAH
    super().save() dijalankan, supaya filenya sudah benar-benar ada.
    """
    if not image_field:
        return

    img_path = image_field.path
    img = Image.open(img_path)

    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    if img.width > max_dimension or img.height > max_dimension:
        img.thumbnail((max_dimension, max_dimension), Image.LANCZOS)

    img.save(img_path, format="JPEG", quality=quality, optimize=True)