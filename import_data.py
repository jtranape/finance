#This import financial data from divers sources and save them as pickle. If the data are not uptodate anymore, all you need is to delete them so that they will be updated

import array
import requests
import pandas as pd
import time
import datetime
import random
import bs4 as bs
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import io

def summary(Ticker):
	#We need price and market Cap
	try:
		df=pd.read_pickle("./data/summary_"+Ticker+".pkl")											#we don't want to scrap yahoo if we already saved the data localy
	except:			
		print("Data doesn't exist, importing...")													#if we don't have the data localy, we get them and save them locally
		URL="https://finance.yahoo.com/quote/"+ Ticker
		dfread=pd.read_html(URL)
		df=dfread[0]
		for i in range(1,len(dfread)):																#merging datafrane
			df=df.append(dfread[i])
		df=df.set_index(0, inplace=False)
		try :
			df.loc['Market Cap'].iat[0]=df.loc['Market Cap'].iat[0].replace("M","*1000000")				#Convert million	
			df.loc['Market Cap'].iat[0]=df.loc['Market Cap'].iat[0].replace("B","*1000000000")			#Convert billion
			df.loc['Market Cap'].iat[0]=df.loc['Market Cap'].iat[0].replace("T","*1000000000000")		#Convert trillion
		except:
			print("nothing to replace")
		df.loc['Market Cap'].iat[0]=pd.eval(df.loc['Market Cap'].iat[0])
		print(df)
		#df=	pd.eval(df,inplace=True)
		df.to_pickle("./data/summary_"+Ticker+".pkl")												#save scrapped data
		time.sleep(random.random())
	print("\nMarket data for "+ Ticker +" : " )
	print(df)
	
	return(df)

def key_statistics(Ticker):
	try:
		df=pd.read_pickle("./data/key_statistics_"+Ticker+".pkl")									#we don't want to scrap yahoo if we already saved the data localy
	except:	
		URL="https://finance.yahoo.com/quote/"+Ticker+"/key-statistics"
		dfread=pd.read_html(URL)
		df=dfread[1]
		for i in range(2,len(dfread)):																#merging datafrane
			df=df.append(dfread[i])
		df=df.set_index(0, inplace=False)
		df.to_pickle("./data/key_statistics_"+Ticker+".pkl")										#save scrapped data
		time.sleep(random.random())
	print("\nKey statistics for "+ Ticker +" : " )
	print(df)
	
	return(df)

def historical_data(Ticker, days):	
	#reading historical data
	#dfs1=pd.read_html(URLhistory)-->This would give us only 3 months of data therefore it is better to download the data as csv and read it
	#https://query1.finance.yahoo.com/v7/finance/download/TOT?period1=1552489321&period2=1584111721&interval=1d&events=history&crumb=SyAISp1rhi7 ->This is how the URL to download the CSV looks like. We need period 1, period 2 and crumb
	#ttm means trailing 12 months meaning last 4 quarters earning.
	try:
		df=pd.read_pickle("./data/historical_data_"+Ticker+".pkl")									#we don't want to scrap yahoo if we already saved the data localy	
	except:	
		print("Data doesn't exist, importing...")
		period_end=int(time.mktime(datetime.date(datetime.datetime.today().year,datetime.datetime.today().month,datetime.datetime.today().day).timetuple()))#timestanp for last trading day (yesterday)
		period_begin=period_end-60*60*24*days#this would be for 1 year or 365 days
		URLhistory="https://finance.yahoo.com/quote/"+Ticker+"/history?period1="+str(period_begin)+"&period2="+str(period_end)+"&interval=1d&filter=history&frequency=1d"

		options = webdriver.ChromeOptions()
		options.add_experimental_option("prefs", {
		    #"download.default_directory": r"yahoo_data",
		    "download.prompt_for_download": False,
		    "download.directory_upgrade": True#,
		})
		driver = webdriver.Chrome(options=options)
		crumb = None
		driver.get(URLhistory)
		time.sleep(1)
		button = driver.find_element_by_name('agree') 												#agree to GDPR prompt
		button.click()
		time.sleep(3)
		#button = driver.find_element_by_xpath("// a[. // span[text() = 'Download Data']]") 		#outdated, doesn't work anymore
		button = driver.find_element_by_xpath("//*[@id=\"Col1-1-HistoricalDataTable-Proxy\"]/section/div[1]/div[2]/span[2]/a")
		time.sleep(2)
		link = button.get_attribute("href")
		print(link)
		#a = urlparse(link)
		crumb = link[len(link)-link.find("crumb"):]													#find crumb in link and take right part
		print(crumb)
		URLhistorydownload="https://query1.finance.yahoo.com/v7/finance/download/"+Ticker+"?period1="+str(period_begin)+"&period2="+str(period_end)+"&interval=1d&events=history&crumb="+crumb
		
		driver.get(URLhistorydownload)
		time.sleep(3)
		driver.close()
		#URLhistory="https://query1.finance.yahoo.com/v7/finance/download/"+Ticker+"?period1=1552254787&period2=1583877187&interval=1d&events=history&crumb=SyAISp1rhi7"
		
		#s=requests.get(URLhistory).content
		df=pd.read_csv('C:/Users/jtran_000/Downloads/'+Ticker+'.csv', header=0)						#reading the CSV file with panda		
		df=df.set_index('Date', inplace=False)
		df.index=pd.to_datetime(df.index)															#convert first column to datetime
		df.to_pickle("./data/historical_data_"+Ticker+".pkl")										#save scrapped data			
	print("\nHistorical data for "+ Ticker +" : " )
	print(df)
	return df

