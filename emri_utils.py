
import numpy as np
import matplotlib.pyplot as plt
from lisatools.sources.emri import EMRITDIWaveform

emri_lisa = EMRITDIWaveform(T=3/52,response_kwargs=dict(tdi_chan="AET"))

m1=np.load('M_1_jillia.npy')
z=np.load('Z_jillian.npy')
m2=np.load('M_2_jillia.npy')
d_l=np.load('d_l_jillian.npy')

def adjust_emri_merger_time(parameters, target_time, tol=1e-3, max_iter=25,p_low=10,p_high=16):
    """
    Adjust the parameter 'p0' in the EMRI parameters to achieve a target merger time.
    
    Parameters:"""
    pars=dict(parameters)

    def p_func(p):
        pars=dict(parameters)
        pars['p0']=p
        a=t_dur(pars)-target_time
        return a

    p= bisection_search(p_func, p_low, p_high, tol, max_iter)

    pars['p0']=p

    return pars


def emri_waveform(parameters, axes=None,ylim=None,xlim=None, colors= ['tab:blue', 'tab:blue', 'tab:blue'] ):
    AET = run_emri(parameters)
    dt = parameters['dt']
    
    t_arr = np.arange(len(AET[0])) * dt


    if axes is None:
        fig, axes = plt.subplots(3, 1, sharex=True, gridspec_kw={'hspace': 0.0})
        if ylim is not None:
            for ax in axes:
                ax.set_ylim(ylim)
        if xlim is not None:
            for ax in axes:
                ax.set_xlim(ylim)
    
    else:
        fig = None
   
    
    labels = ['A channel', 'E channel', 'T channel']

    for i in range(3):
        axes[i].plot(t_arr, AET[i].real, color=colors[i], label=f'EMRI {labels[i]}')
        axes[i].set_ylabel('Strain')
        axes[i].legend()
        axes[i].grid(True)

    axes[-1].set_xlabel('Time [s]')
    plt.show()
    

    return fig, axes



emri_parameters = {

    'T': 2 / 52,  # duration in years
    'dt': 10.0,  # timestep in seconds
    'M': m1[1],  # primary mass
    'a': 0.0,  # spin, ignored in Schwarzschild waveform
    'mu': m2[1],  # secondary mass
    'p0': 15,  # initial semi-latus rectum
    'e0': 0,  # initial eccentricity
    'x0': 1.0,  # initial frequency param, ignored in Schwarzschild
    'qK': 0.0,  # polar spin angle
    'phiK': 0,  # azimuthal spin angle
    'qS': 0.3,  # polar sky angle
    'phiS': 0.3,  # azimuthal sky angle
    'dist': d_l[1],  # luminosity distance in Gpc
    'Phi_phi0': 0.0,  # initial phase
    'Phi_theta0': 0.0,
    'Phi_r0': 0.0,
    'dt': 10,
}

def run_emri(params):
    return emri_lisa(
        params['M'], params['mu'], params['a'], params['p0'], params['e0'], params['x0'], params['dist'],
        params['qS'], params['phiS'], params['qK'], params['phiK'],
        params['Phi_phi0'], params['Phi_theta0'], params['Phi_r0'],
        T=params['T'], dt=params['dt']
    )


def t_dur(parameters):
    AET = run_emri(parameters)
    not_z=np.argmax(AET[0][::-1]!=0)
    in_dex=len(AET[0])-not_z
    return in_dex*10

def bisection_search(f, p_low, p_high, tol=1e-6, max_iter=100):
  
    f_low = f(p_low)
    f_high = f(p_high)

    if f_low * f_high > 0:
        raise ValueError("f(p_low) and f(p_high) must have opposite signs.")

    for i in range(max_iter):
        p_mid = (p_low + p_high) / 2
        f_mid = f(p_mid)


        print(f"[{i:02d}] p_low = {p_low:.6f}, p_high = {p_high:.6f}, f_low = {f_low:.4e}, f_high = {f_high:.4e}")

        if abs(f_mid) < tol:
            return p_mid

        if f_low * f_mid < 0:
            p_high = p_mid
            f_high = f_mid
        else:
            p_low = p_mid
            f_low = f_mid

    return (p_low + p_high) / 2

def EMRI_SNR(parameters):
    AET = run_emri(parameters)
    SNR_new = []
    data = DataResidualArray(AET, dt=10)
    sens_mat = AET1SensitivityMatrix(data.f_arr, stochastic_params=(4.0 * YRSID_SI,))
    analysis = AnalysisContainer(data, sens_mat, signal_gen=emri_lisa)
    snr = analysis.snr()
    SNR_new.append(snr)

    return SNR_new
