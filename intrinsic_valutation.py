#valuation of the business based on own performance and expected cashflow as opposed to multiple valuation
import import_data
import pandas as pd
import numpy as np
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
def beta(index_data,stock_data,sample):									#index:x,stock:y, sample:'d','w','m','q'daily, weekly, monthly, quarterly
	#beta mesures the risk of the stock vs the market. The higher is beta, the riskier.
	#To calculate beta, we use a regression analysis	
	
	df_index=index_data['Adj Close'].interpolate()						#if for some reason we don't have a value for a specific day, we want to interpolate it
	df_stock=stock_data['Adj Close'].interpolate()	
	#df_stock.index= pd.to_datetime(df_stock.index)
	#df_index.index=pd.to_datetime(df_index.index)
	#print(df_stock)
	#print(df_index)
	df_stock=df_stock.resample(sample).mean()							#we resample the data
	df_index=df_index.resample(sample).mean()
	np_stock=df_stock.pct_change().dropna().to_numpy()					#we compute also % of change to get return
	np_index=df_index.pct_change().dropna().to_numpy()	
	min_days=-min(len(np_index),len(np_stock))
	np_index=np_index[min_days:]										#get the last days
	np_stock=np_stock[min_days:]										#get the last days, this is more realistic because it can be that the stock was not traded for a day.
	#print(np_index)
	#print(np_stock)
	plt.figure(figsize=(20,20))
	plt.scatter(np_index,np_stock, alpha=.5)
	np_index=sm.add_constant(np_index, has_constant='add')
	model = sm.OLS(np_stock,np_index).fit()
	print(model.summary())

	np_index=np_index[:,1]#remove the constant

	#print(np_stock)
	#print(np_index)
	alpha=model.params[0]
	beta=model.params[1]
	p_value=model.f_pvalue
	#print(model.params)
	print(p_value)
	print("alpha ="+ str(alpha) +" beta= "+str(beta))
	x_model=np.linspace(np_index.min(),np_index.max(),2)
	y_model=x_model*beta+alpha

	plt.xlabel("index return")
	plt.ylabel("stock return")
	plt.plot(x_model,y_model, alpha=0.5)
	plt.show()
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

def costofequity(exchange, index_data, stock_data, sample):		#this can be calculated as the sum of dividend and buyback discounted
	#E(R)=Rf+ β × [MR−Rf]
	maturity=10													#we assume a maturity of 10 years, 5 years would give us a very low risk free rate
	rf=import_data.riskfreerate(exchange, maturity)
	β=beta(index_data,stock_data,sample)
	MR=market_return(index_data)
	print(rf)
	print(β)
	print(MR)
	print(rf)
	costofequity=rf+β*(MR-rf)
	print("\nCost of equity =" + str(costofequity))
	return costofequity

def taxrate(financial_statement):
	taxrate=financial_statement.loc['Interest Expense'].iat[0]/financial_statement.loc['Income Before Tax'].iat[0]
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

