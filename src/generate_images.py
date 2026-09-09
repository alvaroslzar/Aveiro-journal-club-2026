import os
import numpy as np
from matplotlib import pyplot as plt
from gravityp import *


script_dir = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.abspath(os.path.join(script_dir, "..", "latex", "figures"))

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def make_directories():
    dirs = [
        os.path.abspath(os.path.join(OUTPUT_DIR, "SV")),
        os.path.abspath(os.path.join(OUTPUT_DIR, "SV", "ray_tracing")),
        os.path.abspath(os.path.join(OUTPUT_DIR, "SV", "shadows")),
        os.path.abspath(os.path.join(OUTPUT_DIR, "SV", "transfer_function")),
        os.path.abspath(os.path.join(OUTPUT_DIR, "Hayward")),
        os.path.abspath(os.path.join(OUTPUT_DIR, "Hayward", "ray_tracing")),
        os.path.abspath(os.path.join(OUTPUT_DIR, "Hayward", "shadows")),
        os.path.abspath(os.path.join(OUTPUT_DIR, "Hayward", "transfer_function")),
    ]
    for dir in dirs:
        os.makedirs(dir, exist_ok=True)

# # Matplotlib style
# plt.style.use("paper.mplstyle")
pt = 1./72.27 # Hundreds of years of history... 72.27 points to an inch.
jour_sizes = {"PRD": {"onecol": 246.*pt, "twocol": 510.*pt},
            "CQG": {"onecol": 374.*pt}, # CQG is only one column
            # Add more journals below. Can add more properties to each journal
            }
my_width = jour_sizes["PRD"]["twocol"]
golden = (1 + 5**0.5)/2 # Our figure's aspect ratio
# figsize = (my_width, my_width/golden)


### Emission profiles ###

def compute_inner_edge_SV(r_throat):
    """Inner edge for SV metric, for which g_tt(r)=0"""
    func = lambda x: np.sqrt(4.-x**2)
    return np.piecewise(r_throat, [r_throat<=2.,r_throat>2.] , [func, 0] )

def compute_inner_edge_Hayward(gamma):
    """Inner edge for SV metric, for which g_tt(r)=0."""
    # NOTE: This is the exterior horizon
    gamma_crit = 4*np.sqrt(3)/9
    func = lambda x: 2/3 + (4/3)*np.cos( (1/3)*np.arccos(1-27*x**2/8) )
    return float(np.piecewise(gamma, [gamma <= gamma_crit , gamma > gamma_crit] , [func, 0] ))

def generate_intensity_profiles():
    width = my_width*0.48
    figsize = (width,width/golden)
    savepath = os.path.abspath(os.path.join(OUTPUT_DIR, "Emission_models.pdf"))
    rs = np.linspace(0,13,1000)
    peaks = {
        'SV BH': compute_inner_edge_SV(3/2), 
        'Hayward BH': compute_inner_edge_Hayward(0.5),
        'Wormholes': 0
    }
    fig, ax = plt.subplots(figsize=figsize)
    for label, mu in peaks.items():
        params = (mu, 1/2, -2) # For small sigma it gives numerical error
        emission_model = lambda r: normalized_Standard_Unbound(r, *params)
        ax.plot(rs, emission_model(rs), label=label)
    rmin = round(rs.min())
    rmax = round(rs.max())
    ax.set_xlabel(r'$r/M$')
    ax.set_xlim(rmin,rmax)
    ax.set_xticks(np.arange(0,13,2))
    ax.set_ylabel(r'$I_\mathrm{em}/I_0$')
    ax.set_ylim(0,1)
    ax.legend()
    if savepath is not None:
        plt.savefig(savepath, format='pdf')


### Simpson-Visser ###

def plot_potential_SV(ax, rr, f_SV, areal_radius2, r_throat, xi_t, label, linestyle):
    kwargs_SV = {
        'radial_fun': f_SV,
        'radial_params': (r_throat,),
        'areal': areal_radius2,
        'areal_params': (r_throat, xi_t)
    }
    ax.plot(rr, potential(rr, **kwargs_SV), label=label, linestyle=linestyle)

