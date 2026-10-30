# uv add redis
import json

import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)
TTL = 24 * 3600
hits = misses = 0


def cached_answer(question, user_groups, kb_version):
    global hits, misses
    key = "ans:" + cache_key("rag_answer", 3, s.chat_model, user_groups, question, kb_version)
    if (val := r.get(key)) is not None:
        hits += 1
        return json.loads(val)
    misses += 1
    result = answer(question, index, llm, user_groups)
    if result["answerable"]:                    # never cache refusals caused by transient errors
        r.setex(key, TTL, json.dumps(result))
    return result
