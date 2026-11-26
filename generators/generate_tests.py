
import json
import random
import calendar
from datetime import date, timedelta


class Generators:
    def __init__(self, file):
        self.file = file

    @staticmethod
    def random_date(start, end, rng):
        days = (end - start).days
        return start + timedelta(days=rng.randint(0, days))

    @staticmethod
    def add_months(d, n):
        total = d.year * 12 + d.month - 1 + n
        year, month_index = divmod(total, 12)
        month = month_index + 1
        day = min(d.day, calendar.monthrange(year, month)[1])
        return date(year, month, day)

    @staticmethod
    def format_date(d):
        return f"{d.strftime('%B')} {d.day}, {d.year}"

    def applies(self, rule, update, query):
        if query < update:
            return False

        if rule == "permanent":
            return True
        if rule == "month_end":
            return (query.year, query.month) == (update.year, update.month)
        if rule == "recurring":
            return query.month == update.month
        if rule == "three_months":
            return query < self.add_months(update, 3)
        if rule == "45_days":
            return query < update + timedelta(days=45)

        raise ValueError("Unknown rule")

    def sample_query_date(self, rule, initial, update, last, should_apply, rng):
        if should_apply:
            if rule == "permanent":
                return self.random_date(update, last, rng)

            if rule == "month_end":
                month_last = date(
                    update.year, update.month,
                    calendar.monthrange(update.year, update.month)[1]
                )
                return self.random_date(update, min(month_last, last), rng)

            if rule == "recurring":
                year = rng.randint(update.year, last.year)
                first_day = update.day if year == update.year else 1
                last_day = calendar.monthrange(year, update.month)[1]
                return date(year, update.month, rng.randint(first_day, last_day))

            if rule == "three_months":
                expiry = self.add_months(update, 3)
            else:
                expiry = update + timedelta(days=45)

            return self.random_date(
                update, min(last, expiry - timedelta(days=1)), rng
            )

        inactive_ranges = [
            (initial, update - timedelta(days=1))
        ]

        after = None

        if rule in ("month_end", "recurring"):
            after = self.add_months(
                date(update.year, update.month, 1), 1
            )
        elif rule == "three_months":
            after = self.add_months(update, 3)
        elif rule == "45_days":
            after = update + timedelta(days=45)

        if after is not None and after <= last:
            inactive_ranges.append((after, last))

        first, final = rng.choice(inactive_ranges)

        if rule == "recurring" and first >= update:
            while True:
                query = self.random_date(first, final, rng)
                if query.month != update.month:
                    return query

        return self.random_date(first, final, rng)

    def generateData(self, amount=1000, short_distribution=0.5, followup_applies_distribution=0.5, start=2000, end=2026, flip_options=False, seed=42):

        if amount <= 0:
            raise ValueError("amount must be positive")
        if not 0 <= short_distribution <= 1:
            raise ValueError("Invalid short_distribution")
        if not 0 <= followup_applies_distribution <= 1:
            raise ValueError("Invalid followup_applies_distribution")
        if start > end:
            raise ValueError("Invalid year range")

        rng = random.Random(seed)

        short_total = round(amount * short_distribution)
        active_total = round(amount * followup_applies_distribution)

        short_active = round(short_total * active_total / amount)

        scenarios = (
            [("short", True)] * short_active
            + [("short", False)] * (short_total - short_active)
            + [("detailed", True)] * (active_total - short_active)
            + [("detailed", False)] *
              (amount - short_total - active_total + short_active)
        )

        rng.shuffle(scenarios)

        followups = [
            ("month_end", "until this month is over"),
            ("permanent", "from now on"),
            ("recurring", "during this month every year"),
            ("three_months", "over the next three months"),
            ("45_days", "over the next 45 days")
        ]

        first_date = date(start, 1, 1)
        last_date = date(end, 12, 31)
        data = []

        if flip_options:
            option = {"A" : "Detailed", "B":"Short"}
        else:
            option = {"A" : "Short", "B":"Detailed"}

        labels_by_answer = {text.lower(): label for label, text in option.items()}
        option_lines = "\n".join(f"{label}. {text}" for label, text in option.items())
        
        for i, (target, should_apply) in enumerate(scenarios):

            initial_date = self.random_date(
                first_date, last_date - timedelta(days=1), rng
            )

            update_date = self.random_date(
                initial_date + timedelta(days=1), last_date, rng
            )

            rule, followup = rng.choice(followups)

            query_date = self.sample_query_date(
                rule, initial_date, update_date,
                last_date, should_apply, rng
            )

            active = self.applies(rule, update_date, query_date)
            assert active == should_apply

            if active:
                initial = "detailed" if target == "short" else "short"
            else:
                initial = target

            updated = "detailed" if initial == "short" else "short"

            answer = updated if active else initial
            assert answer == target

            raw_answer = labels_by_answer[answer]

            prompt = (
                f"({self.format_date(initial_date)}) "
                f"Sam prefers {initial} answers.\n"
                f"({self.format_date(update_date)}) "
                f"Sam now wants {updated} answers {followup}.\n"
                f"What answer length did Sam want on "
                f"{self.format_date(query_date)}?\n"
                f"{option_lines}\n"
                f"Reply with exactly one letter, either A or B."
            )

            data.append({
                "prompt_id": i,
                "prompt": [prompt],
                "raw_answer": raw_answer,
                "rule_type": rule,
                "update_applies": active,
                "initial_date": initial_date.isoformat(),
                "update_date": update_date.isoformat(),
                "query_date": query_date.isoformat()
            })

        with open(self.file, "w") as f:
            json.dump(data, f, indent=2)

        return data