def profile(Ticker):
	#this is important for multiple analysis to know the industry
	column=['Sector','Industry']
	try:
		df=pd.read_pickle("./data/profile.pkl")												
	except:	
		print("Data doesn't exist, importing...")
		df=pd.DataFrame(index=[], columns=column)
		
	if df.index.isin([Ticker]).any():																##check if the value exists
		print("The industry and sector for this ticker is already known")							#we don't want to scrap yahoo if we already saved the data localy
		sector=df.loc[Ticker].iat[0]
		industry=df.loc[Ticker].iat[1]
		print("\nSector :"+ sector +"\nIndustry"+ industry)
	else:
		URL="https://finance.yahoo.com/quote/"+Ticker+"/profile"
		r= requests.get(URL)
		data=r.text
		soup=bs.BeautifulSoup(data,'lxml')#html.parser')
		container=soup.findAll("span", class_='Fw(600)')		
		r.close()
		sector=container[0].text		
		industry=container[1].text	
		#dftemp=pd.DataFrame(, columns=column, index=[Ticker])
		#df=df.append(dftemp)

		df.loc[Ticker]=[sector,industry]
		#print(dftemp)
		df=df.drop_duplicates()
		#df=df.drop_na()
		print(df)
		df.to_pickle("./data/profile.pkl")															#save scrapped data
		time.sleep(random.random())
	print("\nIndustry data for "+ Ticker +" : " )
	print(df)
	return(sector, industry)

	#//*[@id="Col1-0-Profile-Proxy"]/section/div[1]/div/div/p[2]/span[2]

def financial_statement_old(Ticker,statement):
	#all numbers are in 1000
	#we could also get the data from simfin.com
	try:
		df=pd.read_pickle("./data/"+statement+"_"+Ticker+".pkl")									#we don't want to scrap yahoo if we already saved the data localy	
	except:	
		print("Data doesn't exist, importing...")
		column=[]
		if statement== 'financials':
			URL="https://finance.yahoo.com/quote/"+Ticker+"/financials"
		elif statement=='balance-sheet':
			URL="https://finance.yahoo.com/quote/"+Ticker+"/balance-sheet"
		elif statement=='cash-flow':
			URL="https://finance.yahoo.com/quote/"+Ticker+"/cash-flow"
		r= requests.get(URL)
		data=r.text
		soup=bs.BeautifulSoup(data,'lxml')#html.parser')

		container=soup.findAll("div", class_='D(tbr)')	
		print(container)				
		for table_data in container[0].find_all('div', class_='D(ib)'):								#initialize header
			column.append(table_data.text)

		df=pd.DataFrame(index=[0], columns=column)													#create empty dataframe with header
		for i in range(1,len(container)):															#we loop for each row of the table starting with row 1 (first row after header)
			j=0
			for col in container[i].find_all('div', class_='D(tbc)'):								#we loop for each column
				#print("i: "+str(i)+"   j: "+str(j)+"    text: "+col.text)
				if j==0:																			#this is the first column, therefore we want to copy it as text
					df=df.append([{'Breakdown': col.text}],ignore_index=True)						#create a new ligne and populate first column
				else:																				#this should be a numerical value
					try:
						df.iloc[-1,j]=float(col.text.replace(',','')) 								#populating the first non valid dataset and convert it to float
					except:
						df.iloc[-1,j]='NaN'
				j=j+1
		r.close()
		df=df.set_index('Breakdown', inplace=False)													#set first column as index
		#df=df.drop(['NaN'])
		df.to_pickle("./data/"+statement+"_"+Ticker+".pkl")											#save scrapped data
		time.sleep(random.random())
	print("\n"+statement + " for "+ Ticker +" : " )
	print(df)	
	return(df)		

