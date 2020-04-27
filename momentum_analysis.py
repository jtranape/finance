#One of the problems that investors face is to know when is the right time to buy. To do so, one method is to use technical analysis to analyze the trend.
#For instance, we can use a short term and a long term moving average to estimate if this is the right time to buy.
#However, if both moving average intersect too often, the trading costs will increase and therefore decrease the yield.
#Technics: Moving average, Volume weighted average price (VWAP) and moving volume weighted average price (MVWAP)
#The MACD indicator formula is calculated by subtracting the 26-day Exponential Moving Average (EMA) from the 12-day EMA.(exponential moving average)
#Stochastic Indicator
#Dollar-Cost Averaging
#https://blog.quantinsti.com/moving-average-trading-strategies/

#further ideas: try volume ^2
#try to predict with LSTM or Fourier analysiss https://www.jakob-aungiers.com/articles/a/LSTM-Neural-Network-for-Time-Series-Prediction


import import_data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def buy_and_hold(stock, broker_fee):

	portfolio=1000
	print(stock.historical_data['Adj Close'][-1])
	print(stock.historical_data['Adj Close'][0])
	portfolio=portfolio*(1-broker_fee)
	portfolio=(
		stock.historical_data['Adj Close'][-1]
		- stock.historical_data['Adj Close'][0]
		)/stock.historical_data['Adj Close'][0]*portfolio + portfolio - stock.htorical_data['Adj Close'][-1]*broker_fee
	print(portfolio)

def dollar_cost_averagging(stock, broker_fee):
	portfolio=1000
	buying_price=[10]
	for i in range(0,10):
		index=int(len(stock.historical_data['Adj Close'])*i/10)
		buying_price.append(stock.historical_data['Adj Close'][index])

	total_fee=np.sum(broker_fee*np.array(buying_price))
	portfolio=np.sum((stock.historical_data['Adj Close'][-1]-buying_price)/buying_price*portfolio/10)-total_fee
	print(portfolio)
	print(total_fee)

def moving_average(stock, broker_fee):
	columns=[str(index_short) for index_short in range(3, 31, 3)]		
	index= [str(index_long) for index_long in range(6, 181, 6)]
	dfresult=pd.DataFrame(index=index, columns=columns)
	for index_short in range(3, 31, 3):																													#a most efficient way would be to use gradient descent
		for index_long in range(index_short, 181, 6):
			MAshort=stock.historical_data['Adj Close'].rolling(index_short).mean()																		#short-term Moving Average
			MAlong=stock.historical_data['Adj Close'].rolling(index_long).mean()																			#long-term Moving Average
			stock.historical_data['Adj Close'].plot()																							#plot raw data
			#MAshort.plot()																														#plot short-term Moving Average
			#MAlong.plot()																														#plot long-term Moving Average
			Dif=MAshort-MAlong																													#compute the difference between short-term and long term Moving Average
			#Dif.plot()
			#plt.show()																															#show raw data and moving averages
			serie=pd.merge(Dif.rename("Difference"), stock.historical_data['Adj Close'].rename("Raw data"), on='Date')#, keys=['Date'])			#we merge raw data and moving average
			#buy when short term moving average is higher than long term
			position=False																														#we initialize position, we assum that we have no position at the begining and start with 
			portfolio=1000																														#a portfolio of 1000 in cash
			total_fee=0																															#this is the total fee
			for row in serie.iterrows():																										#As time pass by, if the short term MA is above the long term, we buy. If not we sell.
				if position==False and row[1]['Difference']>0:
					#buy
					position=True
					buying_price=row[1]['Raw data']
					portfolio=portfolio-row[1]['Raw data']*broker_fee																			#The value of the portfolio decrease because of the broker fee
					total_fee=row[1]['Raw data']*broker_fee+total_fee																			#total broker fee
				if position==True and row[1]['Difference']<0:
					#sell
					position=False
					portfolio=(row[1]['Raw data']-buying_price)/buying_price*portfolio+portfolio-row[1]['Raw data']*broker_fee					#new portfolio : price change - broker fees
					total_fee=row[1]['Raw data']*broker_fee+total_fee																			#total broker fee
			dfresult.at[str(index_long),str(index_short)]=portfolio 																								#row/column
	print(dfresult)

