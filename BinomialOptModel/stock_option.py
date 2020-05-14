import math
import numpy as np
from stock_volatility import stock_vol


class option():

	def __init__(self, S0, K, r, T, N, prm):
		"""
		Initialise parameters
		:param S0: initial stock price
		:param K: strike price
		:param r: risk free interest rate per year
		:param T: length of option in years
		:param N: number of binomial iterations
		:param prm: dictionary with additional parameters
		"""
		self.S0 = S0
		self.K = K
		self.r = r
		self.T = T
		self.N = N
		"""
		prm parameters:
		start = date from when you want to analyse stocks, "yyyy-mm-dd"
		end = date of final stock analysis (likely current date), "yyyy-mm-dd"
		tk = ticker label
		div = dividend paid
		is_calc = is volatility calculated using stock price history, boolean
		use_garch = use GARCH model, boolean
		sigma = volatility of stock
		is_call = is it a call option, boolean
		eu_option = European or American option, boolean
		"""
		self.tk = prm.get('tk', None)
		self.start = prm.get('start', None)
		self.end = prm.get('end', None)
		self.div = prm.get('div', 0)
		self.is_calc = prm.get('is_calc', False)
		self.use_garch = prm.get('use_garch', False)
		self.vol = stock_vol(self.tk, self.start, self.end)
		if self.is_calc:
			if self.use_garch:
				self.sigma = self.vol.garch_sigma()
			else:
				self.sigma = self.vol.mean_sigma()
		else:
			self.sigma = prm.get('sigma', 0)
		self.is_call = prm.get('is_call', True)
		self.eu_option = prm.get('eu_option', True)
		'''
		derived values:
		dt = time per step, in years
		df = discount factor
		'''
		self.dt = T/float(N)
		self.df = math.exp(-(r-self.div)*self.dt)
		self.M = self.N + 1
		self.u = math.exp(self.sigma*math.sqrt(self.dt))
		self.d = 1./self.u
		self.qu = (math.exp((self.r-self.div)*self.dt)-self.d)/(self.u-self.d)
		self.qd = 1-self.qu

	def stocktree(self):
		stocktree = np.zeros([self.M, self.M])
		for i in range(self.M):
			for j in range(i+1):
				stocktree[j, i] = self.S0*(self.u**(i-j))*(self.d**j)
		return stocktree

	def optiontree(self,stocktree):
		option = np.zeros([self.M, self.M])
		if self.is_call:
			option[:,self.N] = np.maximum(np.zeros(self.M), (stocktree[:,self.N] - self.K))
			for i in np.arange(self.N-1, -1, -1):
				for j in range(i+1):
					option[j,i] = math.exp(-self.r*self.dt)*(self.qu*option[j,i+1] + self.qd*option[j+1,i+1])
		else:
			option[:,self.N] = np.maximum(np.zeros(self.M), (self.K - stocktree[:,self.N]))
			if self.eu_option:
				for i in np.arange(self.N-1, -1, -1):
					for j in range(i+1):
						option[j,i] = math.exp(-self.r*self.dt)*(self.qu*option[j,i+1] + self.qd*option[j+1,i+1])
			else:
				for i in np.arange(self.N-1, -1, -1):
					for j in range(i+1):
						option[j,i] = np.maximum((self.K-stocktree[j,i]), math.exp(-self.r*self.dt)*(self.qu*option[j,i+1] + self.qd*option[j+1,i+1]))
		return option

	def price(self):
		stocktree = self.stocktree()
		optiontree = self.optiontree(stocktree)
		optionprice = optiontree
		return optionprice[0,0]
