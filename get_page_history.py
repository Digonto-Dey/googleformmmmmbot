import requests, re
res=requests.get('https://docs.google.com/forms/d/e/1FAIpQLSe-2fx_ibOrVF-SIuf6tD5mwAHU_-5HKono73i-i1Sy44fEDw/viewform')
matches = re.findall(r'name="pageHistory" value="(.*?)"', res.text)
print("pageHistory:", matches)
