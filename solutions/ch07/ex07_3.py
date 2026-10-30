import getpass
import logging

audit = logging.getLogger("audit")


class RestartArgs(BaseModel):
    name: str = Field(pattern=r"^[a-zA-Z0-9_.@-]+$")


RESTARTABLE = {"nginx", "app-worker"}


def restart_service(args: RestartArgs) -> dict:
    if args.name not in RESTARTABLE:
        return {"error": "service not on the restart allow-list"}
    answer = input(f"Agent requests restart of {args.name}. Type the service name to confirm: ")
    approver = getpass.getuser()
    if answer.strip() != args.name:
        audit.info("restart denied", extra={"service": args.name, "approver": approver})
        return {"error": "not approved"}
    out = subprocess.run(["sudo", "systemctl", "restart", args.name],
                         capture_output=True, text=True, timeout=30)
    audit.info("restart executed", extra={"service": args.name, "approver": approver,
                                          "rc": out.returncode})
    return {"ok": out.returncode == 0}
