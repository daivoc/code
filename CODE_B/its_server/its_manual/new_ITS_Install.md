# 아이티에스 (ITS) 설치 및 설정

### PI > UTILITY내 기능
> | Action | setup_its.sh | licenseKey.pyc | productKey.pyc | ipSetup.pyc |
> | ---: | :---: | :---: | :---: | :---: |
> | Code 패치 | ⭕ | ❌ | ❌ | ❌ |
> | Web 패치 | ⭕ | ❌ | ❌ | ❌ |
> | DB 갱신 | ⭕ | ❌ | ❌ | ❌ |
> | Title 등록 | ⭕<br />(ECOS) | ⭕<br />(신규)  | ❌ | ❌ |
> | License | ⭕ | ⭕ | ❌ | ❌ |
> | IP/Subnet/GW | ❌ | ❌ | ❌ | ⭕ |
> | 와치독 IP | ❌ | ❌ | ❌ | ⭕ |
> | NTP IP | ❌ | ❌ | ❌ | ⭕ |
> | 실행순서 | ⭕ | ⭕ | ⭕ | ❌ |
> | 공간확장 | ⭕<br />(Reboot) | ❌ | ❌ | ❌ |
<br />

### **ITS SD Image Download**

> ##### 최신의 부팅 이미지 및 프로그램 다운로드 가능
### [SD Image](http://119.207.126.79/its_server/ecosSdImg/tinyfilemanager.php)
```
ID      : pi
PASS    : its_iot
```

### **Batch of Run Command**
> ##### $ ip='119.207.126.79' && cd ~/utility && scp pi@$ip:ecos_ITS_Download/code/utility/setup_its.sh . && ./setup_its.sh $ip;  
<br/>

### **utility -> setup_its.sh 기능**
> ##### 최신 프로그램으로 GUI를 포함한 코드및 데이터 베이스를 동기화 한다.
> ##### 자동으로 오너 및 그룹 권한을 재설정 한다.
> ##### IP Address 변경은 없이 현재 접속된 IP가 고정으로 설정 된다.
> ##### 기본 타이틀인 **ECOS**로 등록된 라이센스를 발급 한다.
> ##### SD Card 용량(Root File System)을 자동으로 최대화 시킨다.
<br />

1. 웹 갱신
1. 프로그램 갱신
1. 데이터베이스 갱신
1. 설정파일 권한변경
	+ 타이틀 등록 - ECOS
	+ 라이센스 등록
	+ 신규 IP 등록 - 현재 사용중인 IP
	+ 프로그램 등록 - (사용자 선택 등록)
	+ ITS Server 등록
1. SD 저장공간 확장

### **utility -> licenseKey.pyc 기능**
> ##### 사용자 타이틀명 자동 등록 가능
> ##### 사용자 IP Address 변경 또는 설정이 가능하다.
> ##### 라이센스를 발급 및 자동으로 등록한다.
<br />

1. 타이틀 등록 - (사용자 등록)
1. 라이센스 등록
1. 프로그램 등록 - (사용자 선택 등록)
1. ITS Server 등록

### **ITS Server URL**
### [its_server](http://119.207.126.79/its_server/)
```
ID      : manager
PASS    : manager
```

![Logo](https://avatars.githubusercontent.com/u/9473978?s=42&v=4) 