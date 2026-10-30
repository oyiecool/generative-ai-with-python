def ask_operator(name: str, args: dict) -> bool:
    print(f"\nAgent wants to run {name} with {args}")
    return input("Approve? [y/N] ").strip().lower() == "y"
