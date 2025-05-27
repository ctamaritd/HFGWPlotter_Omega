import numpy as np
####Definition of analytic function for spectrum of sound waves from 1st-order PT
#Function of nucleation temperature T* in GeV and dimless parameters alpha, betaoverH, vw, gstar
# f in Hz
#
# Modified to agree with UHFGW review, use 2007.08537

def OmegaPT(Tstar, alpha, betaoverH, vw, gstar, f):
    hubbleh = 0.6766
    TildeOmegagw = 0.058# 1.e-2
    HstarRstar = vw*(8.*np.pi)**(1/3.)/(betaoverH)
    fp0 = 26.e-6*(1./HstarRstar)*(Tstar/100.)*(gstar/100.)**(1/6.)
    s = f/fp0
    C = s**3.*(7./(4.+3.*s**2))**(7./2.)
    kappaA = vw**(6/5)*6.9*alpha/(1.36-0.037*np.sqrt(alpha)+alpha)
    kappaB = alpha**(2/5.)/(0.017+(.997+alpha)**(2/5))
    cs = 1/np.sqrt(3.)
    kappa = cs**(11./5)*kappaA*kappaB/((cs**(11./5)-vw**(11./5))*kappaB+vw*cs**(6/5)*kappaA)
    K = kappa*alpha/(1+alpha)
    tauswHstar = 4/3*HstarRstar/K
    Y=1-1/(np.sqrt(1+2*tauswHstar))
    #Use convention of hc from UHFWG review, hc =sqrt(3) H0/(2Pi f) Sqrt{Omega}
    return(#This was for hc, now we do h2Omega (6.04453E-19/f)*np.sqrt(4.98e-5/hubbleh**2*(100./gstar)**(1./3.)*K**2*(HstarRstar)*TildeOmegagw*C*Y)
        4.98e-5*(100./gstar)**(1./3.)*K**2*(HstarRstar)*TildeOmegagw*C*Y
        )



    
