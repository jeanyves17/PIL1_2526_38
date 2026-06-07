from app.services.upload_service import extension_autorisee

def test_extension_jpg():
    assert extension_autorisee("photo.jpg") is True

def test_extension_png():
    assert extension_autorisee("avatar.png") is True

def test_extension_webp():
    assert extension_autorisee("img.webp") is True

def test_extension_jpeg():
    assert extension_autorisee("img.jpeg") is True

def test_extension_pdf_refuse():
    assert extension_autorisee("document.pdf") is False

def test_extension_exe_refuse():
    assert extension_autorisee("virus.exe") is False

def test_extension_sans_point():
    assert extension_autorisee("fichiersansextension") is False

def test_extension_majuscule():
    assert extension_autorisee("PHOTO.JPG") is True
