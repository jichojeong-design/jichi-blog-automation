import urllib.request
import re

url = "https://blog.naver.com/PostTitleListAsync.naver?blogId=jcjung1401&viewdate=&currentPage=1&categoryNo=7&parentCategoryNo=&countPerPage=25"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req) as resp:
    raw_bytes = resp.read()
    # Find title="...
    m = re.findall(b'"title":"([^"]+)"', raw_bytes)
    for title_bytes in m:
        print("Raw bytes:", title_bytes[:50])
