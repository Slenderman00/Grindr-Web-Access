import pyqrcode

def drawqr(data):
    text = pyqrcode.create(data)
    print(text.text().replace("0", "██").replace("1", "  "))

        