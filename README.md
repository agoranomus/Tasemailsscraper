This python code exports companie`s emails from Tel Aviv stock Exchage official website into a csv file

you can replace the "securitiesmarketdata" file with an updated list of companies that you can download from tase.co.il

then make sure that you rename the raw above the issuer number and security number to ensure correct loading of each company page

example:
issuer_column = 'R'
security_column = 'A'

