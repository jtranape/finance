# Principal	compenent analysis allows to understand to understand which feature explain most a model.
# We want to use PCA to understand which KPI are useful to assess the future return of a company
# https://www.datacamp.com/community/tutorials/principal-component-analysis-in-python
# https://www.geeksforgeeks.org/ml-principal-component-analysispca/?ref=lbp

import import_data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import datetime
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import StandardScaler 
from sklearn.preprocessing import LabelEncoder
from sklearn.decomposition import PCA 
from sklearn.linear_model import LinearRegression 
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor


#which variable could explain performance:
#https://macabacus.com/valuation/multiples
#https://www.kdnuggets.com/2017/02/yhat-support-vector-machine.html

#Equity Value multiples
#E#arning per share= (Net Income - Preferred Dividends)/shares outstanding

#Price multiples
#Price earning ratio
#PEG ratio
##Price/Sales
##Price/Book

#EV
#Entreprise Value(EV) = Market cap + Debt - Cash and cash equivalents
#Enterprise-Value-To-Revenue= EV/revenue 
##Enterprise Value/EBITDA
#EV / EBIT
#EV / Unlevered Free Cash Flow


#Business efficiency
##Profit margin
#Operating margin
##Return on Assets
##Return on Equity

#Revenue Per Share : most probabely not a good multiple but would be interesting to see if this match PCA output 
##Current Ratio =Current assets/current liabilities 

#Dividend:
#payout ratio = total dividend / Net income

#Debt/equity Ratio
#Tax rate


