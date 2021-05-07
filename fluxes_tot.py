
import matplotlib.pyplot as plt
import numpy as np
import math
#!python
import pylab
from pylab import arange,pi,sin,cos,sqrt
from scipy import integrate
from scipy.interpolate import interp1d, Rbf
from flux_stuff import *
import os

for path in ["figures", "folder_fluxes"]:
    if not os.path.exists(path):
        os.system("mkdir "+path)

def compute_flux(Mpbhs, fpbhs, plot_fluxes = 0):

    fluxes_max = []
    for mm, Mpbh in enumerate(Mpbhs):

        folder = "BlackHawkData/{:.1e}/".format(Mpbh)

        if not os.path.exists("folder_fluxes/{:.1e}".format(Mpbh)):
            os.system("mkdir "+"folder_fluxes/{:.1e}".format(Mpbh))

        #-----------
        # INST FILES
        #-----------

        data_primary = np.genfromtxt(folder+"instantaneous_primary_spectra.txt",skip_header = 2)
        data_secondary = np.genfromtxt(folder+"instantaneous_secondary_spectra.txt",skip_header = 2)
        E_prim = data_primary[:,0]
        E_sec = data_secondary[:,0]

        tot_sec = 0.
        for i in [2,3,4]:   # three neutrino species
            tot_sec += data_secondary[:,i+1]

        #flux_max = max(tot_sec)
        #plt.loglog(E_sec,tot_sec, linestyle="--", color=cols[mm])
        #plt.loglog(E_prim,data_primary[:,6],label = r"$M_{\rm PBH}=$"+scinot(Mpbh)+" g", color=cols[mm])

        spec_prim = interp1d(E_prim,data_primary[:,6],fill_value="extrapolate")
        spec_sec = interp1d(E_sec,tot_sec,fill_value="extrapolate")
        #spec_prim = np.vectorize(spec_prim)
        #spec_sec = np.vectorize(spec_sec)

        zmin = 0.
        if Mpbh<Mevap:
            zmin = zevap(Mpbh)
        zmax = (1.+zmin)*1.e5 - 1.
        print("Mass: {:.1e}, z evaporation: {:.1e}".format( Mpbh, zmin ) )

        flux_prim = flux(zmin, zmax, Mpbh, E_prim, spec_prim)
        flux_sec = flux(zmin, zmax, Mpbh, E_sec, spec_sec)

        fluxes_max.append( max(flux_sec*fpbhs[mm]) )

        if Mpbh<Mevap:
            fpbhlabel = r" g, $\beta'=$"
        else:
            fpbhlabel = r" g, $f_{\rm PBH}=$"

        if plot_fluxes:

            #plt.loglog( E_prim, fpbhs[mm]*flux_prim, color = cols[mm], label = r"$M_{\rm PBH}=$"+scinot(Mpbh)+fpbhlabel+scinot(fpbhs[mm]) )
            plt.loglog( E_sec, fpbhs[mm]*flux_sec, color = cols[mm], linestyle="-", label = r"$M_{\rm PBH}=$"+scinot(Mpbh)+fpbhlabel+scinot(fpbhs[mm]) )
            #plt.loglog( Evec, fpbhs[mm]*flux_anal(Evec, Mpbh), color = cols[mm], linestyle=":" )#, label = r"$M_{\rm PBH}=$"+scinot(Mpbh)+r" g, $f_{\rm PBH}=$"+scinot(fpbhs[mm]) )
            #plt.loglog( Evec, fpbhs[mm]*flux_approx(Evec, Mpbh), linestyle="--", color = cols[mm] )

        #np.savetxt("BlackHawkData/{:.1e}/flux.txt".format(Mpbh), np.transpose([E_sec, flux_sec]) )

        np.savetxt("folder_fluxes/{:.1e}/flux.txt".format(Mpbh), np.transpose([E_sec, flux_sec]) )

        # Use total only if they evaporate (CHECK THIS)
        if Mpbh<Mevap:

            #-----------
            # TOT FILES
            #-----------

            spec_tot_prim = np.genfromtxt(folder + "neutrinos_primary_spectrum.txt",skip_header = 1)
            spec_tot_e = np.genfromtxt(folder + "nu_e_secondary_spectrum.txt",skip_header = 1)
            spec_tot_mu = np.genfromtxt(folder + "nu_mu_secondary_spectrum.txt",skip_header = 1)
            spec_tot_tau = np.genfromtxt(folder + "nu_tau_secondary_spectrum.txt",skip_header = 1)
            Evec = spec_tot_e[0,1:]
            timevec = spec_tot_e[1:,0]
            Evec_prim = spec_tot_prim[0,1:]
            timevec_prim = spec_tot_prim[1:,0]
            spec_tot = spec_tot_e + spec_tot_mu + spec_tot_tau

            for it, t in enumerate(timevec):
                if timevec[it-1]==t:
                    finindex = it
                    break

            """plt.loglog(Evec, spec_tot[150,1:],"m:",lw=4,alpha=0.5,label=r"$t=${:.1e}".format(timevec[2]))
            plt.loglog(Evec, spec_tot[150,1:],"r:",lw=4,alpha=0.5,label=r"$t=${:.1e}".format(timevec[150]))
            plt.loglog(Evec, spec_tot[finindex,1:],"g:",lw=4,alpha=0.5,label=r"$t=${:.1e}".format(timevec[finindex]))
            plt.loglog(Evec, spec_tot[-1,1:],"b:",lw=4,alpha=0.5,label=r"$t=${:.1e}".format(timevec[-1]))
            plt.loglog(Evec_prim, spec_tot_prim[2,1:],"m")
            plt.loglog(Evec_prim, spec_tot_prim[150,1:],"r")
            plt.loglog(Evec_prim, spec_tot_prim[finindex,1:],"g")
            plt.loglog(Evec_prim, spec_tot_prim[-1,1:],"b")
            #plt.ylim(1.e-29, 1e30)
            plt.ylim(1.e-10, 1e25)
            plt.xlim(1., 1e15)
            plt.legend()
            plt.xlabel('$E{\\rm \,\, (GeV)}$')
            plt.ylabel('${\\rm d}N/d E dt \,\, ({\\rm GeV}^{-1}{\\rm s}^{-1})$')
            plt.savefig("figures/dNdEdt_test.pdf", bbox_inches='tight')
            plt.show()
            exit()"""

            #xx, yy = np.meshgrid(Evec, timevec)
            #d2NdEdt_ts = Rbf(np.log10(xx), np.log10(yy), np.log10(np.transpose(spec_tot[1:,1:])),kind="linear")
            #print(d2NdEdt_ts)
            #exit()

            reds = z_from_t(timevec)
            #reds = redshift(timevec)

            d2NdEdt_ts = []
            wi = []
            for it, time in enumerate(timevec):
                d2NdEdt = spec_tot[1+it,1:]
                d2NdEdt_time = interp1d(Evec,d2NdEdt,fill_value="extrapolate")
                d2NdEdt_time_prim = interp1d(Evec_prim,spec_tot_prim[1+it,1:],fill_value="extrapolate")

                #wi.append( blackbody(Evec*(1.+redshift(time)), Mpbh) )
                #we = dNdEdt_extension(Evec[-1]*(1.+reds[it]),d2NdEdt_time,Evec*(1.+reds[it]),Mpbh)
                we = d2NdEdt_time(Evec*(1.+reds[it]))

                #we = np.zeros_like(Evec)

                for iE, EE in enumerate(Evec):
                    if EE*(1.+reds[it])>Evec[-1]:
                        #we[iE] = blackbody(EE*(1.+reds[it]), Mpbh)
                        we[iE] = d2NdEdt_time_prim(EE*(1.+reds[it]))

                    #if EE*(1.+redshift(time))>4.*Tpbh(Mpbh):
                    #if EE*(1.+reds[it])>4.*Tpbh(Mpbh):
                    #    we[iE] = min(we[iE], blackbody(EE*(1.+reds[it]), Mpbh))

                    """if EE*(1.+reds[it])>Evec[-1]:
                        we[iE] = blackbody(EE*(1.+reds[it]), Mpbh)
                    else:
                        we[iE] = d2NdEdt_time(EE*(1.+reds[it]))"""
                    #if EE*(1.+redshift(time))>Evec[-1]:
                    #    we[iE] = blackbody(EE*(1.+redshift(time)), Mpbh)

                d2NdEdt_ts.append(  we )
            d2NdEdt_ts = np.array(d2NdEdt_ts)


            finite_differences = 1

            """plt.loglog(Evec, d2NdEdt_ts[150,:],":",lw=4,alpha=0.5)
            plt.loglog(Evec, d2NdEdt_ts[250,:],":",lw=4,alpha=0.5)
            plt.loglog(Evec, wi[150])
            plt.loglog(Evec, wi[250])
            plt.show()
            exit()"""

            flux_tot = []
            for j, EE in enumerate(Evec):
                #integrand = d2NdEdt_ts[:,j]*(1.+redshift(timevec))
                integrand = d2NdEdt_ts[:,j]*(1.+reds)
                if finite_differences:
                    integral = 0.
                    for it, t in enumerate(timevec[:-2]):
                        integral += (timevec[it+1]-timevec[it])*integrand[it]
                else:
                    integral = integrate.simps( integrand[:finindex]*timevec[:finindex], np.log(timevec[:finindex]) )

                #print(np.mean(d2NdEdt_ts[:,j]*(1.+redshift(timevec))*timevec))
                flux_tot.append( n_pbh(Mpbh)*integral*c )
                #print(integral)
            flux_tot = np.array(flux_tot)

            plt.loglog( Evec, fpbhs[mm]*flux_tot, color = cols[mm], linestyle=":" )

            np.savetxt("folder_fluxes/{:.1e}/flux.txt".format(Mpbh), np.transpose([Evec, flux_tot]) )

    return fluxes_max

