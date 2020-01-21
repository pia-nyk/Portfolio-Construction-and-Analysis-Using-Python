import pandas as pd
import scipy
import numpy as np
from scipy.stats import norm
from scipy.optimize import minimize

def max_drawdown(return_series: pd.Series):
    """
    Takes a time series of asset returns
    Computes a dataframe that contains
    wealth index
    previous peaks
    drawdowns
    """
    wealth_index = 1000*(1+return_series).cumprod()
    previous_peaks = wealth_index.cummax()
    drawdowns = (wealth_index - previous_peaks)/previous_peaks
    return pd.DataFrame({
        "Wealth": wealth_index,
        "Peaks" : previous_peaks,
        "Drawdowns": drawdowns
    })

def get_ffme_returns():
    """
    Get the fama french dataset for the returns of the 
    top and lowest deciles by market cap
    """
    me_n = pd.read_csv("data/Portfolios_Formed_on_ME_monthly_EW.csv", 
                      header=0, index_col=0, parse_dates=True, na_values=-99.99)
    rets = me_n[["Lo 10", "Hi 10"]]
    rets.columns = ["SmallCap", "LargeCap"]
    rets = rets/100
    rets.index = pd.to_datetime(rets.index, format="%Y%m").to_period("M")
    return rets
    
def get_hfi_returns():
    """
    Get and load the Ken French 30 Industry Portfolios Value Weighted Monthly Returns
    """
    hfi = pd.read_csv("data/edhec-hedgefundindices.csv",
                      header=0, index_col=0, parse_dates=True)
    hfi = hfi/100
    hfi.index = hfi.index.to_period('M')
    return hfi

def get_ind_returns():
    """
    Load and format the EDHEC Hedge Fund Index Returns
    """
    ind = pd.read_csv("data/ind30_m_vw_rets.csv", header=0, index_col=0)/100
    ind.index = pd.to_datetime(ind.index, format="%Y%m").to_period('M')
    ind.columns = ind.columns.str.strip()
    return ind
    

def semideviation(r):
    """
    Returns the semi deviation, aka negative semi deviation of r
    r must be a Series or a DataFrame
    """
    is_negative = r < 0
    return r[is_negative].std(ddof=0)

def skewness(r):
    """
    Alternate to scipy.stats.skew()
    Computes the skewness of the supplied Series or DataFrame
    Returns a float or a series
    """
    demeaned_r = r - r.mean()
    sigma_r = r.std(ddof=0)
    exp = (demeaned_r**3).mean()
    return exp/sigma_r**3

def kurtosis(r):
    """
    Alternate to scipy.stats.kurtosis()
    Computes the kurtosis of the supplied Series or DataFrame
    Returns a float or a series
    """
    demeaned_r = r - r.mean()
    sigma_r = r.std(ddof=0)
    exp = (demeaned_r**4).mean()
    return exp/sigma_r**4

def is_normal(r, level=0.01):
    """
    Applies the Jarque-Bera test to determine if a Series is normal or not.
    Test is applied at 1% level by default
    Returns True if the hypothesis of normality is accepted, else False.
    """
    statistic, pvalue = scipy.stats.jarque_bera(r)
    return pvalue > level

def var_historic(r, levels=5):
    """
    Returns the historic value at risk at a specified level
    i.e returns the level such that "level" percent of returns 
    fall below that number, and the (100-level) percent are above
    """
    if isinstance(r, pd.DataFrame):
        return r.aggregate(var_historic, levels=levels)
    elif isinstance(r, pd.Series):
        return -np.percentile(r, levels, axis=0)
    else:
        raise TypeError("Series or DataFrame expected")

def var_gaussian(r, levels=5, modified=False):
    """
    Returns the Parametric Gaussian VaR of a Series or DataFrame
    If modified is  True, then the modified VaR is returned
    using Cornish-Fisher modifications
    """
    #compute the Z score assuming the distribution is Gaussian
    z = norm.ppf(levels/100)
    
    if modified:
        #calculate the Z score based on kurtosis and skewness 
        s = skewness(r)
        k = kurtosis(r)
        z = (z + 
                (z**2 + 1)*s/6 +
                (z**3 - 3*z)*(k-3)/24 +
                (2*z**3 - 5*z)*(s**2)/36
            )
        
    return -(r.mean()+z*r.std(ddof=0))

