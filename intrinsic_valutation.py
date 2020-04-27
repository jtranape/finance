#valuation of the business based on own performance and expected cashflow as opposed to multiple valuation
import import_data
import pandas as pd
import numpy as np
import datetime
import statsmodels.api as sm
from scipy.optimize import curve_fit
#from statsmodels import regression
#from sklearn.preprocessing import PolynomialFeatures
#from sklearn import linear_model
import matplotlib.pyplot as plt

def get_exchange(Ticker):
	index=import_data.get_index(Ticker) 
	if (index=="NYSE_Arca_Major_Market_Index" or
		index=="List_of_S%26P_500_companies" or
		index=="NASDAQ-100" or
		index== "Russell_1000_Index"):
		region="US"
	elif (index=="CAC_40" or
		index=="DAX" or
		index=="FTSE_100_Index"):
		region="EU"
	else:
		region="EU"
	print("Region of " +Ticker+ " is "+region)
	return region

def costofdebt(Interest_Coverage_Ratio, market_cap , Ticker, maturity):
	#costofdebtdebt should be tax deductable commitment: account payable, under funded pension or health plan, lease...
	#We could use credit rating but this information is hard to find in a structured way (Yahoo finance, Google Finance, Bloomberg...) therefore we use synthetic rating: Interest Coverage ratio=EBIT/Interest Expenses
	#Right now we just ignore leasing and pension/health plan
	riskfreerate= import_data.riskfreerate(get_exchange(Ticker), maturity)
	spread= synthetic_rating(Interest_Coverage_Ratio, market_cap)
	costofdebt =  riskfreerate + spread
	print("\ncost of debt:"+ str(costofdebt))
	return costofdebt

def	synthetic_rating(Interest_Coverage_Ratio, market_cap):
		#http://pages.stern.nyu.edu/~adamodar/New_Home_Page/valquestions/syntrating.htm Thank you Aswath Damodaran
		#Interest_Coverage_Ratio=EBIT/Interest expense
	if market_cap<10**9: #if the market cap is smaller than 1b
		if Interest_Coverage_Ratio > 12.5:
			spread=0.75/100
		elif Interest_Coverage_Ratio > 9.5:
			spread=1/100
		elif Interest_Coverage_Ratio > 7.5:
			spread=1.5/100
		elif Interest_Coverage_Ratio > 6:
			spread=1.8/100
		elif Interest_Coverage_Ratio > 4.5:
			spread=2/100
		elif Interest_Coverage_Ratio > 3.5:
			spread=2.25/100
		elif Interest_Coverage_Ratio > 3:
			spread=3.5/100
		elif Interest_Coverage_Ratio > 2.5:
			spread=4.75/100
		elif Interest_Coverage_Ratio > 2:
			spread=6.5/100
		elif Interest_Coverage_Ratio > 1.5:
			spread=8/100
		elif Interest_Coverage_Ratio > 1.25:
			spread=10/100
		elif Interest_Coverage_Ratio > 0.8:
			spread=11.5/100
		elif Interest_Coverage_Ratio > 0.5:
			spread=12.7/100
		else:
			spread=14/100
	else:
		if Interest_Coverage_Ratio > 8.5:
			spread=0.75/100
		elif Interest_Coverage_Ratio > 6.5:
			spread=1/100
		elif Interest_Coverage_Ratio > 5.5:
			spread=1.5/100
		elif Interest_Coverage_Ratio > 4.25:
			spread=1.8/100
		elif Interest_Coverage_Ratio > 3:
			spread=2/100
		elif Interest_Coverage_Ratio > 2.5:
			spread=2.25/100
		elif Interest_Coverage_Ratio > 2:
			spread=3.5/100
		elif Interest_Coverage_Ratio > 1.75:
			spread=4.75/100
		elif Interest_Coverage_Ratio > 1.5:
			spread=6.5/100
		elif Interest_Coverage_Ratio > 1.25:
			spread=8/100
		elif Interest_Coverage_Ratio > 0.8:
			spread=10/100
		elif Interest_Coverage_Ratio > 0.65:
			spread=11.5/100
		elif Interest_Coverage_Ratio > 0.2:
			spread=12.7/100
		else:
			spread=14/100

	print("\nspread : "+ str(spread))
	return spread
