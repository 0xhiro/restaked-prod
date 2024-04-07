from django.shortcuts import render
from .services.num_pods_hist import get_num_pods
from .services.strat_breakdown import get_strat_breakdown
from .utils.charts.interpreters.tvl_hist import get_tvl_hist


def index(request):

    return render(request, 'index.html')

def dashboard(request):

    tvl_hist = get_tvl_hist()
    num_pods_hist = get_num_pods()
    strat_breakdown = get_strat_breakdown()


    context = {
        'tvl_hist': tvl_hist, 
        'num_pods_hist': num_pods_hist,
        'strat_breakdown': strat_breakdown,
    }

    return render(request, 'dashboard.html', context)