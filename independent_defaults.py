import numpy as np

profit_matrix = 0

def independent_binomial_loss_distribution(N,M,p,c,r,alpha):
    # Seed an M*N matrix with uniformly random values between 0 and 1
    U = np.random.uniform (0,1,[M,N])

    # Calculate default events by comparing each simulation vector with 
    # the associated probability of default
    default_indicator = 1*np.less(U,p)

    # Loss distribution is sorted dot product of default indicator matrix U, and
    # loss exposure vector, c
    gross_loss_distribution = np.sort(np.dot(default_indicator,c),axis=None)

    global profit_matrix
    
    # Profit matrix is opposite of the default matrix
    profit_matrix = np.less(default_indicator,1)
    
    # Gross loss for each simulation is gross loss + net revenue
    net_loss_distribution = np.sort(np.dot(default_indicator,c)+np.dot(profit_matrix,r),axis=None)[::-1]
    
    return net_loss_distribution

def compute_risk_measures(M,loss_distribution,alpha):
    # initialise result vectors
    expected_shortfall = np.zeros([len(alpha)])
    var = np.zeros([len(alpha)])

    # expected loss is simple average of the loss distribution
    expected_loss = np.mean(loss_distribution)
    print(f"Expected loss: {expected_loss:.2f}")

    # loss volatility is the standard deviation of the loss distribution
    un_expected_loss = np.std(loss_distribution)
    print(f"unExpected loss: {un_expected_loss:.2f}")
    
    for n in range (0,len(alpha)):
        # Determine the index of the siumulation run representing the 
        # quantile being evaluated in this iteration
        my_quantile = np.ceil(alpha[n]*(M-1)).astype(int)
        # Shortfall is the average loss beyond a given quartile
        expected_shortfall[n] = np.mean(loss_distribution[my_quantile:M-1])
        # Value at risk is the value of the expected loss at the given quartile
        var[n] = loss_distribution[my_quantile]
        print(f"{alpha[n]*100}th: {expected_shortfall[n]:.2f}, {var[n]:.2f}")
        
    return expected_loss, un_expected_loss, var, expected_shortfall

def independent_binomial_simulation(N,M,p,c,r,alpha):
    print(f"Total liability: {sum(c):.2f}")
    print(f"Total portfolio net revenue: {sum(r):.2f}")
    
    print(f"Independent defaults Monte Carlo. {M} iterations.")
    loss_distribution = independent_binomial_loss_distribution(N,M,p,c,r,alpha)
    el,ul,var,es = compute_risk_measures(M,loss_distribution,alpha)
    return el, ul, var, es, loss_distribution