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
                                            Company                  Sector                         Industry  Cost of Debt  Cost of Equity  Cost of Capital  beta Beta is fallback  taxrate  Entreprise Value  Share Value  Share Price  Potential Gain/Loss
Ticker
DD             E. I. du Pont de Nemours and Company         Basic Materials                        Chemicals          0.15        4.01e-02         4.51e-02  0.89            False     0.61          1.24e+08       168.23        37.55                 3.48
DOW                        The Dow Chemical Company         Basic Materials                        Chemicals          0.14        1.05e-01         7.06e-02  1.29            False     0.82          3.17e+07        42.66        32.76                 0.30
DIS                         The Walt Disney Company  Communication Services                    Entertainment          0.02        2.82e-02         2.36e-02  0.65            False     0.07          6.76e+08       373.31       104.86                 2.56
MCD                                McDonald's Corp.       Consumer Cyclical                      Restaurants          0.02        2.23e-02         2.05e-02  0.53            False     0.13          1.52e+08       202.11       184.53                 0.10
KO                            The Coca-Cola Company      Consumer Defensive          Beverages—Non-Alcoholic          0.02        1.51e-02         1.49e-02  0.38            False     0.10          2.14e+08        49.87        48.50                 0.03
WMT                            Wal-Mart Stores Inc.      Consumer Defensive                  Discount Stores          0.02       -9.21e-03        -1.55e-03 -0.11            False     0.15         -1.59e+08       -56.07       123.98                -1.45
PG                     The Procter & Gamble Company      Consumer Defensive    Household & Personal Products          0.02       -7.94e-03        -3.73e-03 -0.09            False     0.05          7.13e+08       288.64       116.71                 1.47
CVX                             Chevron Corporation                  Energy             Oil & Gas Integrated          0.02        4.05e-02         3.23e-02  0.90            False     0.06          1.74e+09       921.45        84.26                 9.94
XOM                         Exxon Mobil Corporation                  Energy             Oil & Gas Integrated          0.02        3.60e-02         2.66e-02  0.81            False     0.03          3.18e+09       751.20        42.90                16.51
JPM                            JPMorgan Chase & Co.      Financial Services                Banks—Diversified          0.07        3.83e-02         3.39e-02  0.86            False     0.55          1.27e+08        41.19        94.45                -0.56
WFC                           Wells Fargo & Company      Financial Services                Banks—Diversified          0.09        3.93e-02         3.59e-02  0.87            False     0.60          7.89e+08       192.86        30.75                 5.27
AXP                        American Express Company      Financial Services                  Credit Services          0.04        3.95e-02         3.14e-02  0.88            False     0.37          2.58e+08       320.16        91.43                 2.50
JNJ                               Johnson & Johnson              Healthcare       Drug Manufacturers—General          0.02        1.18e-02         1.26e-02  0.32            False     0.04          7.00e+08       265.17       139.86                 0.90
MRK                                Merck & Co. Inc.              Healthcare       Drug Manufacturers—General          0.02        1.47e-02         1.47e-02  0.37            False     0.09          2.50e+08        98.18        81.68                 0.20
BA                               The Boeing Company             Industrials              Aerospace & Defense          0.15        6.46e-02         8.58e-02  1.39            False     0.13          5.03e+08       892.14       162.00                 4.51
GE                         General Electric Company             Industrials   Specialty Industrial Machinery          0.12        4.06e-02         1.06e-01  0.90            False    -0.25          6.86e+08        78.81         7.69                 9.25
MMM                                      3M Company             Industrials   Specialty Industrial Machinery          0.02        2.34e-02         2.10e-02  0.55            False     0.06          2.85e+08       494.79       147.50                 2.35
HPQ                         Hewlett-Packard Company              Technology                Computer Hardware          0.02        4.98e-02         2.89e-02  1.09            False     0.10          6.46e+08       451.46        15.70                27.76
IBM     International Business Machines Corporation              Technology  Information Technology Services          0.02        3.29e-02         2.42e-02  0.74            False     0.09          5.72e+08       644.16       118.80                 4.42
MSFT                          Microsoft Corporation              Technology          Software—Infrastructure          0.02        2.67e-02         2.52e-02  0.62            False     0.07          1.62e+09       213.10       169.59                 0.26

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
