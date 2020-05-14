from stock_option import option

putoption_eu = option(217.58, 217, 0.05, 0.1, 5, {'tk': 'AAPL', 'is_calc': True, 'start': '2017-08-18',
                                                     'end': '2018-08-18', 'is_call': False, 'eu_option':True})
putoption_am = option(217.58, 217, 0.05, 0.1, 5, {'tk': 'AAPL', 'is_calc': True, 'start': '2017-08-18',
                                                     'end': '2018-08-18', 'is_call': False, 'eu_option':False})

print(putoption_eu.price())
print(putoption_am.price())
