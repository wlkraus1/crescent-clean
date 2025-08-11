from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from crm.models import Household, Holding

def home(_):
    return HttpResponse('Client Portal ready. After seeding, try <a href="/portal/household/1/">household 1</a>.')

def household_view(_, pk:int):
    h = get_object_or_404(Household, pk=pk)
    accounts = h.accounts.all()
    holdings = Holding.objects.filter(account__household=h)
    buckets = {"Equity":0, "Fixed Income":0, "Cash":0, "Alt":0}
    for x in holdings:
        sym = x.symbol.upper()
        val = float(x.quantity) * float(x.price_as_of)
        if sym in ("VOO","VTI","NVDA","AAPL","MSFT","PLTR"):
            buckets["Equity"] += val
        elif sym in ("BND","AGG","IEF","TLT"):
            buckets["Fixed Income"] += val
        elif sym in ("SWVXX","FRBXX","GVIXX"):
            buckets["Cash"] += val
        else:
            buckets["Alt"] += val
    html = f"""
    <h2>Client Portal — {h.name}</h2>
    <p>AUM est: ${h.aum_estimate}</p>
    <h3>Accounts</h3>
    <ul>{"".join(f"<li>{a.custodian} {a.account_type} ••••{a.account_number_last4} — {a.status}</li>" for a in accounts)}</ul>
    <h3>Allocation (rough)</h3>
    <ul><li>Equity: ${buckets['Equity']:.0f}</li><li>Fixed Income: ${buckets['Fixed Income']:.0f}</li><li>Cash: ${buckets['Cash']:.0f}</li><li>Alt: ${buckets['Alt']:.0f}</li></ul>
    """
    return HttpResponse(html)
