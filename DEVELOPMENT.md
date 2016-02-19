# 개발을 시작할 때

## 파이선 패키지 설치
```
pip install -r requirements.txt
```

## DB 초기화
```bash
python manage.py db upgrade
```

# 개발을 완료한 후
## 새 파이선 패키지의 설치가 필요할 떄
해당 패키지 명을 requirements.txt에 추가합니다.

## DB 업데이트
```bash
python manage.py db migrate
python manage.py db upgrade
```