def beta(index,stock):																										#index:x,stock:y, sample:'d','w','m','q'daily, weekly, monthly, quarterly
	#beta mesures the risk of the stock vs the market. The higher is beta, the riskier.
	#To calculate beta, we use a regression analysis	
	df_index=index.historical_data['Adj Close']
	df_stock=stock.historical_data['Adj Close']	

	df_index=df_index.interpolate()																							#if for some reason we don't have a value for a specific day, we want to interpolate it
	df_stock=df_stock.interpolate()	

	samples=['D','W','2W','M','Q']																							#we loop different samples to get the best model
	p_value=10**10
	for sample in samples:

		df_stock=df_stock.resample(sample).mean()																			#we resample the data
		df_index=df_index.resample(sample).mean()
		np_stock=df_stock.pct_change().dropna().to_numpy()																	#we compute also % of change to get return
		np_index=df_index.pct_change().dropna().to_numpy()	
		min_days=-min(len(np_index),len(np_stock))
		np_index=np_index[min_days:]																						#get the last days
		np_stock=np_stock[min_days:]																						#get the last days, this is more realistic because it can be that the stock was not traded for a day.
		plt.figure(figsize=(20,20))
		plt.scatter(np_index,np_stock, alpha=.5)
		np_index=sm.add_constant(np_index, has_constant='add')
		model = sm.OLS(np_stock,np_index).fit()
		print(model.summary())

		np_index=np_index[:,1]																								#remove the constant

		print(model.f_pvalue)
		if p_value > model.f_pvalue:																						#the lower the p-value, the better
			p_value=model.f_pvalue
			#print(model.params)
			alpha=model.params[0]
			beta=model.params[1]
			print("p_value : "+ str(p_value))

			print("alpha ="+ str(alpha) +" beta= "+str(beta))
			x_model=np.linspace(np_index.min(),np_index.max(),2)
			y_model=x_model*beta+alpha

			'''plt.xlabel("index return: "+ index.ticker)
			plt.ylabel("stock return: "+ stock.ticker)
			plt.title("Raw data and beta\np_value ="+ str(p_value) + "\nSampling : " + sample)
			plt.plot(x_model,y_model, alpha=0.5)
			plt.show(block=False)																							#Show raw data and model
			plt.pause(1)
			plt.close()'''
			s=sample
	if p_value < 0.01:																										#if p_value lower than 1%, the hypothesis is confirmed. Otherwise we use Yahoo's data as fallback
		print("p_value : "+ str(p_value) +"\n We accept this model. \n Sample:" +s)
	else:
		print("p_value : "+ str(p_value) +"\n The model is not good enough, we use Yahoo data as fallback. Check if we used the right index data")
		beta=stock.key_statistics.loc['Beta (5Y Monthly)'].values[0]
		stock.beta_is_fallback=True
	stock.beta=beta
	print ("\nbeta=" + str(beta))
	return beta

def market_return(index_data):
	#We can assume that the annual historical mean return of index is a good proxy for the expected market return. 
	#Here, we calculate it as the arithmetic mean of monthly returns (again, based on the 5-year monthly data) and multiply it by 12
	#we could also calculate this at the sum of dividend and buyback discounted for every stock in the marker
	#we can compare the data with: https://www.macrotrends.net/2595/dax-30-index-germany-historical-chart-data
	#some poeple calculate market return as last day - first day/first day. However, if the first day and the last day is good or bad, in orther world, if the market is volitil, this is not really robust.
	#Therefore we take the mean of the market price over the year. This gives us the same return as if we invest everyday in the market (a.k.a. Dollar-Cost Averaging)
	df_index=index_data['Adj Close'].interpolate()
	df_index=df_index.resample('Y').mean()									
	market_return=df_index.pct_change().dropna()
	print(market_return)
	market_return=market_return.mean()	
	print("Market return :" + str(market_return))
	return market_return

def costofequity(exchange, index, stock):																					#this can be calculated as the sum of dividend and buyback discounted
	#E(R)=Rf+ β × [MR−Rf]
	maturity=10																												#we assume a maturity of 10 years, 5 years would give us a very low risk free rate
	rf=import_data.riskfreerate(exchange, maturity)
	β=beta(index,stock)
	MR=market_return(index.historical_data)
	print(rf)
	print(β)
	print(MR)
	costofequity=rf+β*(MR-rf)
	print("\nCost of equity =" + str(costofequity))
	return costofequity