if __name__=="__main__":

    plot_fluxes = 1

    Mpbhs =  [1.e15,  2.e15, 4.e15, 8.e15]
    #Mpbhs =  [1.e10, 1.e11, 1.e12, 1.e13, 1.e14]
    #Mpbhs =  [1.e10]
    #Mpbhs = np.linspace(1.e15, 1.e16, 10)

    fpbhs = np.ones_like(Mpbhs)    # this is beta prime!
    cols = ["r", "m", "purple", "b", "g", "orange"]

    fluxes_max = compute_flux(Mpbhs, fpbhs, plot_fluxes)

    if plot_fluxes:
        flux_max = max(fluxes_max)
        #plt.ylim(1.e-10, 1.e4)
        #plt.xlim(1.e-4, 1.e0)
        plt.xlim(1.e-6, 1.e0)
        plt.ylim(flux_max/1e+15,flux_max*10.)
        plt.legend()
        plt.xlabel('$E{\\rm \,\, (GeV)}$')
        plt.ylabel('${\\rm d}F/d E \,\, ({\\rm GeV}^{-1}{\\rm s}^{-1}{\\rm cm}^{-2})$')
        plt.savefig("figures/flux_tot.pdf", bbox_inches='tight')
        plt.show()
        plt.gcf().clear()
