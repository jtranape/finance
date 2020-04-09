# finance

This algorithm download automatically companies data from main financial sources online (Yahoo Finance, investing.com, wikipedia...) 
and value the stocks using DCF intrinsic valuation.

The output should look like the result below for the main index:(NYSE Arca Major Market Index, SP 500 companies,
NASDAQ 100, CAC 40, DAX, FTSE 100 Index, Russell 1000 Index	...)

The third column from the right is the company valuation/number of share outstanding. If the valuation is correct,
the price should converge to this value.
The last column shows the expected return.

The outcome should not be used for investment decision but rather to identify companies that might be worth considering.
Before investing in a stock, investors should always thoroughly analyze financial reports and understand the business model
before making any investment decision.
Many companies use accounting tricks to mislead investors, therefore you should especially pay attention to the financial 
reports and especially the footnotes.

Result for NYSE:


|	Ticker	|	Company	|	Sector	|	Industry	|	Cost of Debt	|	Cost of Equity	|	Cost of Capital	|	beta	|	Beta is fallback	|	taxrate	|	Entreprise Value	|	Share Value	|	Share Price	|	Potential Gain/Loss	|
|	:-------------	|	:----------:	|	:----------:	|	:----------:	|	:----------:	|	:----------:	|	:----------:	|	:----------:	|	:----------:	|	:----------:	|	:----------:	|	:----------:	|	:----------:	|	-----------:	|
|	DD	|	E. I. du Pont de Nemours and Company	|	Basic Materials	|	Chemicals	|	0.15	|	0.09	|	1.14	|	1.14	|	FALSE	|	0.61	|	9.51E+07	|	128.78	|	37.55	|	2.43	|
|	DOW	|	The Dow Chemical Company	|	Basic Materials	|	Chemicals	|	0.14	|	0.07	|	1.2	|	1.2	|	FALSE	|	0.82	|	3.17E+07	|	42.63	|	32.76	|	0.3	|
|	DIS	|	The Walt Disney Company	|	Communication Services	|	Entertainment	|	0.02	|	0.06	|	0.92	|	0.92	|	FALSE	|	0.07	|	5.32E+08	|	293.7	|	104.86	|	1.8	|
|	MCD	|	McDonald's Corp.	|	Consumer Cyclical	|	Restaurants	|	0.02	|	0.05	|	0.81	|	0.81	|	FALSE	|	0.13	|	1.22E+08	|	161.37	|	184.53	|	-0.13	|
|	KO	|	The Coca-Cola Company	|	Consumer Defensive	|	Beverages—Non-Alcoholic	|	0.02	|	0.04	|	0.62	|	0.62	|	FALSE	|	0.1	|	1.76E+08	|	40.96	|	48.5	|	-0.16	|
|	WMT	|	Wal-Mart Stores Inc.	|	Consumer Defensive	|	Discount Stores	|	0.02	|	0.04	|	0.58	|	0.58	|	FALSE	|	0.15	|	-1.17E+08	|	-41.37	|	123.98	|	-1.33	|
|	PG	|	The Procter & Gamble Company	|	Consumer Defensive	|	Household & Personal Products	|	0.02	|	0.05	|	0.64	|	0.64	|	FALSE	|	0.05	|	4.87E+08	|	197.02	|	116.71	|	0.69	|
|	CVX	|	Chevron Corporation	|	Energy	|	Oil & Gas Integrated	|	0.02	|	0.07	|	1.18	|	1.18	|	FALSE	|	0.06	|	1.31E+09	|	695.13	|	84.26	|	7.25	|
|	XOM	|	Exxon Mobil Corporation	|	Energy	|	Oil & Gas Integrated	|	0.02	|	0.05	|	0.93	|	0.93	|	FALSE	|	0.03	|	2.67E+09	|	631.01	|	42.9	|	13.71	|
|	JPM	|	JPMorgan Chase & Co.	|	Financial Services	|	Banks—Diversified	|	0.07	|	0.05	|	1.2	|	1.2	|	FALSE	|	0.55	|	1.17E+08	|	38	|	94.45	|	-0.6	|
|	WFC	|	Wells Fargo & Company	|	Financial Services	|	Banks—Diversified	|	0.09	|	0.04	|	1.16	|	1.16	|	FALSE	|	0.6	|	7.49E+08	|	183.17	|	30.75	|	4.96	|
|	AXP	|	American Express Company	|	Financial Services	|	Credit Services	|	0.04	|	0.05	|	1.22	|	1.22	|	FALSE	|	0.37	|	2.20E+08	|	272.97	|	91.43	|	1.99	|
|	JNJ	|	Johnson & Johnson	|	Healthcare	|	Drug Manufacturers—General	|	0.02	|	0.05	|	0.68	|	0.68	|	FALSE	|	0.04	|	5.32E+08	|	201.53	|	139.86	|	0.44	|
|	MRK	|	Merck & Co. Inc.	|	Healthcare	|	Drug Manufacturers—General	|	0.02	|	0.05	|	0.71	|	0.71	|	FALSE	|	0.09	|	1.93E+08	|	75.64	|	81.68	|	-0.07	|
|	BA	|	The Boeing Company	|	Industrials	|	Aerospace & Defense	|	0.15	|	0.13	|	1.48	|	1.48	|	FALSE	|	0.13	|	3.96E+08	|	702.52	|	162	|	3.34	|
|	GE	|	General Electric Company	|	Industrials	|	Specialty Industrial Machinery	|	0.12	|	0.13	|	1.09	|	1.09	|	FALSE	|	-0.25	|	6.08E+08	|	69.86	|	7.69	|	8.08	|
|	MMM	|	3M Company	|	Industrials	|	Specialty Industrial Machinery	|	0.02	|	0.06	|	0.89	|	0.89	|	FALSE	|	0.06	|	2.17E+08	|	377.41	|	147.5	|	1.56	|
|	HPQ	|	Hewlett-Packard Company	|	Technology	|	Computer Hardware	|	0.02	|	0.05	|	1.12	|	1.12	|	FALSE	|	0.1	|	5.61E+08	|	392.43	|	15.7	|	24	|
|	IBM	|	International Business Machines Corporation	|	Technology	|	Information Technology Services	|	0.02	|	0.05	|	0.95	|	0.95	|	FALSE	|	0.09	|	4.88E+08	|	549.1	|	118.8	|	3.62	|
|	MSFT	|	Microsoft Corporation	|	Technology	|	Software—Infrastructure	|	0.02	|	0.09	|	1.12	|	1.12	|	FALSE	|	0.07	|	1.05E+09	|	138.02	|	169.59	|	-0.19	|




Description:
The algorithm calculates the cost of debt and of equity based on the financial data of the company. 
Given the leverage ratio, it calculates the cost of capital.
Using supervised machine-learning to forecast revenues and cost of good sold, we forecast the free-cash flow and discount them 
with the cost of capital.
The result is the enterprise value, if we divide it by the number of shares outstanding, we should estimate the share value.

Known limitation:
-cost of debt: Currently, we use a very simplistic approach and don't distinguish between long term and short term debt.
We also use synthetic rating because we don't have credit rating information (Moody, Fitch, S&P)
-Tax rate: some company have negative tax rate which doesn't make sense in the long run. 
-Forecast: we assume that depreciation and amortisation are proportional to sales and capex remains the same. 
This is of course wrong and would need more accurate forecast.
-Many assumptions are made (debt maturity, lifespan of the company...). It would be interesting to do a sensitivity analysis.
-Business model: we only model company buying and selling goods. This might be more appropriate for reseller or industrial companies.
However, we don't model business model including R&D, for instance tech companies. 
Therefore, the result of the valuation for this kind of company would be inaccurate.
-Commodity price: some companies, for instance in the oil and gas industry are more profitable when the price of the commodity is high, for instance oil. This is not included in the model.
