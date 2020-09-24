# ble_server
1. Device 등록
  1) 사용자가 APP을 통하여 Device를 선택함
  2) 해당 Device의 UUID를 서버에 등록함
  3) 서버에서 해당 Device의 Site_id(8자리의 문자열) 반환함

/site/add/<device_id>
변수명: device_id 설명: 사용자가 선택한 Device의 UUID 정보

Request Example
http://127.0.0.1:5000/site/add/4d6fc88b-be75-6698-da48-6866a36ec78e

Response Example
정상적인 경우
{
  "site_id" : "10000001"
}

이미 등록되어 있을 경우
{
  "error" : "Already registered"
}

2. Device 삭제
1) 잘못 등록 했을 경우 사용
2) 개발 또는 테스트 용도 사용

/site/del/<site_id>
변수명: site_id 설명: 삭제하고자 하는 site_id를 입력함

Request Example
http://127.0.0.1:5000/site/del/10000001

Response Example
정상적인 경우
{
  "success"
}

등록된 site_id가 없을 경우
{
  "error" : "Wrong site_id"
}

<pre><code>{if __name__ == "__main__":
print("asdasd")
}</code></pre>

3. 