def exponential_moving_average(stock, broker_fee):
	
	columns=[str(index_short) for index_short in range(3, 31, 3)]		
	index= [str(index_long) for index_long in range(6, 181, 6)]
	dfresult=pd.DataFrame(index=index, columns=columns)
	for index_short in range(3, 31, 3):																													#a most efficient way would be to use gradient descent
		for index_long in range(index_short, 181, 6):
			MAshort=stock.historical_data['Adj Close'].ewm(span=index_short, adjust=False).mean()																	#short-term Moving Average
			MAlong=stock.historical_data['Adj Close'].ewm(span=index_long, adjust=False).mean()																			#long-term Moving Average
			stock.historical_data['Adj Close'].plot()																							#plot raw data
			#MAshort.plot()																														#plot short-term Moving Average
			#MAlong.plot()																														#plot long-term Moving Average
			Dif=MAshort-MAlong																													#compute the difference between short-term and long term Moving Average
			#Dif.plot()
			#plt.show()																															#show raw data and moving averages
			serie=pd.merge(Dif.rename("Difference"), stock.historical_data['Adj Close'].rename("Raw data"), on='Date')#, keys=['Date'])			#we merge raw data and moving average
			#buy when short term moving average is higher than long term
			position=False																														#we initialize position, we assum that we have no position at the begining and start with 
			portfolio=1000																														#a portfolio of 1000 in cash
			total_fee=0																															#this is the total fee
			for row in serie.iterrows():																										#As time pass by, if the short term MA is above the long term, we buy. If not we sell.
				if position==False and row[1]['Difference']>0:
					#buy
					position=True
					buying_price=row[1]['Raw data']
					portfolio=portfolio-row[1]['Raw data']*broker_fee																			#The value of the portfolio decrease because of the broker fee
					total_fee=row[1]['Raw data']*broker_fee+total_fee																			#total broker fee
				if position==True and row[1]['Difference']<0:
					#sell
					position=False
					portfolio=(row[1]['Raw data']-buying_price)/buying_price*portfolio+portfolio-row[1]['Raw data']*broker_fee					#new portfolio : price change - broker fees
					total_fee=row[1]['Raw data']*broker_fee+total_fee																			#total broker fee
			dfresult.at[str(index_long),str(index_short)]=portfolio 																								#row/column
	print(dfresult)




def Volume_weighted_average(stock, broker_fee):
	columns=[str(index_short) for index_short in range(3, 31, 3)]		
	index= [str(index_long) for index_long in range(6, 181, 6)]
	df=stock.historical_data
	df['Volume Scaled Price']=df['Adj Close']*df['Volume']		
	dfresult=pd.DataFrame(index=index, columns=columns)
	for index_short in range(3, 31, 3):																													
		for index_long in range(6, 181, 6):
			df['vwap short']=df['Volume Scaled Price'].rolling(index_short).sum()/df['Volume'].rolling(index_short).sum()
			df['vwap long']=df['Volume Scaled Price'].rolling(index_long).sum()/df['Volume'].rolling(index_long).sum()
			df['vwap dif']=df['vwap short']-df['vwap long']
			position=False																														#we initialize position, we assum that we have no position at the begining and start with 
			portfolio=1000																														#a portfolio of 1000 in cash
			total_fee=0																															#this is the total fee
			for row in df.iterrows():																										#As time pass by, if the short term MA is above the long term, we buy. If not we sell.
				if position==False and row[1]['vwap dif']>0:
					#buy
					position=True
					buying_price=row[1]['Adj Close']
					portfolio=portfolio-row[1]['Adj Close']*broker_fee																			#The value of the portfolio decrease because of the broker fee
					total_fee=row[1]['Adj Close']*broker_fee+total_fee																			#total broker fee
				if position==True and row[1]['vwap dif']<0:
					#sell
					position=False
					portfolio=(row[1]['Adj Close']-buying_price)/buying_price*portfolio+portfolio-row[1]['Adj Close']*broker_fee					#new portfolio : price change - broker fees
					total_fee=row[1]['Adj Close']*broker_fee+total_fee																			#total broker fee
			dfresult.at[str(index_long),str(index_short)]=portfolio 																								#row/column
	print(dfresult)


def main():
	broker_fee=0.0025
	Volume_weighted_average(stock=import_data.company_data("PG"), broker_fee=broker_fee)	
	

if __name__ == "__main__":
	main()
