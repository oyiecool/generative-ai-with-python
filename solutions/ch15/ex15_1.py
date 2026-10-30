def monthly_cost(req_per_day, in_tok, out_tok, p_in, p_out, cached_share=0.0,
                 p_cache_read=None, days=22):
    p_cache_read = p_in * 0.1 if p_cache_read is None else p_cache_read
    cached = in_tok * cached_share
    per_req = ((in_tok - cached) * p_in + cached * p_cache_read + out_tok * p_out) / 1e6
    return per_req * req_per_day * days

for label, p_in, p_out in (("mid-tier", 3, 15), ("small", 0.8, 4)):
    base = monthly_cost(20_000, 4000, 300, p_in, p_out)
    cached = monthly_cost(20_000, 4000, 300, p_in, p_out, cached_share=0.6)
    print(f"{label}: ${base:,.0f}/month, with caching ${cached:,.0f}/month")
