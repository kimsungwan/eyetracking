from PIL import Image

# 원본 로고 로드
img = Image.open('static/images/uvolution_logo.png')

# 현재 크기 확인
print(f"원본 크기: {img.size}")

# 3배로 확대 (고해상도)
new_width = img.width * 3
new_height = img.height * 3

# 고품질 리샘플링으로 확대
img_resized = img.resize((new_width, new_height), Image.LANCZOS)

# 저장
img_resized.save('static/images/uvolution_logo_large.png')
print(f"새로운 크기: {img_resized.size}")
print("저장 완료: static/images/uvolution_logo_large.png")
