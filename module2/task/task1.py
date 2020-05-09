import requests
import re
from requests.packages import urllib3
import logging

logging.captureWarnings(True)
urllib3.disable_warnings()

args = {
    'name': 'rocketeerli',
    'age': 24
}

cookies = '_octo=GH1.1.2001408838.1585102724; _ga=GA1.2.669589782.1585102727; experiment:homepage_signup_flow=eyJ2ZXJzaW9uIjoiMSIsInJvbGxPdXRQbGFjZW1lbnQiOjM4LjM4NzkxNjQzMjMxODI2LCJzdWJncm91cCI6bnVsbCwiY3JlYXRlZEF0IjoiMjAyMC0wMy0yNVQwMjoxODo0Ni42NDlaIiwidXBkYXRlZEF0IjoiMjAyMC0wMy0yNVQwMjoxODo0Ni42NDlaIn0=; tz=Asia%2FShanghai; _device_id=71170c2e9184afc190651d3db26106fe; user_session=wjCc8oWXqtIhetfVsrRdvxFZM2FFtiDOsrHIMt50S04QwkaV; __Host-user_session_same_site=wjCc8oWXqtIhetfVsrRdvxFZM2FFtiDOsrHIMt50S04QwkaV; logged_in=yes; dotcom_user=rocketeerli; has_recent_activity=1; _gat=1; _gh_sess=GCUOzVInojxiu%2FNkmaTRFiP1lmygp9DQj4SnRH2g%2FfQir55PrGcOHhyGYFaYxq5oPATuIdHE5E7s1QBE5ZizEzz8xNK8iJcNJSCnKHcHtI%2FU0DVJpWiUcrsr%2FARAJVIF6sHYOLDUyUWFzC498arMuWGAQXobkBcSvG5%2BSlMR2HMASRs0r494qdcUSHPMpUDNcMTdWPDuYfmYvFh0M%2BC%2FJDOtro7iljND0sTWDjV3Xrx2MN4ubNe8EN1tkqbygw%2BiQPQ6LG7EchRWkxFjBfQUGJwT%2B9G2qEnERruynrRXzOBVqG6liLXI88R2zSyi1K7IkQ9CpNai%2BsD2seDqgywu6mgn284asME6PLx2P%2Fe4p%2F7gD7WYqFvbjlYX02VIoT%2BE7UA78UO9E0Ho%2B5aoD4OlPVwmiRvBjjnBa8STc%2BrseMDeTRvVJ3vDGcMC1O1LN4GS0IhXI2%2FzWusSKOH7C%2Fqx7IsRVm0dXe43Rq6tmKuCbaWwHobqTITYbwdrIJlxvDa%2BIWysdm4l34pZani4QzBqJnnwbOOxsSoFBNUgI3Q8AqmuBXbuwDo4NiksCfg7POkBtnpksD7iWwKB%2Bbwl%2Bqrbh9yshbv84WOL6l3SkSI3o6xHnw2M4qu4kMA5JG%2Fg%2BxRaCBwVc7timnliZiTGBX84KWPYpDPtM1qPwRobqRdpZIZyhrjh2goiQQYRLLHWiMbFC3oPxAH51HKWQq9Az9mhYi01DJ57sIFUYM5MpL46M2UNp6j15WfvOIbqWu7zCaDnvuldU75CAjPJIizlgagQqpjxNet1IH9CSdX54bxhlNWkGZsxJ30N%2BCm0boo3QT0%2BHR7fbP2XdP%2F3egkrhO%2FbDs57NmPV3E5TnF%2BvpKKvGuWr6RwdZtNp%2FEOq0PG7xSGhJmcJUDr6oxE6JIscNFxsisdvY66FW6eH2MBsKpG1MJjhs27eSX0WhH%2B96AGKpVopSdfNHCB66tdpTnM%2FAvlEK9ubfpV%2BGRRgCuCoRs0yNNltNuPT7lydgVRCSXDSJ3pY6AwrgC0Z%2FOokubxs4yKO5KlPB1fEm6Pu43D8XPleQhZNNipHw0yyKNHNK%2B2mUVN04TXnn9dKmw2PhiJ6WxArDE2OokKaEMLartzYbvwkI0vgy2keeaNfNTnu5%2FSjn%2BkUzkmXm2Ia5kBk%2FwGDqFChULEZfVHSKqSe%2F%2BQDjGZwwZkezvX3NhkI%2BukFVZf%2BXOsXmEAPVVJBwtdlOcJYyOItmI4%2BJnR9i2eu2BYGs1DrCtPOQ%2FXetw493zfV%2BvGkTUN%2BLkhXg8w21K3v6tlwTsiV80oPj1fpE3RI0hgAI4jcQ%2BmrbO%2FVcdXSx%2FhW4Few2VNq6hiphoI%2FttSFQOzPq5JMcjEpl4O54OJAtsuw5eTlOJ44cMiFGZSsJ4bMLUvrzhO7PgCAkvBrlnSuvpcbYA0m%2B67ZyV0Vs16RuMEZBrIAj6LuaDX4v7C3x2Lx9PEupw6NwPnN9f0fynQNPidCd5jB2Axe1y0TPzKwWnj50qrSbC2FRMrGFz9coMCDeVYZ4p1fgGAzYNCNWqhbZCaNEnrKLR5q8fJhLoQNH22edNQC35E4LncETJukBhBSDBxuxsoJ2%2BFWaX7oojUmQAzHOoBwckkoQrCxP8aCrC0sGI0J1roufEY39HGeFT23PBiMGKVIP4Fa4fJ7mlP1P9t%2Bfvv5hdz9eUHWqd1dox1bXZJn9h47Lts6m96sZPuoS6XwN20YtYXm7lZ%2Bzrlu2Tl4l2ly1C28ECRWIOWfrdn%2F2HtLE3feCvv5%2BNJmK0eJHwF%2BZ2CDLe5v2Eh1zhtMNJw%2FozFvklWxGtikZaMoNKtvdKMO9mEmYfda2xdosJSHID21oP7MVuG5FfWOobMUQllCOqO6KgWveEjRH8jcHUTfH%2Fb%2F9RA%2B8em%2B2XsbD1EmCC69bAk48RYNiK1y%2B%2BxKjQIc%2B4N5VcuUgCODXHCa--tcLpB0iaz4g5TDE6--DsdjVx9avVuaWKdetekXRw%3D%3D'

