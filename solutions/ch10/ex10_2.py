import sqlite3
from datetime import date


class DailyBudget:
    def __init__(self, path="data/spend.db", limit_usd=5.0):
        self.db, self.limit = sqlite3.connect(path), limit_usd
        self.db.execute("CREATE TABLE IF NOT EXISTS spend (day TEXT, usd REAL)")

    def spent_today(self) -> float:
        row = self.db.execute("SELECT COALESCE(SUM(usd),0) FROM spend WHERE day=?",
                              (date.today().isoformat(),)).fetchone()
        return row[0]

    def record(self, usd: float) -> None:
        self.db.execute("INSERT INTO spend VALUES (?,?)", (date.today().isoformat(), usd))
        self.db.commit()

    def check(self) -> None:
        if self.spent_today() >= self.limit:
            raise RuntimeError("daily AI budget exhausted")
