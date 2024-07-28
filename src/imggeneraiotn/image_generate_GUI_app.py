import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QLineEdit, QTextEdit
from image_generate_dalle3_input import DallEClient

class ImageGenerationApp(QWidget):
  def __init__(self):
    super().__init__()
    self.initUI()
    # DallEClient 초기화
    self.dall_e_client = DallEClient()

  # 사용자 인터페이스 초기화
  def initUI(self):
    # 메인 레이아웃 설정 (수직 레이아웃)
    main_layout = QVBoxLayout()

    # 각 행을 위한 레이아웃 생성 및 설정
    row1_layout = QHBoxLayout()
    row2_layout = QHBoxLayout()
    row3_layout = QHBoxLayout()
    row4_layout = QHBoxLayout()
    

    # 행 1: 이미지 생성 모델
    model_label = QLabel('이미지 생성 모델', self)
    self.model_combo = QComboBox(self)
    self.model_combo.addItems(['dall-e-3', 'dall-e-2'])
    row1_layout.addWidget(model_label)
    row1_layout.addWidget(self.model_combo)

    # 행 1: 이미지 생성 크기
    size_label = QLabel('이미지 생성 크기', self)
    self.size_combo = QComboBox(self)
    self.size_combo.addItems(['1024x1024', '1792x1024', '1024x1792'])
    row1_layout.addWidget(size_label)
    row1_layout.addWidget(self.size_combo)

    # 행 1: 이미지 생성 개수
    number_label = QLabel('이미지 생성 개수', self)
    self.number_edit = QLineEdit(self)
    self.number_edit.setText('1')  # 기본값을 1로 설정
    row1_layout.addWidget(number_label)
    row1_layout.addWidget(self.number_edit)

    # 행 2: 프롬프트 입력
    prompt_label = QLabel('프롬프트 입력', self)
    self.prompt_edit = QLineEdit(self)
    self.prompt_edit.setMinimumHeight(50)  # 프롬프트 입력 폼을 길게 설정
    row2_layout.addWidget(prompt_label)
    row2_layout.addWidget(self.prompt_edit)

    # 행 3: 생성 버튼
    self.generate_button = QPushButton('이미지 생성 버튼', self)
    row3_layout.addWidget(self.generate_button)

    # 버튼을 이미지 생성 메서드에 연결
    self.generate_button.clicked.connect(self.generate_image)

    # 행 4: 이미지 URL 출력
    url_label = QLabel('이미지 생성 URL', self)
    self.url_output = QTextEdit(self)
    row4_layout.addWidget(url_label)
    row4_layout.addWidget(self.url_output)

    # 모든 행을 메인 레이아웃에 추가
    main_layout.addLayout(row1_layout)
    main_layout.addLayout(row2_layout)
    main_layout.addLayout(row3_layout)
    main_layout.addLayout(row4_layout)

    # 윈도우에 메인 레이아웃 설정
    self.setLayout(main_layout)
    # 윈도우 제목 설정
    self.setWindowTitle('이미지 생성프로그램')
    self.show()

  def generate_image(self):
    # 이미지 생성 로직을 위한 메서드    
    model = self.model_combo.currentText()
    size = self.size_combo.currentText()
    prompt = self.prompt_edit.text()  # 사용자로부터 입력받은 프롬프트

    # number_edit 값 확인
    try:
        number = int(self.number_edit.text())
    except ValueError:
        self.show_alert("이미지 생성 개수를 입력해 주세요.")
        return

    if not prompt:
        self.show_alert("프롬프트를 입력해 주세요.")
        return

    # 이미지 생성 요청
    images = self.dall_e_client.generate_image(prompt, model=model, size=size, n=number)

    # 생성된 이미지의 URL 출력
    urls = "\n".join([image.url for image in images])
    self.url_output.setPlainText(urls)


# 메인 실행 코드
if __name__ == '__main__':
  # 애플리케이션 초기화 및 윈도우 생성
  app = QApplication(sys.argv)
  window = ImageGenerationApp()
  sys.exit(app.exec_())
