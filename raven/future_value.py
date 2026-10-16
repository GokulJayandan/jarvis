"""Training-derived, finite-horizon information value, not observed future supply."""
from .probabilities import assets

def future_value(member,day):
    model=assets()['future']
    remaining=sum(count for d,count in model['arrivals'].items() if day<int(d)<60)
    if not remaining: return 0.0
    same_zone=model['zone_frequency'].get(member['zone'],model['rare_zone_frequency'])
    remaining_horizon=max(0,59-day)
    # Shrink expected opportunities; prevents large groups dominating all asks.
    supply=remaining*same_zone*model['reciprocal_rate']
    survival=0.97**min(10,remaining_horizon)
    return min(1,supply)*model['outcome_prior']*survival*(remaining_horizon/59)
