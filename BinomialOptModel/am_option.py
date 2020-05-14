import numpy as np
from stock_option import stockoption
import math


class american_option(stockoption):
    def __int_prms__(self):
        self.M = self.N+1
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
            return option
        else:
            option[:,self.N] = np.maximum(np.zeros(self.M), (self.K - stocktree[:,self.N]))
        for i in np.arange(self.N-1, -1, -1):
            for j in range(i+1):
                option[j,i] = np.maximum((self.K-stocktree[j,i]), math.exp(-self.r*self.dt)*(self.qu*option[j,i+1] + self.qd*option[j+1,i+1]))
        return option

    def price(self):
        self.__int_prms__()
        stocktree = self.stocktree()
        optiontree = self.optiontree(stocktree)
        optionprice = optiontree
        return optionprice[0,0]
