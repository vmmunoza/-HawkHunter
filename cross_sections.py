
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit


# IBD cross section constants, from Strumia and Vissani 2003
m_e = 0.511  # MeV
m_p = 938.272 # MeV
m_n = 939.565   # MeV
np_dif =  m_n - m_p # 1.293 MeV
Mnp = (m_p + m_n)/2. # 938.9 MeV
G_F = 1.166e-5  # GeV^-2
costhetaC = 0.9746  # cosine of Cabibbo angle
M_V = np.sqrt(0.71) # MeV
M_A = 1.    # MeV
m_pi = 139. # MeV
xi = 3.706
g1_0 = -1.270
Eth = ((m_n + m_e)**2. - m_p**2.)/(2.*m_p)  # nu threshold in cross section, 1.8057 MeV
delta = (m_n**2. - m_p**2. - m_e**2.)/(2.*m_p)

E_nu_th = np_dif + m_e   # nu threshold 1.804 MeV


# From Strumia and Vissani 2003
def dsigmadE_IBD(E_nu, E_e):

    # Mandelstam variables
    s = 2.*m_p*E_nu + m_p**2.
    u = s + m_e**2. - 2.*m_p*(E_nu + E_e)
    t = m_n**2. - m_p**2. - 2.*m_p*(E_nu - E_e)

    # f and g dimensionless form factors
    f1 = ( 1.- (1.+xi)*t/(4.*Mnp**2.) )/(1. - t/(4.*Mnp**2.) )/(1. - t/(M_V**2.) )**2.
    f2 = xi/(1. - t/(4.*Mnp**2.) )/(1. - t/(M_V**2.) )**2.
    g1 = g1_0/(1. - t/(M_A**2.) )**2.
    g2 = 2.*Mnp**2.*g1/(m_pi**2. - t)

    # Complete expression
    #A = (t-m_e)**2./16.*( 4.*f1**2.*(4.*Mnp**2. + t + m_e**2.) + 4.*g1**2.*(-4.*Mnp**2. + t + m_e**2.) + f2**2.*(t**2./Mnp**2. + 4.*t + 4.*m_e**2.) + 4.*m_e**2.*t*g2**2./Mnp**2. + 8. )
    #B =
    #C =

    # NLO approx, Strumia and Vissani 2003 eqs. 10
    A = Mnp**2.*( f1**2. - g1**2. )*(t - m_e**2.) - Mnp**2.*np_dif**2.*( f1**2. + g1**2. ) -2.*m_e**2.*Mnp*np_dif*g1*( f1 + f2 )
    B = t*g1*(f1+f2)
    C = ( f1**2. + g1**2. )/4.

    """
    EnuCM = (s-m_p**2.)/(2.*np.sqrt(s))
    EeCM = (s - m_n**2. + m_e**2.)/(2.*np.sqrt(s))
    peCM = np.sqrt( (s - ( m_n - m_e )**2.)*( s - ( m_n + m_e )**2. ) )/(2.*np.sqrt(s))
    #peCM[peCM == np.nan] = 1.e-1

    E_1 = E_nu - delta - EnuCM*(EeCM + peCM)/m_p
    E_2 = E_nu - delta - EnuCM*(EeCM - peCM)/m_p
    #print(E_1, E_2)
    """

    Msquare = A - (s-u)*B + (s-u)**2.*C
    dsigmadt = G_F**2.*costhetaC**2./(2.*np.pi*(s-m_p**2.)**2.)*Msquare
    # Allowed range of energies for E_nu and E_e
    all_range = 1.#np.heaviside( E_nu - Eth, 0. )#*np.heaviside( E_e - E_1, 0. )*np.heaviside( E_2 - E_e, 0. )
    dsigmadEe = 2.*m_p*dsigmadt*all_range
    return dsigmadEe

"""
E_ovec = np.linspace(2.,50)
plt.loglog(E_ovec, dsigmadE_IBD(E_ovec, 1.))
plt.loglog(E_ovec, dsigmadE_IBD(E_ovec, 10.))
plt.loglog(E_ovec, dsigmadE_IBD(E_ovec, 20.))

plt.show()
exit()
"""

# From 1712.06985, in cm^2, correction from Beacom DSNB review
def sigmaIBD(E_e):
    return 9.52e-44*( E_e*np.sqrt(E_e**2. - m_e**2.) )*(1. - 7.*(E_e + np_dif)/m_p )

# nu Argon cross section for DUNE
# From Denton and Suliga mail
EE, sig = np.loadtxt("data/nuAr_XS.txt", unpack=True, delimiter=";")
sigmaAr = interp1d(EE, sig)

"""
def fitfunc(E, A, alp):
    return A*E**alp

#fitpars = np.polyfit(EE, np.log10(sig), 2)
#fit = np.poly1d(fitpars)
fitpars, firtcov = curve_fit(fitfunc, EE, np.log10(sig))


Eii = np.linspace(EE[0], EE[-1])
plt.plot(EE, sig)
#plt.plot(Eii, 10.**fit(Eii))
plt.plot(Eii, 10.**fitfunc(Eii, *fitpars))
plt.plot(Eii, 10.**(-44.8*Eii**(-0.035)),"g:")
plt.yscale("log")
#plt.xscale("log")
#print(fitpars)
print(np.abs(10.**fitfunc(Eii, *fitpars) - sigmaAr(Eii))/sigmaAr(Eii))

plt.show()
"""