def cvar_historic(r, levels=5):
    """
    Computes the conditional VaR or CVaR of the Series or DataFrame
    """
    if isinstance(r, pd.Series):
        is_beyond = r<= -var_historic(r, levels=levels)
        return -r[is_beyond].mean()
    elif isinstance(r, pd.DataFrame):
        return r.aggregate(cvar_historic, levels=levels)
    else:
        raise TypeError("Expected the input to be DataFrame or Series")

def annualized_rets(r, periods_per_year):
    """
    Annualizes a set of returns
    """
    compunded_growth = (1+r).prod()
    n_periods = r.shape[0]
    return compunded_growth**(periods_per_year/n_periods) - 1
    
def annualized_vol(r, periods_per_year):
    """
    Annualises vol for a set of returns
    We should infer the periods per year
    """
    return r.std()*(periods_per_year**0.5)

def sharpe_ratio(r, risk_free_rate, periods_per_year):
    """
    Computes the annualised sharpe ratio of a set of returns
    """
    #convert the annual risk free rate to per period
    rf_per_period = (1+risk_free_rate)**(1/periods_per_year) - 1
    excess_returns = r - rf_per_period
    annual_rets = annualized_rets(excess_returns, periods_per_year)
    annual_vol = annualized_vol(r, periods_per_year)
    return annual_rets/annual_vol
    
def portfolio_return(weights, returns):
    """
    Weights -> Returns
    @ is matrix multiplication
    """
    return weights.T @ returns

def portfolio_vol(weights, comvat):
    """
    Weights -> Volatility
    @ is matrix multiplication
    """
    return (weights.T @ comvat @ weights)**0.5 #weights.T @ comvat @ weights gives us variance

def plot_ef2(n_points, er, cov):
    """
    Plots the 2 asset efficient frontier
    """
    if er.shape[0]!=2:
        raise ValueError("plot_ef2 can only plot 2 asset frontiers")
    weights = [np.array([w, 1-w]) for w in np.linspace(0,1,n_points)]
    rets = [portfolio_return(w, er) for w in weights] 
    vol = [portfolio_vol(w, cov) for w in weights]
    rv = pd.DataFrame({
    "returns": rets,
    "volatility": vol
    })
    return rv.plot.line(x="volatility", y="returns", style=".-")

def minimize_vol(target_return, er, cov):
    """
    target_return -> weight
    """
    n = er.shape[0]
    init = np.repeat(1/n, n)
    bounds = ((0.0, 1.0),)*n
    #constraints for the weights
    return_is_target = {
        'type': 'eq',
        'args': (er,),
        'fun': lambda weights, er: target_return - portfolio_return(weights, er) #the target_return should be the one obtained from portfolio
    }
    
    weights_sum_to_1 = {
        'type': 'eq',
        'fun': lambda weights: np.sum(weights) - 1
    }
    results = minimize(
            portfolio_vol, init,
            args=(cov,), method="SLSQP",
            options = {'disp': False},
            constraints = (return_is_target, weights_sum_to_1),
            bounds = bounds
    )
    return results.x

def optimal_weights(n_points, er, cov):
    """
    list  of returns to run the optimizer on to get the weights
    """
    target_rs = np.linspace(er.min(), er.max(), n_points)
    weights = [minimize_vol(target_return, er, cov) for target_return in target_rs]
    return weights
    
def plot_ef(n_points, er, cov):
    """
    Plots the N asset efficient frontier
    """
    weights = optimal_weights(n_points, er, cov)
    rets = [portfolio_return(w, er) for w in weights] 
    vol = [portfolio_vol(w, cov) for w in weights]
    rv = pd.DataFrame({
    "returns": rets,
    "volatility": vol
    })
    return rv.plot.line(x="volatility", y="returns", style=".-")
    
    