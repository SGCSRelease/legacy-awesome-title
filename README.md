#Project Name : AwesomeTitle (http://title.reluv.me)
릴리즈의, 릴리즈에 의한, 릴리즈를 위한 **별명/업적 관리 사비스**

- 이 서비스는 RELEASE 인들의 친목도모와 프로젝트 소그룹 및 업적관리를 목표합니다.
- 후배님을 위한 개발 가이드라인 => [개발하는법](https://github.com/minhoryang/AwesomeTitle/blob/master/DEVELOPMENT.md)

-----
##현재까지 구현한 기능
1. 회원가입 [Issue #1](https://github.com/minhoryang/AwesomeTitle/issues/1)
  - ID 중복체크 [Issue #4](https://github.com/minhoryang/AwesomeTitle/issues/4)
2. 로그인 [Issue #12](https://github.com/minhoryang/AwesomeTitle/issues/12)
3. 프로필 사진 업로드 [Issue #11](https://github.com/minhoryang/AwesomeTitle/issues/11)
4. 별명 관리 [Issue #7](https://github.com/minhoryang/AwesomeTitle/issues/7)
  - 별명 추천받기 [Issue #9](https://github.com/minhoryang/AwesomeTitle/issues/9) 
5. 릴리즈 사람 찾기 [Issue #5](https://github.com/minhoryang/AwesomeTitle/issues/5)

##개발 중인 기능
1. 별명관리 UI
2. 

##앞으로 구현할 기능 
## 릴리즈 사람들을 찾을 수 있어요! [#3](https://github.com/minhoryang/AwesomeTitle/issues/3)
아래 URL들은 다 같은 페이지를 보여줄 겁니다. 어떻게? [#5](https://github.com/minhoryang/AwesomeTitle/issues/5)

### 이름
한글/영어/중국어/... 이름

- http://title.reluv.me/양민호
- http://title.reluv.me/minhoryang

#### Q. 이름이 겹칠 수 있지 않나요?
와... 이 문제 어떻게 해결하죠? **[TODO]**

#### Q. 영어이름 오타는 어떡하죠?
검색 엔진을 붙여야겠네요 ㅠㅠ

### 자주쓰는 아이디
- http://title.reluv.me/minhoryang
- http://title.reluv.me/gnayrohnim
- http://title.reluv.me/angryonhim

우리 사이트에 `회원가입했던 아이디` + `자신이 자주 쓰는 아이디를 추가`할 수 있습니다.

#### Q. 선점하면 어떡하죠?
A. 뭐 어떡합니까 ;ㅅ;ㅠㅠ

#### Q. 저걸로 다 로그인 할 수 있도록 해주세요!

### 별명(닉네임) [#7](https://github.com/minhoryang/AwesomeTitle/issues/7)
**이게 메인입니다.**
자신이 평상시에 쓰는 `닉네임을 등록`할 수 있고, 다른 `친구들이 별명을 추천`해줄 수 있습니다. `추천받은 별명이 마음에 드는 경우, 관리자 페이지에서 추가`할 수 있습니다!

- http://title.reluv.me/서버노예

#### 별명 추천 [#9](https://github.com/minhoryang/AwesomeTitle/issues/9)

### 이메일 [#6](https://github.com/minhoryang/AwesomeTitle/issues/6)
자신이 사용하는 `메일을 추가`할 수 있어요!
`주로 사용하는 메일`도 지정할 수 있어요.

- http://title.reluv.me/minhoryang@gmail.com

### 휴대폰 번호 [#8](https://github.com/minhoryang/AwesomeTitle/issues/8)
- http://title.reluv.me/01062473590
- http://title.reluv.me/62473590
- http://title.reluv.me/010-6247-3590
- http://title.reluv.me/6247-3590

-----
## 릴리즈 내에서 그룹을 나눌 수 있어요!

### 소그룹

### 업적

### Q. 소그룹이나 업적에는 별명을 붙일 수 없나요?

-----
## 회원가입 /newbie [#1](https://github.com/minhoryang/AwesomeTitle/issues/1)

## 기능 /api
### /api/register [#1](https://github.com/minhoryang/AwesomeTitle/issues/1)
### /api/login
### /api/check_id [#4](https://github.com/minhoryang/AwesomeTitle/issues/4)
### /api/check_hakbun [#4](https://github.com/minhoryang/AwesomeTitle/issues/4)
### /api/admin/...

-----
## 관리 페이지
### /<사람>/admin
### /<그룹>/admin

-----
## Q. 너무 많은 개인정보를 공개하는거 아닌가요?
### 로그인을 해야 볼 수 있는 정보를 선택하고 싶어요.