def make_potential_plot_SV(rr, f_SV, areal_radius2, r_throats, xi_ts, linestyles,
                        figsize=(7,7), savepath=None):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize, sharey=True)

    for i, xi_t in enumerate(xi_ts):
        label = r'$\Xi/M=$'+f' {xi_t}'
        plot_potential_SV(ax1, rr, f_SV, areal_radius2, r_throats[0], xi_t, label, linestyles[i])
        plot_potential_SV(ax2, rr, f_SV, areal_radius2, r_throats[1], xi_t, None, linestyles[i])

    ax1.set_ylabel(r'$V(r)/M^2$')
    ax1.text(-12, 0.08, s=r'$r_{\mathrm{throat}}=1.5M$')
    ax2.text(-12, 0.08, s=r'$r_{\mathrm{throat}}=2.5M$')
    for ax in [ax1,ax2]:
        ax.set_xlim( int(rr.min()) , int(rr.max()) )
        ax.set_ylim(0,0.1)
        ax.set_xlabel(r'$r/M$')

    handles, labels = ax1.get_legend_handles_labels()

    fig.legend(handles, labels, loc='upper center', bbox_to_anchor=(0.53, 1.1),
            ncol=4, frameon=True)
    plt.tight_layout()
    if savepath is not None:
        plt.savefig(savepath, format='pdf')

