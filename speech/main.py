import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QLineEdit
from PyQt5.QtCore import QDateTime, QThread, pyqtSignal
from memo_generator import AudioNotesGenerator

# 작업을 위한 스레드 클래스
class GenerateNotesThread(QThread):
    finished = pyqtSignal(bool)  # 작업 완료 시그널

    def __init__(self, generator, file_path, output_filename):
        super().__init__()
        self.generator = generator
        self.file_path = file_path
        self.output_filename = output_filename

    def run(self):
        # 오디오 노트 생성 작업 수행
        notes = self.generator.generate_audio_notes(self.file_path, self.output_filename)
        self.finished.emit(notes is not None)  # 작업 완료 시그널 방출

# AudioNotesApp 클래스는 QWidget을 상속받아 정의됨
class AudioNotesApp(QWidget):
    def __init__(self):
        super().__init__()
        # AudioNotesGenerator 객체를 생성
        self.generator = AudioNotesGenerator()
        # UI를 초기화
        self.initUI()

    # UI 초기화 메서드
    def initUI(self):
        # 창의 제목 설정
        self.setWindowTitle('Audio Notes Generator')
        # 창의 위치 및 크기 설정
        self.setGeometry(100, 100, 500, 200)

        # 레이아웃 생성
        layout = QVBoxLayout()

        # 안내 라벨 생성 및 레이아웃에 추가
        self.label = QLabel("오디오 파일의 경로를 입력하거나 찾아보기 버튼을 사용하여 파일을 선택합니다.", self)
        layout.addWidget(self.label)

        # 파일 경로 입력을 위한 QLineEdit 생성 및 레이아웃에 추가
        self.line_edit = QLineEdit(self)
        layout.addWidget(self.line_edit)

        # 파일 탐색을 위한 버튼 생성 및 클릭 이벤트 연결
        self.browse_button = QPushButton('Browse', self)
        self.browse_button.clicked.connect(self.browse_file)
        layout.addWidget(self.browse_button)

        # 노트 생성을 위한 버튼 생성 및 클릭 이벤트 연결
        self.generate_button = QPushButton('노트 생성', self)
        self.generate_button.clicked.connect(self.generate_notes)
        layout.addWidget(self.generate_button)

        # 레이아웃을 현재 위젯에 설정
        self.setLayout(layout)

    # 파일 탐색 메서드
    def browse_file(self):
        # 파일 탐색 창 옵션 설정
        options = QFileDialog.Options()
        # 오디오 파일만 필터링하여 파일 탐색 창 열기
        file_path, _ = QFileDialog.getOpenFileName(self, "오디오 파일 열기", "", "Audio Files (*.mp3 *.wav)", options=options)
        # 파일 경로가 선택되면 QLineEdit에 파일 경로 설정
        if file_path:
            self.line_edit.setText(file_path)

    # 노트 생성 메서드
    def generate_notes(self):
        # QLineEdit에서 파일 경로 가져오기
        file_path = self.line_edit.text()
        # 파일 경로가 존재하는 경우
        if file_path:
            # 상태 라벨을 "생성중..."으로 업데이트
            self.label.setText("생성중...")
            # 라벨 업데이트 즉시 반영
            QApplication.processEvents()
            # 스레드 객체 생성
            self.thread = GenerateNotesThread(
                self.generator, 
                file_path, 
                self.get_output_filename()
                )
            # 스레드의 작업 완료 시그널과 슬롯 연결
            self.thread.finished.connect(self.on_generate_finished)
            # 스레드 시작
            self.thread.start()

    # 작업 완료 시 호출되는 슬롯
    def on_generate_finished(self, success):
        # 작업 결과에 따라 라벨 텍스트 업데이트
        if success:
            self.label.setText("생성완료! 새로운 음성 데이터를 추가해서 노트를 생성하세요.")
        else:
            self.label.setText("노트를 생성하지 못했습니다. 오디오 파일을 확인하고 다시 시도하세요..")

    # 출력 파일 이름 생성 메서드
    def get_output_filename(self):
        # 현재 날짜 및 시간 가져오기
        current_datetime = QDateTime.currentDateTime().toString('yyyyMMdd_hhmmss')
        # 출력 파일 이름 형식 지정
        return f'{current_datetime}_notes.docx'

# 메인 루프
if __name__ == '__main__':
    # QApplication 객체 생성
    app = QApplication(sys.argv)
    # AudioNotesApp 객체 생성 및 창 표시
    ex = AudioNotesApp()
    ex.show()
    # 이벤트 루프 실행
    sys.exit(app.exec_())
