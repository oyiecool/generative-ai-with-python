def workflow_report() -> str:
    results = [ping_host(h) for h in HOSTS] + \
              [check_port(h, p) for h, p in sorted(PORTS)] + \
              [service_status(s) for s in sorted(SERVICES)] + [local_health()]
    r = ollama.chat(model="qwen2.5:1.5b", options={"temperature": 0}, messages=[
        {"role": "system", "content": "Summarise these check results as Markdown with sections OK, "
                                      "Problems, Suggested next steps. Use only these results."},
        {"role": "user", "content": "\n".join(results)}])
    return r.message.content