def multiples(stock):
		#Let's create a dataframe with double index: company and fiscal year
	#For this company, let's calculate the main multiple and the stock performance of next year.

	dftemp=stock.financial_statement
	dftemp=dftemp.drop('ttm', axis=1)
	
	# Financial Statement
	print(dftemp)
	dftemp=dftemp.loc[[
		'Total Revenue','Gross Profit','Net Income',
		'Operating Income or Loss', 
		'Net Income available to common shareholders',
		'Basic EPS','Diluted EPS',
		'Interest Expense','Income Before Tax',
		'Basic Average Shares','Diluted Average Shares',										#We need average shares to calculate market cap, EV 
		'EBITDA'
		]]

	# Balance sheet
	try:
		dftemp=dftemp.append(stock.cash_flow_statement.loc[[									#adding needed items from Cashflow statement
			'Dividends Paid'
			]].drop('ttm', axis=1))
	except:
		print("\'Dividends Paid\' not found in cash flow statement")
		dftemp.loc['Dividends Paid']=0

	# Cash flow Statement
	dftemp=dftemp.append(stock.cash_flow_statement.loc[[										#adding needed items from Cashflow statement
		'Free Cash Flow'
			]].tail(1).drop('ttm', axis=1))														#get only last raw with value
	dftemp=dftemp.append(stock.balance_sheet.loc[[												#adding needed items from Balance sheet
		'Cash And Cash Equivalents', 'Total Current Assets',
		'Total Assets',
		'Total Current Liabilities','Total Liabilities',
		'Total stockholders\' equity'															#Book value of equity
		]])

	# Cleanup 'Average Shares' for last fiscal year
	print(dftemp.loc['Basic Average Shares'][0])
	if dftemp.loc['Basic Average Shares'][0]=='NaN':
		dftemp.loc['Basic Average Shares'][0]=stock.shares_outstanding/1000						#divided by 1000 because in tausend
		dftemp.loc['Diluted Average Shares'][0]=stock.shares_outstanding/1000
		dftemp.loc['Basic EPS'][0]=dftemp.loc['Net Income available to common shareholders'][0]/stock.shares_outstanding*1000
		dftemp.loc['Diluted EPS'][0]=dftemp.loc['Net Income'][0]/stock.shares_outstanding*1000

	# Price
	prices=stock.historical_data['Adj Close'].resample('Y').mean()
	prices.index=prices.index.strftime("%m/%d/%Y")
	#print(prices)
	if dftemp.columns[0][0:2]!="12":																#If this doesn't work then most probably there is a mismatch with the date
		print("date mismatch")
		return
	else:
		dftemp.loc['Price']=prices[dftemp.columns]
	# Financials Ratio:
	# Price multiples
	# Price earnings ratio=Price / Earnings Per Share (EPS)
	dftemp.loc['Price earnings ratio']=dftemp.loc['Price']/dftemp.loc['Diluted EPS'].astype(float)
	# PEG ratio

	# Price/Sales= Marketcap/Sales
	dftemp.loc['Price-to-sales ratio']= dftemp.loc['Price']*dftemp.loc['Diluted Average Shares'].astype(float)/dftemp.loc['Total Revenue']

	# Price/BookMarketcap/Book value of equity
	dftemp.loc['Price-to-book ratio']= dftemp.loc['Price']*dftemp.loc['Diluted Average Shares'].astype(float)/dftemp.loc['Total stockholders\' equity']

	#EV
	#Entreprise Value(EV) = Market cap + Debt - Cash and cash equivalents
	#Enterprise-Value-To-Revenue= EV/revenue
	dftemp.loc['Enterprise-Value-To-Revenue'] = (
		dftemp.loc['Price']*dftemp.loc['Diluted Average Shares'].astype(float) 					#market cap
		+ dftemp.loc['Total Liabilities'] 														#debt
		- dftemp.loc['Cash And Cash Equivalents']												#Cash
		)/dftemp.loc['Total Revenue']

	#Enterprise Value/EBITDA
	dftemp.loc['Enterprise-Value-To-Ebitda'] = (
		dftemp.loc['Price']*dftemp.loc['Diluted Average Shares'].astype(float) 					#market cap
		+ dftemp.loc['Total Liabilities'] 														#debt
		- dftemp.loc['Cash And Cash Equivalents']												#Cash
		)/dftemp.loc['EBITDA']

	#EV / EBIT
	dftemp.loc['Enterprise-Value-To-Ebit'] = (
		dftemp.loc['Price']*dftemp.loc['Diluted Average Shares'].astype(float) 					#market cap
		+ dftemp.loc['Total Liabilities'] 														#debt
		- dftemp.loc['Cash And Cash Equivalents']												#Cash
		)/dftemp.loc['Net Income']																#EBIT

	#EV / Unlevered Free Cash Flow
	dftemp.loc['Enterprise-Value-To-Free-Cash-Flow'] = (
		dftemp.loc['Price']*dftemp.loc['Diluted Average Shares'].astype(float) 					#market cap
		+ dftemp.loc['Total Liabilities'] 														#debt
		- dftemp.loc['Cash And Cash Equivalents']												#Cash
		)/dftemp.loc['Free Cash Flow']


	# Business efficiency
	dftemp.loc['Gross profit margin']=dftemp.loc['Gross Profit']/dftemp.loc['Total Revenue']
	dftemp.loc['Operating profit margin']=dftemp.loc['Operating Income or Loss']/dftemp.loc['Total Revenue']
	dftemp.loc['Net profit margin']=dftemp.loc['Net Income']/dftemp.loc['Total Revenue']
	dftemp.loc['Return on Equity']=dftemp.loc['Net Income']/dftemp.loc['Total stockholders\' equity']
	dftemp.loc['Return on Assets']=dftemp.loc['Net Income']/dftemp.loc['Total Assets']
	 
	# Revenue Per Share
	dftemp.loc['Revenue Per Share']=dftemp.loc['Total Revenue']/dftemp.loc['Diluted Average Shares'].astype(float)
	

	#Current Ratio =Current assets/current liabilities
	dftemp.loc['Current Ratio']=dftemp.loc['Total Current Assets']/dftemp.loc['Total Current Liabilities']

	#Dividend:
	#payout ratio = total dividend / Net income
	dftemp.loc['Payout Ratio']=-dftemp.loc['Dividends Paid']/dftemp.loc['Net Income']

	# Tax rate
	dftemp.loc['Tax Rate']=dftemp.loc['Interest Expense']/dftemp.loc['Income Before Tax']
	
	# Leverage
	dftemp.loc['Leverage']=dftemp.loc['Total Liabilities']/(dftemp.loc['Total Liabilities']+stock.price*stock.shares_outstanding)

	# Stock Return =(ending price- initial price + dividend) / initial price
	dividend=-dftemp.loc['Dividends Paid']/dftemp.loc['Diluted Average Shares'].astype(float)
	#This is the return for the following year
	#avg_return=(prices.shift(-1)-prices-dividend)/prices 										#should try also with prices-prices.shift(1)
	avg_return=(
		stock.historical_data['Adj Close'].resample('Y').agg(['last'])['last']
		- stock.historical_data['Adj Close'].resample('Y').agg(['first'])['first']
		+ dividend
		)/stock.historical_data['Adj Close'].resample('Y').agg(['first'])['first']
	avg_return.index=avg_return.index.strftime("%m/%d/%Y")
	dftemp.loc['Stock Return (n+1)']=avg_return[dftemp.columns]
	
	#Cleanup
	#We only keep multiples:
	dftemp=dftemp.loc[[
			'Price earnings ratio', 'Price-to-sales ratio',
			'Price-to-book ratio', 'Enterprise-Value-To-Revenue',
			'Enterprise-Value-To-Ebitda', 'Enterprise-Value-To-Ebit',
			'Enterprise-Value-To-Free-Cash-Flow','Gross profit margin',
			'Net profit margin','Return on Equity', 'Return on Assets',
			'Revenue Per Share', 'Current Ratio', 'Payout Ratio', 
			'Tax Rate','Leverage',
			'Stock Return (n+1)'
		]]
	dftemp.index.name="multiples"		
	dftemp=dftemp.T 																			#Transpose so that we can append all stocks
	dftemp.insert(0,"Stock",stock.ticker)														#Add stock name as index
	dftemp.set_index("Stock", inplace=True, append = True)										
	print(dftemp)
	return dftemp

