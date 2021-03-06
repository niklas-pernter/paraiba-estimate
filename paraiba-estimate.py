import argparse
import re

class Account:
    def __init__(self, initial, value, sub_accounts=[], pool_bonus=0.0) -> None:
        self.initial = initial
        self.value = value
        self.daily_balance = 0.0
        self.waiting_to_deposit = 0.0
        self.sub_accounts = sub_accounts
        self.pool_bonus = pool_bonus

    def deposit(self):
        self.value += self.waiting_to_deposit
        self.waiting_to_deposit = 0


    def deposit_with_amount(self, amount):
        self.value += amount
        self.waiting_to_deposit = 0


    def get_downline_bonus(self):
        return 0.001 if self.value > 1000 else 0.0


    def get_firstline_bonus(self):
        return sum(a.value for a in self.sub_accounts) * self.get_deposit_bonus()


    def get_downline_bonus(self):
        return 0.0
        # TODO
        if self.value >= 1000:
            if len(self.sub_accounts) <= 4: 
                return 0.0001
            elif len(self.sub_accounts) <= 9: 
                return 0.002
            elif len(self.sub_accounts) <= 19: 
                return 0.003
            else: return 0.004

    def add_interest_to_subaccounts(self):
        for account in self.sub_accounts: account.add_interest()

    def get_deposit_bonus(self):
        if self.value >= 100:
            if len(self.sub_accounts) <= 4: return 0.0005
            elif len(self.sub_accounts) <= 9: return 0.001
            elif len(self.sub_accounts) <= 19: return 0.002
            else: return 0.003


class SubAccount(Account):
    def __init__(self, initial, value, id, num_of_subaccounts) -> None:
        super().__init__(initial, value, [0] * num_of_subaccounts)
        self.id = id

    def add_interest(self):
        interest = self.value * self.get_deposit_bonus() + self.pool_bonus
        self.waiting_to_deposit += interest
        self.daily_balance = interest


class PrimaryAccount(Account):
    def __init__(self, initial, value, sub_accounts, pool_bonus) -> None:
        super().__init__(initial, value, sub_accounts, pool_bonus)

    def add_interest(self):
        deposit_bonus = self.value * self.get_deposit_bonus()
        fistline_bonus = self.get_firstline_bonus()
        downline_bonus = self.value * self.get_downline_bonus()
        interest = deposit_bonus + fistline_bonus + downline_bonus + self.pool_bonus
        self.waiting_to_deposit += interest
        self.daily_balance = interest

    def deposit_from_subaccount_to_firstline(self, account):
        self.deposit_with_amount(account.waiting_to_deposit)
        account.waiting_to_deposit = 0

        
