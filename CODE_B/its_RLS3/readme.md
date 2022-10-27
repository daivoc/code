	## 영역제한(areaFilter) 사전정의
	## 영역제한은 거부(denyGroup)그룹이 우선 적용된다.
	if len(config["maskCoord"]["denyGroup"]):
		areaFilter = "denyGroup"
	elif len(config["maskCoord"]["allowGroup"]):
		areaFilter = "allowGroup"
	else:
		areaFilter = "ignoreGroup"
		
	## 크기제한(sizeFilter) 사전정의
	## 최소크기 또는 최대크기 조건 제한
	if config["size"]["min"] and config["size"]["max"]:
		sizeFilter = "both"
	elif config["size"]["min"]:
		sizeFilter = "min"
	elif config["size"]["max"]:
		sizeFilter = "max"
	else:
		sizeFilter = "none"


{
    "camUrl": "rtsp://root:optex5971@192.168.0.126",
    "holeTime": 1,
    "cntPreShotMax": 20,
    "cntPostShotMax": 10,
    "description": "location on vancouver",
    "memo": ""
}