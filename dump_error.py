import requests, re
res=requests.post('https://docs.google.com/forms/d/e/1FAIpQLSe-2fx_ibOrVF-SIuf6tD5mwAHU_-5HKono73i-i1Sy44fEDw/formResponse', data={'entry.987881316': 'অধূমপায়ী'})
# find all text in the body to see the error
from bs4 import BeautifulSoup
soup = BeautifulSoup(res.text, 'html.parser')
for div in soup.find_all('div', {'role': 'alert'}):
    print("ALERT:", div.text)
for span in soup.find_all('span', class_='RveJvd'):
    print("RveJvd:", span.text)
