import requests
payload = {'entry.1122048754': 'পুরুষ', 'entry.360969613': '23', 'entry.2066022346': 'বিশ্ববিদ্যালয় হল', 'entry.1931149760': '30K', 'entry.2116347128': '5\'5"', 'entry.1188676735': '58', 'entry.1843320193': 'Science', 'entry.1878462445': 'মাস্টার্স', 'entry.143098020': '3.81', 'entry.243962405': 'মাঝে মাঝে', 'entry.987881316': 'অধূমপায়ী', 'pageHistory': '0'}
URL = 'https://docs.google.com/forms/d/e/1FAIpQLSe-2fx_ibOrVF-SIuf6tD5mwAHU_-5HKono73i-i1Sy44fEDw/formResponse'

res=requests.post(URL, data=payload)
print('Status:', res.status_code)
if res.status_code != 200:
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(res.text, 'html.parser')
    for div in soup.find_all('div', {'role': 'alert'}):
        print("ALERT:", div.text)
