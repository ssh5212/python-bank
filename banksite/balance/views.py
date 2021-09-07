from django.http.request import QueryDict
from django.shortcuts import render
from bs4 import BeautifulSoup
from urllib.request import urlopen

def get_data(symbol):
	url = 'http://finance.naver.com/item/sise.nhn?code={}'.format(symbol)
	with urlopen(url) as doc:
		soup = BeautifulSoup(doc, 'lxml', from_encoding='euc-kr')
		cur_price = soup.find('strong', id='_nowVal')
		cur_rate = soup.find('strong', id='_rate')
		stock = soup.find('title')
		stock_name = stock.text.split(':')[0].strip()
		return cur_price.text, cur_rate.text.strip(), stock_name

def main_view(request):
	querydict = request.GET.copy()
	mylist = querydict.lists() # get 방식으로 넘어온 URL을 리스트 형태로 변환
	rows = [] # 한 줄에 하나의 주식 정보를 가지고 있음
	total = 0 # 전체 주식 금액

	for x in mylist:
		cur_price, cur_rate, stock_name = get_data(x[0])
		price = cur_price.replace(',', '')
		stock_count = format(int(x[1][0]), ',') # 천의 자리마다 ,적용
		sum = int(price) * int(x[1][0])
		stock_sum = format(sum, ',')
		rows.append([stock_name, x[0], cur_price, stock_count, cur_rate, stock_sum]) # rows 리스트에 내용 추가
		total = total + int(price) * int(x[1][0]) # 평가금액 * 주식 수
	
	total_amount = format(total, ',')
	values = {'rows' : rows, 'total' : total_amount} # html에 전달할 파일 딕셔너리 형태로 저장
	return render(request, 'balance.html', values) # render를 통해 html 파일을 표기하고 values 데이터를 넘겨줌