def taxrate(financial_statement):																				
	#using only value might be not accurate, therefore we can use a weithed average of last 4 year with higher weight for recent years
	quarter=int(datetime.datetime.today().month/3)							#at the begining of the year, data for last year are the same as ttm data, therefore the weight for ttm depends on the quarter
	taxrate=(financial_statement.loc['Interest Expense'].iat[0]*quarter
		+financial_statement.loc['Interest Expense'].iat[1]*4
		+financial_statement.loc['Interest Expense'].iat[2]*3
		+financial_statement.loc['Interest Expense'].iat[3]*2)/(financial_statement.loc['Income Before Tax'].iat[0]*quarter
		+financial_statement.loc['Income Before Tax'].iat[1]*4
		+financial_statement.loc['Income Before Tax'].iat[2]*3
		+financial_statement.loc['Income Before Tax'].iat[3]*2)
	print("\nTax rate :" + str(taxrate))
	return taxrate


def debt_market_value(costofdebt,financial_statement, balance_sheet):
	#The simplest way to estimate the market value of debt is to convert the book value of debt in market value of debt 
	#by assuming the total debt as a single coupon bond with a coupon equal to the value of interest expenses on the 
	#total debt and the maturity equal to the weighted average maturity of the debt. 
	#https://www.myaccountingcourse.com/accounting-dictionary/market-value-of-debt
	#this is a first approach, we assume the debt has only 1 maturity and we ignore long term and short term debt
	rate=financial_statement.loc['Interest Expense'].iat[0]/balance_sheet.loc['Total Liabilities'].iat[0]
	print(rate)
	nper=10												#this is an assumption because we don't know debt maturity, we assume 10 years of maturity
	pmt=-financial_statement.loc['Interest Expense'].iat[0]
	fv=balance_sheet.loc['Total Liabilities'].iat[0]
	debt_market_value=-np.pv(costofdebt, nper, -pmt, fv)
	print("Debt market value: " + str(debt_market_value))
	return debt_market_value

def equity_market_value(summary):
	#this is equal to #share outstanding * share price but we can just take market cap
	equity_market_value=summary.loc['Market Cap'].iat[0]
	return equity_market_value

def	costofcapital(exchange, index, stock):
	#Weighted average cost of capital at market value (NOT book value because we are interested of the price as of today)
	#Debt
	ICO=stock.financial_statement.loc['Income Before Tax'].iat[0]/stock.financial_statement.loc['Interest Expense'].iat[0] 	#we compute interest coverage ration
	Kd=costofdebt(ICO,stock.summary.loc['Market Cap'].iat[0], stock.ticker, 10)												#Interest_Coverage_Ratio, market_cap , Ticker, maturity
	#Equity
	Ke=costofequity(exchange, index, stock)										#exchange, index_data, stock_data, sample :'D', 'W', 'M'
	E=equity_market_value(stock.summary)
	D=debt_market_value(Kd,stock.financial_statement*1000, stock.balance_sheet*1000)										#*1000 because all numbers are in 1000
	print("Equity value :" +str(E))
	print("Debt value :" +str(D))
	V=E+D
	print("Debt ratio :" +str(D/V))
	taxr=taxrate(stock.financial_statement)
	stock.taxrate=taxr
	WACC=E/V*Ke+D/V*Kd*(1-taxr)
	stock.cost_of_capital=WACC
	stock.cost_of_debt=Kd
	stock.cost_of_equity=Ke
	print("Weighted average cost of capital: " + str(WACC))
	stock.leverage=D/(E+D)
	return WACC	
def revenue_model(year, a, b, c):
	#to forecast revenue, we use a log model because a straightline model would be foolish and would assume that growth doesn't decrease when the company become bigger
	return a * np.log(b * year) + c 
def gross_margin_model(revenue,a,b,c):
	#to forecast COGS, we assume that gross margin decrease when sales increase because of economy of scale 
	return a * np.exp(-b * revenue) + c	

