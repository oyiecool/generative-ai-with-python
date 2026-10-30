def read_log(args) -> dict:
    lines = Path(args.path).read_text(errors="replace").splitlines()
    errors = [l for l in lines if "ERROR" in l or "CRIT" in l]
    return {"total_lines": len(lines), "error_lines": len(errors),
            "last_errors": errors[-20:], "truncated": len(errors) > 20}