def main():
	import_data.list_market_index()
	import_data.company_data("KO")
	try:
		dfmulti_train=pd.read_pickle("./data/multi_train.pkl")													#calculating the multiples for 500 companies might take some time, we might want to save the output	
	except:	
		dfmulti_train=pd.DataFrame(index=[],columns=[
			'Price earnings ratio', 'Price-to-sales ratio',
			'Price-to-book ratio', 'Enterprise-Value-To-Revenue',
			'Enterprise-Value-To-Ebitda', 'Enterprise-Value-To-Ebit',
			'Enterprise-Value-To-Free-Cash-Flow','Gross profit margin',
			'Net profit margin','Return on Equity', 'Return on Assets',
			'Revenue Per Share', 'Current Ratio', 'Payout Ratio', 
			'Tax Rate','Leverage',
			'Stock Return (n+1)'
			])
		#KO=multiples(import_data.company_data("KO"))
		#dfmulti_train=dfmulti_train.append(KO)#,ignore_index=True)
		
		#print (dfmulti_train)
		
		for row in import_data.List_of_SP_500_companies.iterrows():
				try:
					stock=import_data.company_data(row[1][1])
					dfmulti_train=dfmulti_train.append(multiples(stock))
					print(dfmulti_train)

				except:
					print("Could not get multiples for "+ row[1][1])
		print(dfmulti_train)
		


		dfmulti_train.dropna(inplace=True)
		print(dfmulti_train)
		#X_train=dfmulti_train.iloc[:,0:14].astype(float) 	#.drop(columns='Stock Return (n+1)').values#tail(3).values
		#y=dfmulti_train.iloc[:,-1].astype(float) 	#['Stock Return (n+1)'].values.astype(float) 		
		
		dfmulti_train.to_pickle("./data/multi_train.pkl")
	print(dfmulti_train)
	dfmulti_train=dfmulti_train.drop(columns=['Price-to-sales ratio', 'Price-to-book ratio', 'Enterprise-Value-To-Revenue', 'Enterprise-Value-To-Ebitda', 'Current Ratio', 'Payout Ratio'])
	
	X_train=dfmulti_train.drop(columns='Stock Return (n+1)').values
	y_train=dfmulti_train['Stock Return (n+1)'].values
	print(X_train)
	print(y_train)

	# Test dataset:
	try:
		dfmulti_test=pd.read_pickle("./data/multi_test.pkl")													
	except:	
		dfmulti_test=pd.DataFrame(index=[],columns=[
			'Price earnings ratio', 'Price-to-sales ratio',
			'Price-to-book ratio', 'Enterprise-Value-To-Revenue',
			'Enterprise-Value-To-Ebitda', 'Enterprise-Value-To-Ebit',
			'Enterprise-Value-To-Free-Cash-Flow','Gross profit margin',
			'Net profit margin','Return on Equity', 'Return on Assets',
			'Revenue Per Share', 'Current Ratio', 'Payout Ratio', 
			'Tax Rate','Leverage',
			'Stock Return (n+1)'
			])
		#KO=multiples(import_data.company_data("KO"))
		#dfmulti_test=dfmulti_test.append(KO)#,ignore_index=True)
		
		#print (dfmulti_test)
		
		for row in import_data.FTSE_100_Index.iterrows():
				try:
					stock=import_data.company_data(row[1][1])
					dfmulti_test=dfmulti_test.append(multiples(stock))
					print(dfmulti_test)

				except:
					print("Could not get multiples for "+ row[1][1])
		print(dfmulti_test)
		


		dfmulti_test.dropna(inplace=True)
		print(dfmulti_test)
		#X_test=dfmulti_test.iloc[:,0:14].astype(float) 	#.drop(columns='Stock Return (n+1)').values#tail(3).values
		#y=dfmulti_test.iloc[:,-1].astype(float) 	#['Stock Return (n+1)'].values.astype(float) 		
		
		dfmulti_test.to_pickle("./data/multi_test.pkl")
	print(dfmulti_test)
	dfmulti_test=dfmulti_test.drop(columns=['Price-to-sales ratio', 'Price-to-book ratio', 'Enterprise-Value-To-Revenue', 'Enterprise-Value-To-Ebitda', 'Current Ratio', 'Payout Ratio'])
	
	X_test=dfmulti_test.drop(columns='Stock Return (n+1)').values.astype(float)
	y_test=dfmulti_test['Stock Return (n+1)'].values.astype(float)
	print(X_test)
	print(y_test)
	print(dfmulti_test.describe())
	# we need to normalize == 
	
	sc = StandardScaler() 
	  
	X_norm = sc.fit_transform(X_train) 
	#scaled_data should be now normalized
	#print(X_norm) 
	y_norm=sc.fit_transform(y_train.reshape(-1, 1))


	#PCA Analysis on training dataset
	pca = PCA(n_components = 2) #This would reduce to 2 components
	#pca = PCA(0.95) # we want the model to explain 95% of the variance 
  
	X_pca = pca.fit_transform(X_norm) 
	#X_train = pca.transform(X_test) 
	#plt.scatter(X_pca,y_train)
	print(X_pca.reshape(2,-1)[0].shape)
	print(X_pca.reshape(2,-1)[1].shape)
	print(y_train.shape)
	fig = plt.figure()
	#ax = fig.add_subplot(111, projection='3d')
	ax = Axes3D(fig)

	ax.scatter(X_pca.reshape(2,-1)[0].astype(float),X_pca.reshape(2,-1)[1].astype(float),y_train.astype(float))
	plt.show()



	pca = PCA(0.95) # we want the model to explain 95% of the variance 
	X_pca = pca.fit_transform(X_norm) 

	explained_variance = pca.explained_variance_ratio_ 
	print(explained_variance)
	print(X_pca)

	index= [str(index) for index in range(len(X_pca))]
	print(pca.components_)
	print(pd.DataFrame(pca.components_,columns=dfmulti_train.drop(columns='Stock Return (n+1)').columns))#,index = index))

	#linear regression
	model=LinearRegression()
	model.fit(X_train,y_train)
	print("Score for LinearRegression:" + str(model.score(X_test,y_test)))	


	#model = ExtraTreesClassifier()
	model=ExtraTreesRegressor()#min_samples_leaf=5)
	model.fit(X_train,y_train)

	print("Score for ExtraTreesRegressor:" + str(model.score(X_test,y_test)))	

	feat_importances = pd.Series(model.feature_importances_, index=dfmulti_train.drop(columns='Stock Return (n+1)').columns)
	print("Extra Tree feature importance \n: ")
	print(feat_importances.sort_values(ascending=False)) 

	#plot graph of feature importances for better visualization
	feat_importances.sort_values(ascending=False).nlargest(10).plot(kind='barh')
	plt.show()
	# We could split data into 2 random samples
	#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.8, random_state = 0) 
	#X_train=np.nan_to_num(X_train)
	

	#print(X_train)
	# performing preprocessing part 
	
	#X_test = sc.transform(X_test) 

	#classifier = LogisticRegression(random_state = 0) 
	#classifier.fit(X_pca, y_train) 

	# Random forest
	regr = RandomForestRegressor()
	regr.fit(X_train, y_train)

	print("Score for RandomForestRegressor:" + str(model.score(X_test, y_test)))
	feat_importances = pd.Series(model.feature_importances_, index=dfmulti_train.drop(columns='Stock Return (n+1)').columns)
	print("Random Forest feature importance \n: ")
	print(feat_importances.sort_values(ascending=False))
	feat_importances.sort_values(ascending=False).nlargest(10).plot(kind='barh')
	plt.show()

	# KNeighborsClassifier()
	


	model=KNeighborsRegressor()
	model.fit(X_train,y_train)
	print("Score for KNeighborsRegressor:" + str(model.score(X_test, y_test)))
	

	#https://scikit-learn.org/stable/auto_examples/cluster/plot_kmeans_digits.html#sphx-glr-auto-examples-cluster-plot-kmeans-digits-py
	#SVM
	model = SVR(C=1.0, epsilon=0.2)
	model.fit(X_train, y_train)
	print("Score for SVR:" + str(model.score(X_test, y_test)))
	
	#ANN

	model = MLPRegressor(hidden_layer_sizes=(30,),  activation='tanh', solver='adam', max_iter=500, verbose=True, alpha=10)

	model.fit(X_train, y_train)

	print("Score for Artificial Neuronal Network:" + str(model.score(X_test, y_test)))
	

	#Embedded

	#cross validation

if __name__ == "__main__":
	main()