def free_cash_flow(stock, WACC):
	#http://www.streetofwalls.com/finance-training-courses/investment-banking-technical-training/discounted-cash-flow-analysis/
	#https://corporatefinanceinstitute.com/resources/knowledge/valuation/dcf-formula-guide/
	#https://www.wallstreetprep.com/knowledge/income-statement-forecasting/#Depreciation_and_amortization
	number_of_years=15
	columns=["year "+ str(i) for i in range(number_of_years)]																#create header for forecast
	#columns=['year 1', 'year 2', 'year 3', 'year 4', 'year 5', 'year 6', 'year 7', 'year 8', 'year 9', 'year 10', 'year 11', 'year 12', 'year 12', 'year 14', 'year 15']
	index=['Total Revenue']
	dfforecast=pd.DataFrame(index=index, columns=columns)	#create forecast line by line, we first forecast revenue, then operation margin...to calculate free cashflow

	#1)forecast revenue
	revenue=stock.financial_statement.loc['Total Revenue'][-4:].values#.to_numpy()											#we want to use the last 4 years to build a model and use ttm value as a start value for y0
	revenue=np.flip(revenue)
	revenue=revenue.tolist()
	year = [1,2,3,4]#np.linspace(0, 4, 50)		
	popt, pcov = curve_fit(revenue_model, year, revenue)																	#reverse the order of the years
	print(popt)
	year_forecast=[i for i in range(5,5+number_of_years)]																	#create years for forecast
	#year_forecast=[5,6,7,8,9,10,11,12,13,14,15,16,17,18,19]
	revenue_forecast=list()
	for i in year_forecast:																									#we forecast the revenue with our model, using ttm as start value.
		revenue_forecast.append(revenue_model(i,popt[0],popt[1],popt[2])+stock.financial_statement.loc['Total Revenue'].iat[0]-stock.financial_statement.loc['Total Revenue'].iat[1])
	
	#plt.plot(year,revenue)
	#plt.plot(year_forecast,revenue_forecast)
	#plt.show()
	'''This is for polynomial model
	poly = PolynomialFeatures(degree=1)
	X=[[0],[1],[2],[3]]
	X_=poly.fit_transform(X)
	reg = linear_model.LinearRegression().fit(X_,revenue)
	xpred=poly.fit_transform([[4],[5],[6],[7]])
	#reg.score(revenue,[0,1,2,3])
	print("coef=" + str(reg.coef_))
	print("intercept :" +str (reg.intercept_))
	print(reg.predict(xpred))
	'''
	dfforecast.loc['Total Revenue']=revenue_forecast
	print(dfforecast)
	#2)COGS (should decrease if Revenue increase: correl revenue and COGS)-->Economy of scale
	try:
		gross_margin=stock.financial_statement.loc['Cost of Revenue'][-4:].values/stock.financial_statement.loc['Total Revenue'][-4:].sort_values#we use last 4 years to build a model
		gross_margin=np.flip(gross_margin)																					#reverse the order of the years
		gross_margin=gross_margin.tolist()		
		popt, pcov = curve_fit(gross_margin_model, revenue, gross_margin)
		COGS_forecast=list()
		for rev in revenue_forecast:
			COGS_forecast.append(gross_margin_model(rev,popt[0],popt[1],popt[2])*rev)										#we forecast cost based on forecasted revenue
		dfforecast.loc['- Cost of Revenue']=COGS_forecast
	except:
		print("\nno Cost of Revenue found")
		dfforecast.loc['- Cost of Revenue']=0

	#compute Gross profit
	dfforecast.loc['= Gross Profit']=dfforecast.loc['Total Revenue']-dfforecast.loc['- Cost of Revenue']
	
	#3)R&D + SG&A for tech companies Research Development might drive Revenue and growth but we first ignore thisand estimate constant
	try:
		RnD=(stock.financial_statement.loc['Research Development']/stock.financial_statement.loc['Total Revenue']).mean(axis=0)
	except:
		RnD=0
	try:
		SGnA=(stock.financial_statement.loc['Selling General and Administrative']/stock.financial_statement.loc['Total Revenue']).mean(axis=0)
	except:
		SGnA=0
	if RnD + SGnA==0:																										#This means that we don't have the breakdown for SGnA and RnD
		try:
			TOE=(stock.financial_statement.loc['Total Operating Expenses']/stock.financial_statement.loc['Total Revenue']).mean(axis=0)
		except:
			print("Could not find Total Operating Expenses")
			TOE=0
		dfforecast.loc['= Total Operating Expenses']=dfforecast.loc['Total Revenue']*TOE
	else:
		dfforecast.loc['- Research Development']=dfforecast.loc['Total Revenue']*RnD
		dfforecast.loc['- Selling General and Administrative']=dfforecast.loc['Total Revenue']*SGnA
		dfforecast.loc['= Total Operating Expenses']=dfforecast.loc['- Selling General and Administrative']+dfforecast.loc['- Research Development']
	#4)EBITDA
	dfforecast.loc['= EBITDA']=dfforecast.loc['= Gross Profit']-dfforecast.loc['= Total Operating Expenses']

	 

	#5)-D&A
	#There are more sophisticated way to forecast balance sheet and estimate D&A but for now let's assume D&A is proportional to salesand capex remains the same
	#to estimate D&A we should recreate balance sheet with days sales outstanding, inventory turnover ratio, number of days payables
	#https://www.wallstreetprep.com/knowledge/guide-balance-sheet-projections/
	try:
		DnA=(stock.cash_flow_statement.loc['Depreciation & amortization']/stock.financial_statement.loc['Total Revenue']).mean(axis=0)
	except:
		DnA=0
	dfforecast.loc['- Depreciation & amortization']=DnA*dfforecast.loc['Total Revenue']

	#Tax effected Ebit
	dfforecast.loc['= EBIT']=dfforecast.loc['= EBITDA']-dfforecast.loc['- Depreciation & amortization']	
	
	#6)tax
	taxr=taxrate(stock.financial_statement)
	dfforecast.loc['- Tax']=dfforecast.loc['= EBIT']*taxr
	dfforecast.loc['= Tax effected Ebit']=dfforecast.loc['= EBIT']-dfforecast.loc['- Tax']

	#7)+D&A+netCAPEX (non-cash expenses)
	#https://www.wallstreetoasis.com/forums/best-way-to-forecast-da-and-capex
	dfforecast.loc['+ Depreciation & amortization']=DnA*dfforecast.loc['Total Revenue']
	try:
		capex=stock.cash_flow_statement.loc['Capital Expenditure'].mean(axis=0)
	except:
		capex=0
		print("Capital Expenditure not found")
	dfforecast.loc['+ CAPEX']=capex

	#8)netWorkingCapital
	nWC=(stock.cash_flow_statement.loc['Change in working capital']/stock.financial_statement.loc['Total Revenue']).mean(axis=0)
	dfforecast.loc['+ netWorkingCapital']=nWC*dfforecast.loc['Total Revenue']

	
	#9)DCF
	dfforecast.loc['= Free Cash Flow'] = dfforecast.loc['= Tax effected Ebit'] + dfforecast.loc['+ Depreciation & amortization'] + dfforecast.loc['+ CAPEX'] + dfforecast.loc['+ netWorkingCapital']
	print(dfforecast)
	#10)Terminal value
	growth=dfforecast.loc['= Free Cash Flow'].pct_change().min()*1/2
	#Gordon Formula: Terminal Value = FCFn × (1 + g) ÷ (r – g)
	#we could either use Gordon Formula or increase the number of years to calculate cashflow. It seems that the result of Gordon Terminal value highly depend on the expected growth and WACC. 
	#Therefore we use 15 years discounted cashflow which is average lifespan of S&P500 companies
	#https://www.bbc.com/news/business-16611040
	#print(WACC)
	#print (growth)
	TV=dfforecast.loc['= Free Cash Flow'].iat[-1] * (1 + growth) / (WACC- growth)
	#print(TV)
	cashflow=dfforecast.loc['= Free Cash Flow'].tolist()#.append(TV)
	#print(cashflow)
	#cashflow.append(TV)
	#print(cashflow)
	EV=np.npv(WACC,cashflow)/(1+WACC)
	print("\n Entreprise value:"+ str(EV))
	stock.entreprise_value=EV
	return EV

