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
|	DD	|	E. I. du Pont de Nemours and Company	|	Basic Materials	|	Chemicals	|	0.15	|	4.01E-02	|	4.51E-02	|	0.89	|	FALSE	|	0.61	|	1.24E+08	|	168.23	|	37.55	|	3.48	|
|	DOW	|	The Dow Chemical Company	|	Basic Materials	|	Chemicals	|	0.14	|	1.05E-01	|	7.06E-02	|	1.29	|	FALSE	|	0.82	|	3.17E+07	|	42.66	|	32.76	|	0.3	|
|	DIS	|	The Walt Disney Company	|	Communication Services	|	Entertainment	|	0.02	|	2.82E-02	|	2.36E-02	|	0.65	|	FALSE	|	0.07	|	6.76E+08	|	373.31	|	104.86	|	2.56	|
|	MCD	|	McDonald's Corp.	|	Consumer Cyclical	|	Restaurants	|	0.02	|	2.23E-02	|	2.05E-02	|	0.53	|	FALSE	|	0.13	|	1.52E+08	|	202.11	|	184.53	|	0.1	|
|	KO	|	The Coca-Cola Company	|	Consumer Defensive	|	Beverages—Non-Alcoholic	|	0.02	|	1.51E-02	|	1.49E-02	|	0.38	|	FALSE	|	0.1	|	2.14E+08	|	49.87	|	48.5	|	0.03	|
|	WMT	|	Wal-Mart Stores Inc.	|	Consumer Defensive	|	Discount Stores	|	0.02	|	-9.21E-03	|	-1.55E-03	|	-0.11	|	FALSE	|	0.15	|	-1.59E+08	|	-56.07	|	123.98	|	-1.45	|
|	PG	|	The Procter & Gamble Company	|	Consumer Defensive	|	Household & Personal Products	|	0.02	|	-7.94E-03	|	-3.73E-03	|	-0.09	|	FALSE	|	0.05	|	7.13E+08	|	288.64	|	116.71	|	1.47	|
|	CVX	|	Chevron Corporation	|	Energy	|	Oil & Gas Integrated	|	0.02	|	4.05E-02	|	3.23E-02	|	0.9	|	FALSE	|	0.06	|	1.74E+09	|	921.45	|	84.26	|	9.94	|
|	XOM	|	Exxon Mobil Corporation	|	Energy	|	Oil & Gas Integrated	|	0.02	|	3.60E-02	|	2.66E-02	|	0.81	|	FALSE	|	0.03	|	3.18E+09	|	751.2	|	42.9	|	16.51	|
|	JPM	|	JPMorgan Chase & Co.	|	Financial Services	|	Banks—Diversified	|	0.07	|	3.83E-02	|	3.39E-02	|	0.86	|	FALSE	|	0.55	|	1.27E+08	|	41.19	|	94.45	|	-0.56	|
|	WFC	|	Wells Fargo & Company	|	Financial Services	|	Banks—Diversified	|	0.09	|	3.93E-02	|	3.59E-02	|	0.87	|	FALSE	|	0.6	|	7.89E+08	|	192.86	|	30.75	|	5.27	|
|	AXP	|	American Express Company	|	Financial Services	|	Credit Services	|	0.04	|	3.95E-02	|	3.14E-02	|	0.88	|	FALSE	|	0.37	|	2.58E+08	|	320.16	|	91.43	|	2.5	|
|	JNJ	|	Johnson & Johnson	|	Healthcare	|	Drug Manufacturers—General	|	0.02	|	1.18E-02	|	1.26E-02	|	0.32	|	FALSE	|	0.04	|	7.00E+08	|	265.17	|	139.86	|	0.9	|
|	MRK	|	Merck & Co. Inc.	|	Healthcare	|	Drug Manufacturers—General	|	0.02	|	1.47E-02	|	1.47E-02	|	0.37	|	FALSE	|	0.09	|	2.50E+08	|	98.18	|	81.68	|	0.2	|
|	BA	|	The Boeing Company	|	Industrials	|	Aerospace & Defense	|	0.15	|	6.46E-02	|	8.58E-02	|	1.39	|	FALSE	|	0.13	|	5.03E+08	|	892.14	|	162	|	4.51	|
|	GE	|	General Electric Company	|	Industrials	|	Specialty Industrial Machinery	|	0.12	|	4.06E-02	|	1.06E-01	|	0.9	|	FALSE	|	-0.25	|	6.86E+08	|	78.81	|	7.69	|	9.25	|
|	MMM	|	3M Company	|	Industrials	|	Specialty Industrial Machinery	|	0.02	|	2.34E-02	|	2.10E-02	|	0.55	|	FALSE	|	0.06	|	2.85E+08	|	494.79	|	147.5	|	2.35	|
|	HPQ	|	Hewlett-Packard Company	|	Technology	|	Computer Hardware	|	0.02	|	4.98E-02	|	2.89E-02	|	1.09	|	FALSE	|	0.1	|	6.46E+08	|	451.46	|	15.7	|	27.76	|
|	IBM	|	International Business Machines Corporation	|	Technology	|	Information Technology Services	|	0.02	|	3.29E-02	|	2.42E-02	|	0.74	|	FALSE	|	0.09	|	5.72E+08	|	644.16	|	118.8	|	4.42	|
|	MSFT	|	Microsoft Corporation	|	Technology	|	Software—Infrastructure	|	0.02	|	2.67E-02	|	2.52E-02	|	0.62	|	FALSE	|	0.07	|	1.62E+09	|	213.1	|	169.59	|	0.26	|


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
