# Portfolio Construction and Analysis Using Python

<b> Important formulae and concepts </b>

<ul>
  <li> Profit/Loss on investment = <img src="https://render.githubusercontent.com/render/math?math=(P_{t+2} - P_{t+1})/P_{t+1}"></li>
  <li> Price Returns = <img src="https://render.githubusercontent.com/render/math?math=P_{t+2} - P_{t+1}"></li>
  <li> Compounded returns <img src="https://render.githubusercontent.com/render/math?math=R_{t,t+2} = (1+R_{t,t+1})(1+R_{t+1,t+2})"></li>
  <li> Annualized returns = <img src="https://render.githubusercontent.com/render/math?math=((1+r_1)*(1+r_2)*...(1+r_n))^{1/n} - 1"></li>
  <li> Measure of volatility = <img src="https://render.githubusercontent.com/render/math?math=$\sqrt{variance}$"></li>
  <li> Annualized Volatility <img src="https://render.githubusercontent.com/render/math?math=$\sigma_{ann}$ = $\sigma_p\sqrt{p}$"></li>
  <li> Sharpe Ratio = Excess returns/annualized volatility </li><br/>
  
 <i> Check out the use of sharpe ratio to assess investment returns on Small cap and Large cap companies - Risk_Adjusted_Returns.ipynb</i>

  <li> Maximum drawdown = (Trough value - Peak value)/Peak value </li><br/>
  
  <i> Calculating MDD for Small cap and Large cap companies - Working_with_drawdowns.ipynb</i>
  
  <b> Why skewness and kurtosis should be considered? </b><br/>
  The returns in real world hardly ever follow Gaussian distribution. The returns are much larger/smaller in actual. Skewness, being the measure of assymetry tells how much a curve deviates from normal.
  In theory, the probability of getting extreme returns should diminish symmetrically as in the tails of a normal curve. however, the actual probabilities turn out to be higher. For analysing this, kurtosis can be used. 
  Kurtosis, gives us information about the thickness of the tail of the distruibution. 
  
  <b> Jaque-Bera test </b> can be used to find the normality of returns data. 
  
  <li>S(R) = <img src="https://render.githubusercontent.com/render/math?math=E[(R - E(R))^3]/[Var(R)]^{3/2}"></li>
  <li>K(R) = <img src="https://render.githubusercontent.com/render/math?math=E[(R - E(R))^4]/[Var(R)]^2"></li>
  
  <i> Checking the normality of hedge fund indices - Devaition From Normality.ipynb </i>
  
<b> Semi-deviation </b><br/>
  Investors are usually interested in looking at the extremes on the negative side. Semi-deviation or semi-volatility is the deviation below the mean. <br/>
  
  <li> Value at risk (VaR) = maximum loss that can occur to a portfolio holding with a given probability </li>
  <li> Beyond VaR (CVar) = Expected return, conditional upon the return being less than the value at risk number = <img src="https://render.githubusercontent.com/render/math?math=-E(R|R < -VaR)"></li>
  
  Finding out VaR and CVaR on Hedge fund indices - Downside Measures.ipynb
  
  <b> Standard methods for calculating VaR </b>
  <ol>
    <li> Historical (Non-Parametric) - no model assumption required but relies completely on historical data </li>
    <li> Variance-Covariance (Parametric Gaussian) - assumes a Gaussian distribution but returns hardly follow such a distribution </li>
    <li> Parametric Non Gaussian - Specification risk involved (risk of having chosen wrong model) </li>
    <li> Cornish Fisher (Semi Fisher) - no model assumption required <img src="https://render.githubusercontent.com/render/math?math=Z_$\alpha$' = Z_$\alpha$ + cohesion"><li>
  </ol>
  
  
  

  
