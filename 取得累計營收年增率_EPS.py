
# 由公開資訊觀測站 > 財務報表 > 採IFRS後 > 合併/個別報表 > 綜合損益表 > 取得資料算出 "累計營收年增率","EPS" 
# ---------------------------------------------------------------------------------------------------------------------------------------
import pandas as pd
import requests
from bs4 import BeautifulSoup

stock_num = input('Please enter the stock number (ex, 2330): ')
year = input('Please enter the year (ex, 108): ')
season = input('Please enter the season (1~4): ')
url = 'https://mops.twse.com.tw/mops/web/ajax_t164sb04'
#payload = {'encodeURIComponent':1,'step': 1,'firstin': 1,'off': 1,'queryName': 'co_id','inpuType': 'co_id','TYPEK': 'all','isnew': 'true','co_id': 2330}
payload = {'encodeURIComponent': 1,'step': 1,'firstin': 1,'off': 1,'queryName':'co_id','inpuType':'co_id','TYPEK':'all','isnew':'false','co_id':stock_num,'year':year,'season':season}
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
list_req = requests.post(url, data = payload, headers = headers)
soup = BeautifulSoup(list_req.content,'lxml')
# debug msg
#print(soup.prettify())
#print(soup.text)

td_list = []
eps_list = []
tdflag = 0
epsflag = 0
td_label = soup.find_all('td')
for td_tag in td_label:
    if td_tag.string == '營業收入合計':
        tdflag=1
        #print(td_tag.string,tdflag)
    elif td_tag.string == '營業成本合計':
        tdflag=0
    elif tdflag == 1:
        #print(td_tag.string)
        td_list.append(td_tag.string)
    else:
        if td_tag.string == '營業成本合計':
            break

for td_tag in td_label:
    if td_tag.string == '基本每股盈餘':
        epsflag = 1
    elif epsflag == 1:
        #print(td_tag.string)
        eps_list.append(td_tag.string)
    else:
        epsflag=0
if int(season)==2 or int(season)==3 or int(season)==4:
    eps_value = float(eps_list[9])
else:
    eps_value = float(eps_list[5])
#print(eps_value)

#print(td_list)
if int(season)==2 or int(season)==3 or int(season)==4:
    Cumulative_income = td_list[4].replace(',','')
    Cumulative_income_of_the_previous_year = td_list[6].replace(',','')
    #print(Cumulative_income)
    #print(Cumulative_income_of_the_previous_year)
else:
    Cumulative_income = td_list[0].replace(',','')
    Cumulative_income_of_the_previous_year = td_list[2].replace(',','')
    #print(Cumulative_income)
    #print(Cumulative_income_of_the_previous_year)

# 累計營收年增率
# 今年以來累計營收較去年同期累計營收的成長率
# 計算公式 = (今年以來累計營收 - 去年同期累計營收) / 去年同期累計營收 * 100%
revenue = int(Cumulative_income)-int(Cumulative_income_of_the_previous_year)
revenue = (revenue/int(Cumulative_income_of_the_previous_year))*100
#print(revenue)
print('--------------------------------------')
print('今年以來累計營收 :',int(Cumulative_income))
print('去年以來累計營收 :',int(Cumulative_income_of_the_previous_year))
print('單位：新台幣仟元')
print('--------------------------------------')
print('累計營收年增率 :',round(revenue,2),'%')

# 基本每股盈餘(EPS)
print(year,'第',season,'季EPS: ',eps_value)
#print('本季EPS為: ',eps_value)














# Other method, but has the bug
#---------------------------------------------------------------------
#eps_list = []
#eps = soup.select('tr')[49]
#for eps_index in range(0,8):
#    component = eps.select('td')[eps_index].text
#    print(component)
#    if component:
#        eps_list.append(component)

#eps1 = pd.Series(eps_list)
##print(eps1)

#revenue = []
#soup = soup.select('tr')[7]
## print(soup)
## print(soup.select('td')[0]) # 營業收入合計
## print(soup.select('td')[1]) # 108年第3季營收
## print(soup.select('td')[3]) # 107年第3季營收
#for num in range(0,8):
#    component = soup.select('td')[num].text

#    if component:
#        revenue.append(component)
#ds = pd.Series(revenue)
#ds1 = ds[5].replace(',','')
#ds2 = ds[7].replace(',','')

## 累計營收年增率
## 今年以來累計營收較去年同期累計營收的成長率
## 計算公式 = (今年以來累計營收 - 去年同期累計營收) / 去年同期累計營收 * 100%
#revenue = int(ds1)-int(ds2)
#revenue = (revenue/int(ds2))*100
##print(revenue)
#print('--------------------------------------')
#print('今年以來累計營收 :',int(ds1))
#print('去年以來累計營收 :',int(ds2))
#print('單位：新台幣仟元')
#print('--------------------------------------')
#print('累計營收年增率 :',round(revenue,2),'%')

## 基本每股盈餘(EPS)
#print(year,'第',season,'季EPS: ',round(float(eps1[1]),2))
#---------------------------------------------------------------------