def financial_statement(Ticker,statement):
	#all numbers are in 1000
	#we could also get the data from simfin.com
	try:
		df=pd.read_pickle("./data/"+statement+"_"+Ticker+".pkl")									#we don't want to scrap yahoo if we already saved the data localy	
	except:	
		print("Data doesn't exist, importing...")
		column=[]
		if statement== 'financials':
			URL="https://finance.yahoo.com/quote/"+Ticker+"/financials"
		elif statement=='balance-sheet':
			URL="https://finance.yahoo.com/quote/"+Ticker+"/balance-sheet"
		elif statement=='cash-flow':
			URL="https://finance.yahoo.com/quote/"+Ticker+"/cash-flow"
		options = webdriver.ChromeOptions()
		options.add_experimental_option("prefs", {
		    #"download.default_directory": r"yahoo_data",
		    "download.prompt_for_download": False,
		    "download.directory_upgrade": True#,
		})
		driver = webdriver.Chrome(options=options)
		driver.get(URL)
		time.sleep(1)
		button = driver.find_element_by_name('agree') 												#agree to GDPR prompt
		button.click()
		time.sleep(3)
		drop_downs = driver.find_elements_by_class_name('tgglBtn')
		for drop_down in drop_downs:
			drop_down.click()																		#This will just expend the first level but it is ok for now
			time.sleep(1)

		soup=bs.BeautifulSoup(driver.page_source, 'lxml')
		container=soup.findAll("div", class_='D(tbr)')					
		for table_data in container[0].find_all('div', class_='D(ib)'):								#initialize header
			column.append(table_data.text)

		df=pd.DataFrame(index=[], columns=column)													#create empty dataframe with header
		for i in range(1,len(container)):															#we loop for each row of the table starting with row 1 (first row after header)
			j=0
			for col in container[i].find_all('div', class_='D(tbc)'):								#we loop for each column
				#print("i: "+str(i)+"   j: "+str(j)+"    text: "+col.text)
				if j==0:																			#this is the first column, therefore we want to copy it as text
					df=df.append([{'Breakdown': col.text}],ignore_index=True)						#create a new ligne and populate first column
				else:																				#this should be a numerical value
					try:
						df.iloc[-1,j]=float(col.text.replace(',','')) 								#populating the first non valid dataset and convert it to float
					except:
						df.iloc[-1,j]='NaN'
				j=j+1
		df=df.set_index('Breakdown', inplace=False)													#set first column as index
		#df=df.drop(['NaN'])
		df.to_pickle("./data/"+statement+"_"+Ticker+".pkl")											#save scrapped data
		time.sleep(random.random())
		driver.close()
	print("\n"+statement + " for "+ Ticker +" : " )
	print(df)	
	return(df)	

def get_options_date(Ticker):
	try:
		df=pd.read_pickle("./data/options_"+Ticker+".pkl")											#we don't want to scrap yahoo if we already saved the data localy	
	except:	
		URL="https://finance.yahoo.com/quote/"+Ticker+"/options"
		options = webdriver.ChromeOptions()
		options.add_experimental_option("prefs", {
		    #"download.default_directory": r"yahoo_data",
		    "download.prompt_for_download": False,
		    "download.directory_upgrade": True#,
		})
		driver = webdriver.Chrome(options=options)
		driver.get(URL)
		time.sleep(1)
		button = driver.find_element_by_name('agree') 												#agree to GDPR prompt
		button.click()
		time.sleep(10)
		#date_list=driver.find_element_by_xpath("//*[@id=\"Col1-1-OptionContracts-Proxy\"]/section/div/div[1]/select")
		#date_list = [x for x in driver.find_elements_by_xpath("//*[@id=\"Col1-1-OptionContracts-Proxy\"]/section/div/div[1]")]
		date_list = [x for x in driver.find_elements_by_xpath("//*[@id=\"Col1-1-OptionContracts-Proxy\"]/section/div/div[1]/select/option")]
		time.sleep(1)
		#date_list.click()
		df=pd.DataFrame(index=[], columns=['Date_code'])
		for element in date_list:
			df.loc[element.get_attribute("text")]=element.get_attribute("value")
		print(df)



