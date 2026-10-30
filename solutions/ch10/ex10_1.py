from aikit.agent import Agent, Budget, Tool

tools = [
    Tool("disk_usage", "Show disk usage for an allowed path.", DiskUsageArgs, disk_usage),
    Tool("service_status", "Check whether a systemd service is active.", ServiceStatusArgs, service_status),
]
agent = Agent(model=s.chat_model, system="You are a read-only server diagnostics assistant.",
              tools=tools, budget=Budget(max_steps=6))
answer, trace = agent.run("Is nginx running, and is /var close to full?")
print(answer)
for e in trace.events:
    print(e)