def	costofcapital(exchange, market_index, stock):
	#Weighted average cost of capital at market value (NOT book value because we are interested of the price as of today)
	#Debt
	ICO=stock.financial_statement.loc['Income Before Tax'].iat[0]/stock.financial_statement.loc['Interest Expense'].iat[0] 	#we compute interest coverage ration
	Kd=costofdebt(ICO,stock.summary.loc['Market Cap'].iat[0], stock.ticker, 10)												#Interest_Coverage_Ratio, market_cap , Ticker, maturity
	#Equity
	Ke=costofequity(exchange, market_index.historical_data, stock.historical_data, 'W')										#exchange, index_data, stock_data, sample :'D', 'W', 'M'
	E=equity_market_value(stock.summary)
	D=debt_market_value(Kd,stock.financial_statement*1000, stock.balance_sheet*1000)										#*1000 because all numbers are in 1000
	print("Equity value :" +str(E))
	print("Debt value :" +str(D))
	V=E+D
	print("Debt ratio :" +str(D/V))
	taxr=taxrate(stock.financial_statement)
	WACC=E/V*Ke+D/V*Kd*(1-taxr)

	print("Weighted average cost of capital: " + str(WACC))
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
	columns=['year 0', 'year 1', 'year 2', 'year 3']
	index=['Total Revenue']
	dfforecast=pd.DataFrame(index=index, columns=columns)	#create forecast line by line, we first forecast revenue, then operation margin...to calculate free cashflow

	#1)forecast revenue
	revenue=stock.financial_statement.loc['Total Revenue'][-4:].values#.to_numpy()											#we want to use the last 4 years to build a model and use ttm value as a start value for y0
	revenue=np.flip(revenue)
	revenue=revenue.tolist()
	year = [1,2,3,4]#np.linspace(0, 4, 50)		
	popt, pcov = curve_fit(revenue_model, year, revenue)																	#reverse the order of the years
	print(popt)
	year_forecast=[5,6,7,8]
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
	gross_margin=stock.financial_statement.loc['Cost of Revenue'][-4:].values/stock.financial_statement.loc['Total Revenue'][-4:].values
	gross_margin=np.flip(gross_margin)																										#reverse the order of the years
	gross_margin=gross_margin.tolist()		
	popt, pcov = curve_fit(gross_margin_model, revenue, gross_margin)
	COGS_forecast=list()
	for rev in revenue_forecast:
		COGS_forecast.append(gross_margin_model(rev,popt[0],popt[1],popt[2])*rev)												#we forecast cost based on forecasted revenue
	dfforecast.loc['- Cost of Revenue']=COGS_forecast
	

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
	if RnD + SGnA==0:																											#This means that we don't have the breakdown for SGnA and RnD
		TOE=(stock.financial_statement.loc['Total Operating Expenses']/stock.financial_statement.loc['Total Revenue']).mean(axis=0)
		dfforecast.loc['= Total Operating Expenses']=dfforecast.loc['Total Revenue']*TOE
	else:
		dfforecast.loc['- Research Development']=dfforecast.loc['Total Revenue']*RnD
		dfforecast.loc['- Selling General and Administrative']=dfforecast.loc['Total Revenue']*SGnA
		dfforecast.loc['= Total Operating Expenses']=dfforecast.loc['- Selling General and Administrative']+dfforecast.loc['- Research Development']
	#4)EBITDA
	dfforecast.loc['= EBITDA']=dfforecast.loc['= Gross Profit']-dfforecast.loc['= Total Operating Expenses']

	 

	#5)-D&A
	#we can go more fancy and forecast balance sheet and estimate D&A but for now let's assume D&A is proportional to salesand capex remains the same
	#to estimate D&A we should recreate balance sheet with days sales outstanding, inventory turnover ratio, number of days payables
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
	dfforecast.loc['+ Depreciation & amortization']=DnA*dfforecast.loc['Total Revenue']
	capex=stock.cash_flow_statement.loc['Capital Expenditure'].mean(axis=0)
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
	print (WACC)
	print (growth)
	TV=dfforecast.loc['= Free Cash Flow'].iat[-1] * (1 + growth) / (WACC- growth)
	print(TV)
	cashflow=dfforecast.loc['= Free Cash Flow'].tolist()#.append(TV)
	print(cashflow)
	cashflow.append(TV)
	print(cashflow)
	EV=np.npv(WACC,cashflow)/(1+WACC)
	print(EV)
	return EV

def main():
	stock=import_data.company_data("TOT")
	index=import_data.market_index("^FCHI")

	#ICO=SAP.financial_statement.loc['Income Before Tax'].iat[0]/SAP.financial_statement.loc['Interest Expense'].iat[0]
	#syntetic_rating(ICO,Total.summary.loc['Market Cap'].iat[0])
	#costofdebt=costofdebt(ICO,SAP.summary.loc['Market Cap'].iat[0],"SAP",5)
	#print(DAX.historical_data)
	#print(SAP.historical_data)
	#cofd=costofdebt(ICO,SAP.summary.loc['Market Cap'].iat[0],"SAP",5)
	#beta(DAX.historical_data,SAP.historical_data,'M')
	#print(market_return(DAX.historical_data))
	#costofequity("EU",5,DAX.historical_data,SAP.historical_data,'M')
	#taxrate(SAP.financial_statement)
	WACC=costofcapital(get_exchange("TOT"), index, stock)
	

	EV=free_cash_flow(stock,WACC)*1000
	share_outstanding=stock.key_statistics.loc['Shares Outstanding 5'].values
	share_outstanding[0]=share_outstanding[0].replace("M","*1000000")	#Convert million
	share_outstanding[0]=share_outstanding[0].replace("B","*1000000000")	#Convert billion
	print(share_outstanding)
	share_price=EV/pd.eval(share_outstanding)
	print(share_price)
	print(stock.financial_statement)
	print(stock.cash_flow_statement)

if __name__ == "__main__":
	main()