class ParaibaEstimate:
    def __init__(self, num_of_subaccounts, firstline_balance, days_to_run, till_balance, pool_bonus) -> None:
        self.initial_investment = 0.0
        self.days_to_run = days_to_run
        self.weeks_till_balance_value = till_balance
        self.weeks_till_balance_week = 0
        self.weeks = 0

        num_of_subaccounts_regex_search = re.search(r"([0-9]+)=?([0-9]+)?", num_of_subaccounts)
        num_of_subaccounts = int(num_of_subaccounts_regex_search.group(1))
        
        default_value = num_of_subaccounts_regex_search.group(2) 
        num_of_subaccounts_default_values = default_value if default_value is not None else 100 

        sub_accounts = []
        for i in range(1, num_of_subaccounts+1):
            value = float(num_of_subaccounts_default_values)
            if default_value is None:
                value = float(input("Value of Sub-Account #{0}: ".format(i)) or 100)
            sub_accounts.append(SubAccount(value, value, i, num_of_subaccounts))
            self.initial_investment += value
                
        self.initial_investment += firstline_balance
        self.primary_account = PrimaryAccount(firstline_balance, firstline_balance, sub_accounts, pool_bonus)


    def estimate(self):
        self.weeks = int(self.days_to_run / 7)
        for _ in range(1, self.weeks+1):
            for i in range(1, 4+1): self.add_interest_for_day(i)


    def estimate_weeks_till_value(self):
        running = True
        week = 0
        while running:
            for i in range(1, 4+1): self.add_interest_for_day(i)
            week += 1
            if self.primary_account.value > self.weeks_till_balance_value:
                self.weeks = week
                running = False


    def add_interest_for_day(self, i):
        self.primary_account.add_interest()
        self.primary_account.add_interest_to_subaccounts()
        if self.primary_account.daily_balance >= 25: self.primary_account.deposit()
        elif i % 4 == 0:
            if self.primary_account.waiting_to_deposit >= 25: self.primary_account.deposit()
        for account in self.primary_account.sub_accounts:
            if account.daily_balance >= 25: self.primary_account.deposit_from_subaccount_to_firstline(account)
            elif account.waiting_to_deposit >= 25: self.primary_account.deposit_from_subaccount_to_firstline(account)


    def print_balance_after_week(self, weeks):
        week_text = "week" if weeks == 1 else "weeks"
        month_text = "month" if int(weeks/4) == 1 else "months"
        print(str("{0}$ -> {1}$ after {2} {3} ({4} {5})".format(
            self.primary_account.initial, 
            self.weeks_till_balance_value, 
            weeks, 
            week_text, 
            int(weeks/7), 
            month_text)
            ))


    def print_summary(self):
        total_investment = self.primary_account.value + sum(a.value for a in self.primary_account.sub_accounts)
        total_waiting_to_deposit = self.primary_account.waiting_to_deposit + sum(a.waiting_to_deposit for a in self.primary_account.sub_accounts)
        months = self.weeks / 4
        years = months / 12

        output = """Estimated summary after {0} weeks or {1} months or {2} years

            Firstline
                - Value: {3}$
                - Waiting to deposit: {4}$
                
                - Daily interest: {5}$
                - Weekly interest: {6}$
                - Monthly interest: {7}$

            Total Investment
                - Value: {8}$
                - Initial investment: {9}$
                - Total waiting to deposit: {10}$
                - After inflation (1.2% after {11} years): {12}$
                """.format(
            str(self.weeks),
            str(round(months, 2)),
            str(round(years, 2)),
            str(f"{round(self.primary_account.value, 2):,}"),
            str(f"{round(self.primary_account.waiting_to_deposit, 2):,}"),
            str(f"{round(self.primary_account.daily_balance, 2):,}"),
            str(f"{round(self.primary_account.daily_balance*4, 2):,}"),
            str(f"{round(self.primary_account.daily_balance*16, 2):,}"),

            str(f"{round(total_investment, 2):,}"),
            str(f"{round(self.initial_investment, 2):,}"),
            str(f"{round(total_waiting_to_deposit, 2):,}"),
            str(round(years, 2)),
            str(f"{round(total_investment - (total_investment * (0.012 * years)), 2):,}")
        )
    
        print("\n" + output)
        input("Press enter to exit...")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("-a", "--subaccounts", type=str, default="20", help="add = with number to set default for all account example: 20=100")
    parser.add_argument("-f", "--firstline-balance", type=float, default=1077, help="Default is 1000")
    parser.add_argument("-d", "--days", type=int, default=365, help="Default 365 days")
    parser.add_argument("-b", "--till-balance", type=float, help="Weeks until balance equals to input")
    parser.add_argument("-p", "--pool-bonus", type=float, help="Pool bonus (read from Dashboard)")

    args = parser.parse_args()

    calc = ParaibaEstimate(args.subaccounts, args.firstline_balance, args.days, args.till_balance, args.pool_bonus)

    if args.till_balance is not None:
        if args.till_balance > 0.0: calc.estimate_weeks_till_value()
    else: calc.estimate()
    calc.print_summary()
