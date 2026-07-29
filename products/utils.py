from io import BytesIO
from PIL import Image, ImageOps


def optimize_image(image_field, max_dimension=1600, quality=85):
    """
    Optimasi gambar yang sudah tersimpan di disk:
    - PUTAR OTOMATIS sesuai tag EXIF Orientation dari kamera HP
      (mencegah foto potret jadi landscape setelah di-resize)
    - Resize jika sisi terpanjang melebihi max_dimension (px)
    - Compress kualitas JPEG untuk memperkecil ukuran file
    - Convert mode RGBA/P (misal PNG transparan) ke RGB

    PENTING (fix Windows): gambar dibaca PENUH ke memori dulu
    (pakai BytesIO), file aslinya benar-benar DITUTUP, baru
    hasil olahan ditimpa ke disk.
    """
    if not image_field:
        return

    img_path = image_field.path

    with Image.open(img_path) as img:
        img.load()

        # ✅ BARU — Baca tag EXIF Orientation dari kamera HP,
        # lalu PUTAR PIXEL ASLI sesuai orientasi yang benar.
        # Setelah ini, orientasi sudah "terkunci" secara permanen
        # di data pixel — tidak bergantung tag EXIF lagi!
        img = ImageOps.exif_transpose(img)

        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        if img.width > max_dimension or img.height > max_dimension:
            img.thumbnail((max_dimension, max_dimension), Image.LANCZOS)

        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=quality, optimize=True)

    with open(img_path, "wb") as f:
        f.write(buffer.getvalue())