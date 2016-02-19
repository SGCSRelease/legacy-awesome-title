# 개발을 시작할 때

## 1. 소스코드를 받습니다
```bash
git clone https://github.com/minhoryang/AwesomeTitle.git
cd AwesomeTitle
```
아래의 명령을 한번도 쳐 본 기억이 없다면, 새 컴퓨터에서 작업을 하신다면, 아래의 명령을 쳐주세요.
```bash
git config --global user.name "자신의 이름을 영어로"
git config --global user.email "자신의 Github이메일"
git config --global core.editor vim
```

## 2. Pyenv를 이용해 자신이 사용할 Python 환경을 맞춥니다!
```bash
pyenv local python3.5.1-awesometitle
```
[(참고) pyenv 설치법](https://minhoryang.github.io/ko/posts/aws-ec2-instance-creation-for-python-dev/)

## 3. 파이선 패키지 설치
```bash
pip install -r requirements.txt
```

## 4. MySQL DB 준비
- localhost
- ID: awesometitle
- PW: awesometitle
- DB: awesometitle

[(참고) mysql 설치 및 phpmyadmin을 통한 mysql 관리 **(TODO)**]()

# 개발하는 법
## 1. 개발하고 싶은 일감을 이슈에 적습니다.
## 2. 자신이 가지고 있는 코드를 최신 코드로 업데이트 합니다.
```bash
git checkout master
git pull origin master
```

(기존에 작업하고 있던 코드가 있을 경우, 업데이트에서 에러가 날 수 있습니다. 깨끗한 상태로 만드시고 진행해주세요.)

```bash
git checkout -- . 
```
## 3. (혹시모르니)
- 패키지도 다시 설치합니다.

```bash
pip install -r requirements.txt
```

- phpmyadmin에서 DB를 초기화합니다.
- 다시 DB를 구성합니다

```bash
python manage.py db upgrade
```

## 3. 작업할 브랜치를 만듭니다.
```bash
git branch issue_no_10
git checkout issue_no_10
```

## 4. 브랜치에 개발을 진행합니다.

### 4-1. 새 파이선 패키지의 설치가 필요할 때는
해당 패키지 명을 requirements.txt에 추가합니다.

### 4-2. DB구조에 변화를 주었을 때는 Migrate 스크립트를 만듭니다.
```bash
python manage.py db migrate
python manage.py db edit  # 꼭 확인!
python manage.py db upgrade
```
- Migrate 후 꼭 생성된 파일을 edit 명령으로 확인해봅시다.

### 4-3. 커밋을 하기 전에, 개발을 끝내기 전에, 잘 돌아가는지 확인해봅시다!

### 4-4. 혹시 다른 개발자에게 알려야 할 일이 있을 경우, README.md를 수정합시다.
mac에서는 macdown프로그램을 추천합니다.

## 5. 커밋메세지에 자신이 작업한 Issue의 번호와 이름을 기록합니다.
```bash
git add 작업한 파일들
git commit -m "Issue #10, '오늘 하루도 수고하셨습니다.'라고 추가하고싶습니다."
git push origin issue_no_10
```

## 6. 선배를 괴롭힙니다.
Issue에 선배를 소환한 후, 코드리뷰를 받습니다.

## 7. 완료 후  master 브랜치에 머지를 합니다.
```bash
git checkout master
git merge issue_no_10
git push origin master
```
이 때 문제가 일어날 수 있습니다.
(선배를 부르세요!)