def options(Ticker):
	try:
		df=pd.read_pickle("./data/options_"+Ticker+".pkl")											#we don't want to scrap yahoo if we already saved the data localy	
	except:	
		print("Data doesn't exist, importing...")
		URL="https://finance.yahoo.com/quote/"+Ticker+"/options"
		try:
			dfread=pd.read_html(URL,header=0)
			df=dfread[0]
			for i in range(1,len(dfread)):															#merging datafrane
				df=df.append(dfread[i])
			df=df.set_index('Contract Name', inplace=False)
			df.to_pickle("./data/options_"+Ticker+".pkl")											#save scrapped data
			time.sleep(random.random())
		except:
			print("No options for this company")
			df=""
	print("\nOptions for "+ Ticker +" :" )
	print(df)
	return(df)

def shares_outstanding(stock):
	share_outstanding=stock.key_statistics.loc['Shares Outstanding 5'].values
	share_outstanding[0]=share_outstanding[0].replace("M","*1000000")	#Convert million
	share_outstanding[0]=share_outstanding[0].replace("B","*1000000000")	#Convert billion
	share_outstanding=pd.eval(share_outstanding)
	print(share_outstanding[0])
	return share_outstanding[0]

def price(stock):
	price=stock.summary.loc['Open'].values															#for now we take the opening price but we could take an average of bid and ask price
	print("\nPrice: "+price[0])
	return float(price[0])	

def riskfreerate(exchange, maturity): #get riskfreerate, either for US, UK or EU equities
	#let's take bond rate with same time horizon as investment 5 to 10 years
	#^IRX	13 Week Treasury Bill
	#^FVX	Treasury Yield 5 Years
	#^TNX	Treasury Yield 10 Years
	#^TYX	Treasury Yield 30 Years
	#we could also use https://www.bloomberg.com/markets/rates-bonds/government-bonds/
	try:
		df=pd.read_pickle("./data/riskfreerate_"+exchange+".pkl")									#we don't want to scrap yahoo if we already saved the data localy	
	except:	
		print("Data doesn't exist, importing...")
		if exchange == 'US':
			URL="https://www.investing.com/rates-bonds/usa-government-bonds"
		elif exchange == 'UK':
			URL="https://www.investing.com/rates-bonds/uk-government-bond"
		elif exchange == 'EU':
			URL="https://www.investing.com/rates-bonds/germany-government-bonds" 					#for EU we take german bond because it has the lowest yield in Europe and can therefore be considered as the safest bond
		else:
			print("exchange market unknown")
		#to avoid 403 return we use header in the request
		header = {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
			"X-Requested-With": "XMLHttpRequest"
			}
		r=requests.get(URL,headers=header)
		dfread=pd.read_html(r.text)
		df=dfread[0]
		df.to_pickle("./data/riskfreerate_"+exchange+".pkl")	
		time.sleep(random.random())
	print("\nRisk-free rate for "+ exchange +" :" )
	print(df)
	for row in df.index:
		if df['Name'][row].find(str(maturity))>=0 and df['Name'][row].find("M")==-1:
			riskfreerate=df['Yield'][row]/100
			break
	print("\n Risk-free rate for "+exchange + " maturity: " + str(maturity) + " years = " + str(riskfreerate))
	return(riskfreerate)
		