def main():
	
	#index=import_data.market_index("^FCHI")
	#stock=import_data.company_data("BNP.PA")
	#WACC=costofcapital(get_exchange(index.ticker), index, stock)
	#EV=free_cash_flow(stock,WACC)*1000
	#share_value=EV/stock.shares_outstanding
	#beta(index,stock)
	#print(market_return(DAX.historical_data))
	#costofequity("EU",5,DAX.historical_data,SAP.historical_data,'M')
	#taxrate(SAP.financial_statement)
	
	pd.set_option('precision', 2)																								#format float dataframe with 2 significant digits
	
	import_data.list_market_index()																								#initializes index data

	df_result=pd.DataFrame(index=[],columns=[
		'Sector', 'Industry', 'Cost of Debt',
		'Cost of Equity','Cost of Capital', 'beta', 
		'Beta is fallback', 'taxrate', 'Entreprise Value', 
		'Share Value', 'Share Price', 'Potential Gain/Loss'
		])
	index=import_data.market_index("^DJI")																						#Dow Jones

	
	for row in import_data.NYSE_Arca_Major_Market_Index.iterrows():
		try:
			stock=import_data.company_data(row[1][1])
			WACC=costofcapital(get_exchange(index.ticker), index, stock)
			EV=free_cash_flow(stock,WACC)*1000
			share_value=EV/stock.shares_outstanding
			stock.potential_gain_loss=(share_value-stock.price)/stock.price
			df_result.loc[stock.ticker]=[
				stock.profile[0], stock.profile[1], stock.cost_of_debt, 
				stock.cost_of_equity, stock.cost_of_capital, stock.beta, 
				stock.beta_is_fallback, stock.taxrate, stock.entreprise_value, 
				share_value, stock.price, stock.potential_gain_loss
				]
		except:
			print("Impossible to value " + row[1][1])
	
	'''
	index=import_data.market_index("^GSPC")																						#S&P500
	for row in import_data.List_of_SP_500_companies.iterrows():
		try: 
			stock=import_data.company_data(row[1][1])
			WACC=costofcapital(get_exchange(index.ticker), index, stock)
			EV=free_cash_flow(stock,WACC)*1000
			share_value=EV/stock.shares_outstanding
			stock.potential_gain_loss=(share_value-stock.price)/stock.price
			df_result.loc[stock.ticker]=[
			stock.profile[0], stock.profile[1], stock.cost_of_debt,
			stock.cost_of_equity, stock.cost_of_capital, stock.beta,
			stock.beta_is_fallback, stock.taxrate, stock.entreprise_value,
			share_value, stock.price, stock.potential_gain_loss
			]
		except:
			print("Impossible to value " + row[1][1])
	print(df_result.sort_values(by=['Sector', 'Industry']))
	
	index=import_data.market_index("^IXIC")																						#NASDAQ Composite
	for row in import_data.NASDAQ_100.iterrows():
		try:
			stock=import_data.company_data(row[1][1])
			WACC=costofcapital(get_exchange(index.ticker), index, stock)
			EV=free_cash_flow(stock,WACC)*1000
			share_value=EV/stock.shares_outstanding
			stock.potential_gain_loss=(share_value-stock.price)/stock.price
			df_result.loc[stock.ticker]=[
			stock.profile[0], stock.profile[1], stock.cost_of_debt, 
			stock.cost_of_equity, stock.cost_of_capital, stock.beta, 
			stock.beta_is_fallback, stock.taxrate, stock.entreprise_value, 
			share_value, stock.price, stock.potential_gain_loss
			]
		except:
			print("Impossible to value " + row[1][1])
	print(df_result.sort_values(by=['Sector', 'Industry']))


	index=import_data.market_index("^FCHI")																						#CAC40
	for row in import_data.CAC_40.iterrows():
		try:
			stock=import_data.company_data(row[1][1])
			WACC=costofcapital(get_exchange(index.ticker), index, stock)
			EV=free_cash_flow(stock,WACC)*1000
			share_value=EV/stock.shares_outstanding
			stock.potential_gain_loss=(share_value-stock.price)/stock.price
			df_result.loc[stock.ticker]=[
			stock.profile[0], stock.profile[1], stock.cost_of_debt, 
			stock.cost_of_equity, stock.cost_of_capital, stock.beta,
			stock.beta_is_fallback, stock.taxrate, stock.entreprise_value, 
			share_value, stock.price, stock.potential_gain_loss
			]
		except:
			print("Impossible to value " + row[1][1])
	print(df_result.sort_values(by=['Sector', 'Industry']))
	
	index=import_data.market_index("^GDAXI")																					#DAX
	for row in import_data.DAX.iterrows():
		try:
			stock=import_data.company_data(row[1][1])
			WACC=costofcapital(get_exchange(index.ticker), index, stock)
			EV=free_cash_flow(stock,WACC)*1000
			share_value=EV/stock.shares_outstanding
			stock.potential_gain_loss=(share_value-stock.price)/stock.price
			df_result.loc[stock.ticker]=[
			stock.profile[0], stock.profile[1], stock.cost_of_debt, 
			stock.cost_of_equity, stock.cost_of_capital, stock.beta, 
			stock.beta_is_fallback,stock.taxrate, stock.entreprise_value, 
			share_value, stock.price, stock.potential_gain_loss
			]
		except:
			print("Impossible to value " + row[1][1])
	print(df_result.sort_values(by=['Sector', 'Industry']))
	

	index=import_data.market_index("UKXNUK.L")																					#FTSE
	for row in import_data.FTSE_100_Index.iterrows():
		try:
			stock=import_data.company_data(row[1][1])
			WACC=costofcapital(get_exchange(index.ticker), index, stock)
			EV=free_cash_flow(stock,WACC)*1000
			share_value=EV/stock.shares_outstanding
			stock.potential_gain_loss=(share_value-stock.price)/stock.price
			df_result.loc[stock.ticker]=[
			stock.profile[0], stock.profile[1], stock.cost_of_debt, 
			stock.cost_of_equity, stock.cost_of_capital, stock.beta, 
			stock.beta_is_fallback, stock.taxrate, stock.entreprise_value, 
			share_value, stock.price, stock.potential_gain_loss
			]
		except:
			print("Impossible to value " + row[1][1])
	print(df_result.sort_values(by=['Sector', 'Industry']))
	
	index=import_data.market_index("^RUT")																						#Russell_1000_Index
	for row in import_data.Russell_1000_Index.iterrows():
		try:
			stock=import_data.company_data(row[1][1])
			WACC=costofcapital(get_exchange(index.ticker), index, stock)
			EV=free_cash_flow(stock,WACC)*1000
			share_value=EV/stock.shares_outstanding
			stock.potential_gain_loss=(share_value-stock.price)/stock.price
			df_result.loc[stock.ticker]=[
			stock.profile[0], stock.profile[1], stock.cost_of_debt, 
			stock.cost_of_equity, stock.cost_of_capital, stock.beta, 
			stock.beta_is_fallback, stock.taxrate, stock.entreprise_value, 
			share_value, stock.price, stock.potential_gain_loss
			]
		except:
			print("Impossible to value " + row[1][1])
	print(df_result.sort_values(by=['Sector', 'Industry']))
	'''
	print("\nResult for NYSE:")
	print(import_data.NYSE_Arca_Major_Market_Index.set_index('Ticker').join(df_result, how='left').sort_values(by=['Sector', 'Industry']))
'''
	print("\nResult for S&P500:")
	print(import_data.List_of_SP_500_companies.set_index('Ticker').join(df_result, how='left').sort_values(by=['Sector', 'Industry']))	
	
	print("\nResult for NASDAQ Composite:")
	print(import_data.NASDAQ_100.set_index('Ticker').join(df_result, how='left').sort_values(by=['Sector', 'Industry']))

	print("\nResult for CAC40:")
	print(import_data.CAC_40.set_index('Ticker').join(df_result, how='left').sort_values(by=['Sector', 'Industry']))

	print("\nResult for DAX:")
	print(import_data.DAX.set_index('Ticker').join(df_result, how='left').sort_values(by=['Sector', 'Industry']))

	print("\nResult for FTSE:")
	print(import_data.FTSE_100_Index.set_index('Ticker').join(df_result, how='left').sort_values(by=['Sector', 'Industry']))

	print("\nResult for Russell 1000 Index:")
	print(import_data.Russell_1000_Index.set_index('Ticker').join(df_result, how='left').sort_values(by=['Sector', 'Industry']))
'''
if __name__ == "__main__":
	main()
