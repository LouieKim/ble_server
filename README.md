# Energy Meter server(20년 9월 20일)

# 1. Device 등록
1) 사용자가 APP을 통하여 Device를 선택함
2) 해당 Device의 UUID를 서버에 등록함
3) 서버에서 해당 Device의 Site_id(8자리의 문자열) 반환함

/site/add/<device_id>   
변수명: device_id 설명: 사용자가 선택한 Device의 UUID 정보  

Request Example   
"http://127.0.0.1:5000/site/add/4d6fc88b-be75-6698-da48-6866a36ec78e"

Response Example
<pre><code>
정상적인 경우
{
  "site_id" : 12345678
}

이미 등록되어 있을 경우
{
  "error" : "Already registered"
}</code></pre>

# 2. Device 삭제
1) 잘못 등록 했을 경우 사용
2) 개발 또는 테스트 용도 사용

/site/del/<site_id>  
변수명: site_id 설명: 삭제하고자 하는 site_id를 입력함  

Request Example  
http://127.0.0.1:5000/site/del/12345678  

Response Example
<pre><code>
정상적인 경우
{
  "success" : 12345678
}

등록된 site_id가 없을 경우
{
  "error" : "Wrong site_id"
}</code></pre>

# 3. site_id 찾기
1) Device의 UUID를 이용해서 해당 site_id를 확인 또는 찾음

/site/get/<device_id>  
변수명: device_id 설명: device_id의 UUID를 입력함  

Request Example  
http://127.0.0.1:5000/site/get/4d6fc88b-be75-6698-da48-6866a36ec78e

Response Example
<pre><code>
정상적인 경우
{
  "site_id" : 12345678
}

이미 등록되어 있을 경우
{
  "error" : "Wrong device_id"
}</code></pre>

# 4. 전체 site_id 가져오기
1) 개발 또는 테스트 용도

/site/get/all  

Request Example  
http://127.0.0.1:5000/site/all  

Response Example
<pre><code>
정상적인 경우
{
  "site_ids" : [[12345678],[12345679],[12345680],...[12345690]]
}

이미 등록되어 있을 경우
{
  "error" : "um...error"
}</code></pre>

# 5. 수신된 데이터 서버 올리기
1) Device로 부터 수신한 데이터를 서버에 전달함

/history/add/<site_id>/<value>  
변수명: site_id 설명: 등록할 때 서버로부터 받은 site_id  
변수명: value 설명: Device로 수신된 데이터

Request Example  
http://127.0.0.1:5000/history/add/12345678/1234  

Response Example
<pre><code>
정상적인 경우
{
  "success" : 1234
 }

등록된 site_id가 없을 경우
{
  "error" : "Wrong site_id"
}</code></pre>

# 6. 일간 전력 사용량 가져오기
1) 사용자가 지정한 월의 일간 사용량을 가져옴

/history/get/day/<site_id>/<date>  
변수명: site_id 설명: 등록할 때 서버로부터 받은 site_id  
변수명: date 설명: 사용자가 설정한 해당 월 정보  
ex) 20년 9월 -> 2009, 19년 8월 -> 1908  

Request Example  
http://127.0.0.1:5000/history/get/day/12345678/2009  

Response Example
<pre><code>
정상적인 경우
{
  "day_history" : [["2020-09-01 00:00:00", 20],["2020-09-02 00:00:00", 30],["2020-09-03 00:00:00", 40],
  .....
  ["2020-09-24 00:00:00", 100]]
}

등록된 site_id가 없을 경우
{
  "error" : "Wrong site_id"
}</code></pre>

# 7. 월간 전력 사용량 가져오기
1) 사용자가 지정한 월 포함 과거 13개월의 사용량을 가져옴

/history/get/month/<site_id>/<date>  
변수명: site_id 설명: 등록할 때 서버로부터 받은 site_id  
변수명: date 설명: 사용자가 설정한 해당 월 정보  
ex) 20년 9월 -> 2009, 19년 8월 -> 1908  

Request Example  
http://127.0.0.1:5000/history/get/month/12345678/2009  

Response Example
<pre><code>
정상적인 경우
{
  "month_history" : [["2019-09-01 00:00:00", "20"],["2019-10-01 00:00:00", "30"],["2019-11-01 00:00:00", "40"],
  .....
  ["2020-09-01 00:00:00", "100"]]
}

등록된 site_id가 없을 경우
{
  "error" : "Wrong site_id"
}</code></pre>
