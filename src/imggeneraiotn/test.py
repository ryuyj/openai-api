import sys
import openai
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtGui import QPixmap
from io import BytesIO

# OpenAI API 키 설정
openai.api_key = 'YOUR_OPENAI_API_KEY'

class ImageGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('OpenAI Image Generator')
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()
        
        self.prompt_input = QLineEdit(self)
        self.prompt_input.setPlaceholderText('Enter your prompt here...')
        self.layout.addWidget(self.prompt_input)
        
        self.generate_button = QPushButton('Generate Image', self)
        self.generate_button.clicked.connect(self.generate_image)
        self.layout.addWidget(self.generate_button)
        
        self.image_label = QLabel(self)
        self.layout.addWidget(self.image_label)
        
        self.setLayout(self.layout)
        
    def generate_image(self):
        prompt = self.prompt_input.text()
        if prompt:
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="1024x1024"
            )
            image_url = response['data'][0]['url']
            self.download_and_display_image(image_url)
        
    def download_and_display_image(self, url):
        response = requests.get(url)
        image = QPixmap()
        image.loadFromData(BytesIO(response.content).read())
        self.image_label.setPixmap(image)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageGeneratorApp()
    ex.show()
    sys.exit(app.exec_())
