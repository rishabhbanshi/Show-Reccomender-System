from jikanpy import Jikan
import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QImage, QPixmap
jikan=Jikan()
# print(jikan.search('anime',['Haikyuu!!: Karasuno Koukou VS Shiratorizawa Gakuen Koukou',['Naruto']]))
img=(jikan.anime(50)['image_url'])

app = QApplication([])

image = QImage()
image.loadFromData(requests.get(img).content)

image_label = QLabel()
image_label.setPixmap(QPixmap(image))
image_label.show()

app.exec_()