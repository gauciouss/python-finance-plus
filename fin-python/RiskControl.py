from enum import Enum
from Logger import *
import numpy as np
import math
from scipy.stats import norm
import datetime


class PRODUCTION_TYPE(Enum):
        STOCK = 'stock'
        FUTURES = 'futures'
        OPTIONS = 'options'
        WARRANT = 'warrant'
    

class STATISTIC_ALPHABET(Enum):
    Price = 1
    Delta = 2
    Gamma = 3
    Theta = 4
    Vega = 5
    Rho = 6
    Vanna = 7
    Volga = 8
    Charm = 9



class RiskController:

    logger = None

    def __init__(self):
        self.logger = LoggerFactory.getLogger(self)
    
    #計算剩餘到期天數
    def getTimesUpDays(self, year, month, date):
        return (datetime.datetime(year, month, date, 0, 0, 0) - datetime.datetime.today()).days + 0.5 + 1
    
    '''
    計算理論價, delta, theta, vega, rho, vanna volga, charm
    spot: 小台市價
    strike: 履約價
    d2m: 到期天數
    r: 利率
    vol: Hedge V
    option_type
    stats 要算哪個?
    '''
    def BS_pricing(self, spot, strike, d2m, r, vol, option_type, STATISTIC_ALPHABET):
        self.logger.trace("start exec BS_pricing(). spot: {}, strike: {}, d2m: {}, r: {}, vol: {}, option_type: {}, STATISTIC_ALPHABET: {}", spot, strike, d2m, r, vol, option_type, STATISTIC_ALPHABET)
        option_type = -1 if option_type == -1 else 1
        t = d2m / 365
        stats = STATISTIC_ALPHABET.value        
        result = 0
        if t > 0:
            d1 = (math.log(spot / strike) + (r + 0.5 * vol * vol) * t) / (vol * t**0.5)
            d2 = d1 - vol * t ** 0.5
            Nd1 = norm.cdf(d1 * option_type, 0, 1)
            Nd2 = norm.cdf(d2 * option_type, 0, 1)
            Nd1_pdf = norm.pdf(d1, 0, 1)   
            if stats == 1:
                #Price
                result = (spot * Nd1 - strike * math.exp(-r * t) * Nd2) * option_type 
            elif stats == 2:
                #Delta
                result = Nd1 * option_type                  
            elif stats == 3:
                #Gamma
                result = Nd1_pdf / (spot * vol * t ** 0.5)
            elif stats == 4:
                #Theta
                result = (-(spot*Nd1_pdf*vol) / (2*t**0.5) - r * strike * Nd2 * math.exp(-r * t) * option_type ) / 365                
            elif stats == 5:
                #Vega 1%
                result = spot * t ** 0.5 * Nd1_pdf * 0.01                
            elif stats == 6:
                #Rho 1%
                result = strike * t * Nd2 * math.exp(-r * t) * option_type * 0.01
            elif stats == 7:
                #Vanna
                result = -Nd1_pdf * d2 / vol * 0.01                
            elif stats == 8:
                #Volga
                result = spot * t ** 0.5 * Nd1_pdf * d1 * d2 / vol * 0.01 * 0.01                
            elif stats == 9:                
                #Charm
                result = Nd1_pdf * ((r + 0.5 * vol ** 2) * t ** 0.5 - 0.5 * d1 * vol) / (vol * t) * (-1 / 365)
        else:
            if stats == 1:
                #Price
                result = max((spot - strike) * option_type, 0)                
            elif stats == 2:
                #Delta
                if spot > strike:
                    result = 0.5 * (1 + option_type)
                elif spot < strike:
                    result = 0.5 * (-1 + option_type)
                else:
                    result = 0.5 * option_type                
            elif stats == 3:
                #Gamma
                result = 0 if spot != strike else 1                
            elif stats == 4:
                #Theta
                result = 0                
            elif stats == 5:
                #Vega 
                result = 0
            elif stats == 6:
                #Rho 
                result = 0
            elif stats == 7:
                #Vanna
                result = 0
            elif stats == 8:
                #Volga
                result = 0
            elif stats == 9: 
                #Charm
                result = 0
                
        self.logger.trace("complete exec BS_pricing(). spot: {}, strike: {}, d2m: {}, r: {}, vol: {}, option_type: {}, STATISTIC_ALPHABET: {}, result: {}", spot, strike, d2m, r, vol, option_type, STATISTIC_ALPHABET, result)
        return result


    '''
    計算 call 的價值
    stock_price: 目標市價
    strike_price: 履約價
    riskfree_rate:
    maturity: 距離到期日天數
    volatility:
    dividend_rate:
    '''
    def call_price(self, stock_price, strike_price, riskfree_rate, maturity, volatility, dividend_rate):
        self.logger.trace("start exec call_price():=. stock_price: {}, strike_price: {}, riskfree_rate: {}, maturity: {}, volatility: {}, dividend_rate: {}", stock_price, strike_price, riskfree_rate, maturity, volatility, dividend_rate)
        d1 = (math.log((stock_price / strike_price)) + (riskfree_rate - dividend_rate + volatility ** 2 * 0.5) *  maturity) / (volatility * maturity ** 0.5)        
        d2 = d1 - volatility * maturity ** 0.5
        result = stock_price * math.exp(-1 * dividend_rate * maturity) * norm.cdf(d1) - strike_price * math.exp(-1 * riskfree_rate * maturity) * norm.cdf(d2)
        self.logger.info("complete exec call_price(). stock_price: {}, strike_price: {}, riskfree_rate: {}, maturity: {}, volatility: {}, dividend_rate: {}, result: {}", stock_price, strike_price, riskfree_rate, maturity, volatility, dividend_rate, result)
        return result


    '''
    計算 put 的價值
    stock_price: 目標市價
    strike_price: 履約價
    riskfree_rate:
    maturity: 距離到期日天數
    volatility:
    dividend_rate:
    '''
    def put_price(self, stock_price, strike_price, riskfree_rate, maturity, volatility, dividend_rate):
        self.logger.trace("start exec put_price(). stock_price: {}, strike_price: {}, riskfree_rate: {}, maturity: {}, volatility: {}, dividend_rate: {}", stock_price, strike_price, riskfree_rate, maturity, volatility, dividend_rate)
        d1 = (math.log((stock_price / strike_price)) + (riskfree_rate - dividend_rate + volatility ** 2 * 0.5) *  maturity) / (volatility * maturity ** 0.5)        
        d2 = d1 - volatility * maturity ** 0.5
        result = strike_price * math.exp(-1 * riskfree_rate * maturity) * norm.cdf(-d2) - stock_price * math.exp(-1 * dividend_rate * maturity) * norm.cdf(-d1)     
        self.logger.info("complete exec put_price(). stock_price: {}, strike_price: {}, riskfree_rate: {}, maturity: {}, volatility: {}, dividend_rate: {}, result: {}", stock_price, strike_price, riskfree_rate, maturity, volatility, dividend_rate, result)
        return result

    '''
    計算 call / warrant 的隱藏波動率
    target_price: 目標市價
    Strike: 履約價
    riskfree_rate:
    d2m: 距離到期日天數
    Strike_price: 履約價價格
    ratio: 
    '''
    def implied_vol_for_warrant(self, target_price, Strike, riskfree_rate, d2m, Strike_price, ratio):
        self.logger.trace('start exec implied_vol_for_warrant(). target_price: {}, Strike: {}, riskfree_rate: {}, d2m: {}, Strike_price: {}, ratio: {}', target_price, Strike, riskfree_rate, d2m, Strike_price, ratio)
        result = 0
        fa = 0
        c = 0
        count = 0
        t = d2m / 365
        a = 0.001
        b = 0.999      
        self.logger.debug("(target_price - Strike) * ratio = " + (str((target_price - Strike) * ratio)))  
        if Strike_price <= (target_price - Strike) * ratio:
            result = 0
        else:
            fa = self.call_price(target_price * ratio, Strike * ratio, riskfree_rate, t, a, 0) - Strike_price
            self.logger.debug("fa = {}", str(fa))
        
        while True:
            if abs(fa) < 0.005:
                break
            
            c = (a + b) / 2
            fc = self.call_price(target_price * ratio, Strike * ratio, riskfree_rate, t, c, 0) - Strike_price            
            if fa * fc < 0:
                b = c
            else:
                a = c
                fa = fc
            count = count + 1

            if count > 10:
                break

        result = c
        self.logger.info('complete exec implied_vol_for_warrant(). target_price: {}, Strike: {}, riskfree_rate: {}, d2m: {}, Strike_price: {}, ratio: {}, result: {}', target_price, Strike, riskfree_rate, d2m, Strike_price, ratio, result)
        return result

    '''
    計算 put 的隱藏波動率
    '''
    def implied_vol_for_put(self, target_price, Strike, riskfree_rate, d2m, Strike_price, ratio):
        self.logger.trace('start exec implied_vol_for_put(). target_price: {}, Strike: {}, riskfree_rate: {}, d2m: {}, Strike_price: {}, ratio: {}', target_price, Strike, riskfree_rate, d2m, Strike_price, ratio)
        result = 0
        fa = 0
        c = 0
        count = 0
        t = d2m / 365
        a = 0.001
        b = 0.999   
        if Strike_price <= (Strike - target_price) * ratio:
            result = 0
        else:
            fa = self.put_price(target_price * ratio, Strike * ratio, riskfree_rate, t, a, 0) - Strike_price
            self.logger.debug("fa = {}", str(fa))
        

        while True:
            if abs(fa) < 0.005:
                break

            c = (a + b) / 2            
            fc = self.put_price(target_price * ratio, Strike * ratio, riskfree_rate, t, c, 0) - Strike_price

            if fa * fc < 0:
                b = c
            else:
                a = c
                fa = fc
            count = count + 1
            if count > 10:
                break
        
        result = c
        self.logger.info('complete exec implied_vol_for_put(). target_price: {}, Strike: {}, riskfree_rate: {}, d2m: {}, Strike_price: {}, ratio: {}, result: {}', target_price, Strike, riskfree_rate, d2m, Strike_price, ratio, result)
        return result

########################
r = RiskController()

#print(r.BS_pricing(10878, 10200, r.getTimesUpDays(2018, 10, 17), 0.02, 0.112, 0, STATISTIC_ALPHABET.Price))

iv = r.implied_vol_for_put(10887, 10400, 0.02, r.getTimesUpDays(2018, 10, 17), 32, 1)
print(iv)

#pp = r.put_price(10887*0.02, 10400, 1, 32.5/365, 0.001, 0)
#print(pp)