def list_market_index():
		#Major index:
		#https://en.wikipedia.org/wiki/NYSE_Arca_Major_Market_Index
		#https://en.wikipedia.org/wiki/List_of_S%26P_500_companies
		#https://en.wikipedia.org/wiki/NASDAQ-100
		#https://en.wikipedia.org/wiki/CAC_40
		#https://en.wikipedia.org/wiki/DAX
		#https://en.wikipedia.org/wiki/FTSE_100_Index
		#https://en.wikipedia.org/wiki/Russell_1000_Index
	index=["NYSE_Arca_Major_Market_Index","List_of_S%26P_500_companies","NASDAQ-100","CAC_40","DAX","FTSE_100_Index","Russell_1000_Index"]
	column=['Company','Ticker']
	global NYSE_Arca_Major_Market_Index																#can be used everywhere
	global List_of_SP_500_companies	
	global NASDAQ_100
	global CAC_40	
	global DAX		
	global FTSE_100_Index
	global Russell_1000_Index	
	for ind in index:
		try:
			df=pd.read_pickle("./data/"+ind+".pkl")													#we don't want to scrap yahoo if we already saved the data localy	
		except:	
			print("Data doesn't exist, importing...")
			URL="https://en.wikipedia.org/wiki/"+ind
			dfread=pd.read_html(URL, header=0)
			df=pd.DataFrame(index=[], columns=column)												#empty dataframe
			if ind=="NYSE_Arca_Major_Market_Index":													#we populate the dataframe
				df=dfread[1][['Company','Symbol']].copy()
				df=df.rename(columns={"Symbol": "Ticker"})
				NYSE_Arca_Major_Market_Index=df
			elif ind=="List_of_S%26P_500_companies":												#we populate the dataframe
				df=dfread[0][['Security','Symbol']].copy()
				df=df.rename(columns={"Security":"Company","Symbol":"Ticker"})
				List_of_SP_500_companies=df
			elif ind=="NASDAQ-100":																	#we populate the dataframe
				df=dfread[2].copy()
				NASDAQ_100=df	
			elif ind=="CAC_40":																		#we populate the dataframe
				df=dfread[3][['Company','Ticker']].copy()
				CAC_40=df	
			elif ind=="DAX":																		#we populate the dataframe
				df=dfread[3][['Company','Ticker symbol']].copy()
				df=df.rename(columns={"Ticker symbol":"Ticker"})
				DAX=df	
			elif ind=="FTSE_100_Index":																#we populate the dataframe
				df=dfread[3][['Company','Ticker']].copy()
				FTSE_100_Index=df	
			elif ind=="Russell_1000_Index":															#we populate the dataframe
				df=dfread[3][['Company','Ticker']].copy()
				Russell_1000_Index=df
			df=df.set_index('Company', inplace=False)
			df.to_pickle("./data/"+ind+".pkl")
			time.sleep(random.random())		
		else:
			if ind=="NYSE_Arca_Major_Market_Index":													#get data from archive										
				NYSE_Arca_Major_Market_Index=df
			elif ind=="List_of_S%26P_500_companies":																		
				List_of_SP_500_companies=df
			elif ind=="NASDAQ-100":														
				NASDAQ_100=df	
			elif ind=="CAC_40":															
				CAC_40=df	
			elif ind=="DAX":															
				DAX=df	
			elif ind=="FTSE_100_Index":													
				FTSE_100_Index=df	
			elif ind=="Russell_1000_Index":												
				Russell_1000_Index=df

		#print("\n "+ ind)
		#sprint(df)
	
def get_index(Ticker):
	list_market_index()																				#get Ticker of major index
	#index=["NYSE_Arca_Major_Market_Index","List_of_S%26P_500_companies","NASDAQ-100","CAC_40","DAX","FTSE_100_Index","Russell_1000_Index"]
	if Ticker in NYSE_Arca_Major_Market_Index[['Ticker']].values:
		index="NYSE_Arca_Major_Market_Index"
	if Ticker in List_of_SP_500_companies[['Ticker']].values:
		index="List_of_SP_500_companies"
	if Ticker in NASDAQ_100[['Ticker']].values:
		index="NASDAQ_100"
	if Ticker in CAC_40[['Ticker']].values:
		index="CAC_40"
	if Ticker in DAX[['Ticker']].values:
		index="DAX"
	if Ticker in FTSE_100_Index[['Ticker']].values:
		index="FTSE_100_Index"
	if Ticker in Russell_1000_Index[['Ticker']].values:
		index="Russell_1000_Index"
	else: 
		index="not found"

	print(Ticker + "'s index is "+ index)
	return index


class market_index:
	def __init__(self, Ticker):
		self.ticker=Ticker
		#self.exchange: str=''
		self.historical_data=historical_data(Ticker,1825)											#1825=%years

class company_data:
	cost_of_debt: float 
	cost_of_equity: float
	cost_of_capital: float
	beta: float
	beta_is_fallback: bool = False
	taxrate: float 
	entreprise_value: float
	leverage: float
	potential_gain_loss: float
	def __init__(self, Ticker):
		self.ticker=Ticker
		self.name=''
		self.index=get_index(Ticker)
		self.summary=summary(Ticker)
		self.key_statistics=key_statistics(Ticker)
		self.historical_data=historical_data(Ticker,1825)											#1825=%years
		self.profile=profile(Ticker)																#sector & industry
		self.financial_statement=financial_statement(Ticker,'financials')
		self.cash_flow_statement=financial_statement(Ticker,'cash-flow')
		self.balance_sheet=financial_statement(Ticker,'balance-sheet')
		self.shares_outstanding=shares_outstanding(self)
		self.price=price(self)
		self.options=options(Ticker)


def main():
	#Total=company_data("TOT")
	#profile("TOT")
	company_data("TSLA")

if __name__ == "__main__":
	 main() 
