import pygame

# pygame 초기화
pygame.init()

# 오디오 시스템 초기화
pygame.mixer.init()

file_path = "d:/openai_project/src/speech/data/test4.mp3"
# MP3 파일 로드
pygame.mixer.music.load(file_path)

# 재생 시작
pygame.mixer.music.play()

# 재생이 완료될 때까지 대기
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)

# pygame 종료
pygame.quit()