headers = {
   'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}

jar = requests.cookies.RequestsCookieJar()
for cookie in cookies.split(';'):
    key, value = cookie.split('=', 1)
    jar.set(key, value)
# 设置 cookie 和 连接、等待的超时时间, timeout默认None，永久等待
r = requests.get('https://github.com/', cookies=jar, headers=headers, timeout=(5, 30))
# print(r.text)

## GET 请求

# r = requests.get('http://httpbin.org/get', params=args)
# print(type(r.text))
# print(r.json())
# print(type(r.json()))

r = requests.get('https://static1.scrape.cuiqingcai.com/', headers=headers)
exit() if not r.status_code == requests.codes.ok else print('Request Successfully')
pattern = re.compile('<h2.*?>(.*?)</h2>', re.S)
titles = re.findall(pattern, r.text)
print(titles)

#r = requests.get('https://github.com/favicon.ico')
#with open('favicon.ico', 'wb') as f:
#    f.write(r.content)

print(type(r.status_code), r.status_code)
print(type(r.headers), r.headers)
print(type(r.cookies), r.cookies)
print(type(r.url), r.url)
print(type(r.history), r.history)

# cookies
r = requests.get('http://www.baidu.com')
print(r.cookies)
for key, value in r.cookies.items():
    print(key, '=', value)

## POST 请求
files = {
    'file': open('favicon.ico', 'rb')
}
r = requests.post("http://httpbin.org/post", data=args, files=files)
#print(r.text)


## Session
s = requests.Session()
s.get('http://httpbin.org/cookies/set/number/12475893')
r = s.get('http://httpbin.org/cookies')
print(r.text)


## SSL 证书
response = requests.get('https://static2.scrape.cuiqingcai.com/', verify=False)
print(response.status_code)

## 身份认证
from requests.auth import HTTPBasicAuth

#r = requests.get('https://static3.scrape.cuiqingcai.com/', auth=HTTPBasicAuth('admin', 'admin'))
r = requests.get('https://static3.scrape.cuiqingcai.com/', auth=('admin', 'admin'))
print(r.status_code)