def generate_SV():

    def f_SV(r: float, r_throat: float) -> float:
        """Radial function e^{2nu} of the Simpson-Visser metric in units of M=1"""
        return 1 - 2./np.sqrt(r**2+r_throat**2)

    def areal_radius2(r: float, r_throat: float, xi_t: float) -> float:
        """areal radius squared e^{2xi} of a wormhole in units of M=1"""
        return ( np.sqrt(r**2+r_throat**2) + xi_t )**2

    def compute_photon_rings_SV(r_throat, xi_t):
        """Compute the coordinate r of the photon ring for the SV metric"""
        # We define x^2 = r^2 + r_throat^2
        p_ring_x = np.sqrt( 9/2 + xi_t + 3*np.sqrt(9/4+xi_t) ) # Value of x at the photon ring
        func = lambda r: np.sqrt( p_ring_x**2 - r**2 ) # Position of the photon ring for the r coordinate
        return [ np.piecewise(r_throat, [ r_throat<=p_ring_x , r_throat>p_ring_x ] , [func, 0] ) ]

    def compute_b_crits_SV(xi_t):
        """Compute the critical impact paremeter of a non stationary SV wormhole"""
        radical = np.sqrt(9+4*xi_t)
        return [ 0.5 * np.sqrt( 18*(3+radical)+4*xi_t*( 9+xi_t+2*radical ) ) ]

    def get_SV_kwargs(r_throat, xi_t):
        # TODO: Dar la posibilidad de que radial_fun y areal puedan no tener parámetros
        return {
        'r_phs': compute_photon_rings_SV(r_throat, xi_t),
        'inner_edge': compute_inner_edge_SV(r_throat),
        'radial_fun': f_SV,
        'radial_params': (r_throat,),
        'areal': areal_radius2,
        'areal_params': (r_throat, xi_t)
        }

    # Potential
    figsize = (my_width,my_width/3)
    savepath=None
    savepath = os.path.abspath(os.path.join(OUTPUT_DIR, "SV", "SV_potential.pdf"))
    rr = np.linspace(-14,14,200)
    r_throats = [3/2,5/2,]
    xi_ts = [-1,0,1]
    linestyles = [ '--' , '-.' , '-' ]
    make_potential_plot_SV(rr, f_SV, areal_radius2, r_throats, xi_ts, linestyles,
                        figsize=figsize, savepath=savepath)

    # Ray tracing
    steps = (0.3,0.07,0.01)
    width = my_width*0.48*2/3
    r_throats = [3/2,5/2]
    xi_ts = [-1,0,1]
    for r_throat in r_throats:
        for xi_t in xi_ts:
            b_crits = compute_b_crits_SV(xi_t) # Note that compute_b_crits_SV returns a list
            SV_kwargs = get_SV_kwargs(r_throat, xi_t)
            rings_SV = find_rings_list(b_crits, SV_kwargs)

            inner_shadow = compute_inner_shadow(0,10,**SV_kwargs)
            bs_direct, bs_lensed, bs_p_ring = compute_optimal_array_steps(inner_shadow, 10, rings_SV, steps, joint=False)
            bs = {
                'inner_shadow': ('black', np.arange(0, inner_shadow, steps[0])),
                'direct': ('dodgerblue', bs_direct),
                'lensed': ('orange', bs_lensed),
                'p_ring': ('red', bs_p_ring[~np.isin(bs_p_ring,b_crits)]), # We remove the value b_crit
            }
            savepath = os.path.abspath(os.path.join(OUTPUT_DIR, f"SV/ray_tracing/RT_SV_r{int(r_throat)}_xi{round(xi_t)}.pdf"))
            make_geodesics_plot(bs, figsize=(width,width), savepath=savepath,
                                **SV_kwargs)

    # Transfer functions
    width = my_width*0.48*2/3
    r_throats = [3/2,5/2]
    xi_ts = [-1,0,1]
    for r_throat in r_throats:
        for xi_t in xi_ts:
            b_crits = compute_b_crits_SV(xi_t)
            SV_kwargs = get_SV_kwargs(r_throat, xi_t)
            rings_SV = find_rings_list(b_crits, SV_kwargs)
            bs_list = compute_optimal_array_Npoints(0,10, rings_SV, Npoints=50, joint=False, fill=True)
            for bs in bs_list:
                bs = bs[~np.isin(bs,b_crits)]

            savepath = os.path.abspath(os.path.join(OUTPUT_DIR, f"SV/transfer_function/TF_SV_r{int(r_throat)}_xi{round(xi_t)}.pdf"))
            make_transfer_function_plot(b_crits, SV_kwargs, bs_list,
                                        correction=0, figsize=(width,width), savepath=savepath)

    # Observed intensity and shadow
    y_range = (0,0.34)
    width = my_width*0.48*2/3
    figsize = (width,width)
    savepath = None
    bs = np.linspace(0,10*np.sqrt(2),1000)
    r_throats = [3/2,5/2]
    xi_ts = [-1,0,1]
    for r_throat in r_throats:
        for xi_t in xi_ts:
            b_crits = compute_b_crits_SV(xi_t)
            SV_kwargs = get_SV_kwargs(r_throat, xi_t)
            r_hor = SV_kwargs['inner_edge']
            rings_SV = find_rings_list(b_crits, SV_kwargs)
            bs_transfer_list = compute_optimal_array_Npoints(0,10*np.sqrt(2), rings_SV, Npoints=100, joint=False, fill=True)
            params = (r_hor, 1/2, -2) # For small sigma it gives numerical error
            emission_model = lambda r: normalized_Standard_Unbound(r, *params)
            savepath = os.path.abspath(os.path.join(OUTPUT_DIR, f"SV/shadows/Observed_SV_r{int(r_throat)}_xi{round(xi_t)}.pdf"))
            plot_observed_intensity(bs, bs_transfer_list, emission_model, SV_kwargs,
                                    figsize, savepath=savepath, y_range=y_range)
            
            savepath = os.path.abspath(os.path.join(OUTPUT_DIR, f"SV/shadows/Sh_SV_r{int(r_throat)}_xi{round(xi_t)}.pdf"))
            figsize = (width/1.05,width/1.05)
            make_shadow_plot(bs_transfer_list, emission_model, SV_kwargs,
                            figsize, savepath=savepath, y_range=y_range)
            figsize = (width,width)

# Generate all plots
def main():
    make_directories()
    generate_intensity_profiles()
    generate_SV()


if __name__=='__main__':
    main()