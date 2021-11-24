import argparse
import datetime
import re

class Account:
    def __init__(self, initial, value, percent=0.3) -> None:
        self.initial = initial
        self.value = value
        self.daily_balance = 0.0
        self.waiting_to_deposit = 0.0
        self.percent = percent


    def deposit(self):
        self.value += self.waiting_to_deposit
        self.waiting_to_deposit = 0


    def deposit_with_amount(self, amount):
        self.value += amount
        self.waiting_to_deposit = 0


    def get_downline_bonus(self):
        return 0.001 if self.value > 1000 else 0.0


    def get_deposit_bonus(self):
        return self.value * self.percent


class SubAccount(Account):
    def __init__(self, initial, value, id, percent) -> None:
        super().__init__(initial, value, percent)
        self.id = id


    def add_interest(self):
        self.waiting_to_deposit += self.get_deposit_bonus()
        self.daily_balance = self.get_deposit_bonus()


class PrimaryAccount(Account):
    def __init__(self, initial, value, sub_accounts, percent) -> None:
        super().__init__(initial, value, percent)
        self.sub_accounts = sub_accounts


    def get_firstline_bonus(self):
        return sum(e.value for e in self.sub_accounts) * self.percent


    def add_interest(self):
        interest = self.get_deposit_bonus() + self.get_firstline_bonus() + self.get_downline_bonus()
        self.waiting_to_deposit += interest
        self.daily_balance = interest


    def add_interest_to_subaccounts(self):
        for account in self.sub_accounts: account.add_interest()


    def deposit_from_subaccount_to_firstline(self, account):
        self.deposit_with_amount(account.waiting_to_deposit)
        account.waiting_to_deposit = 0

        
class ParaibaEstimate:
    def __init__(self, num_of_subaccounts, firstline_balance, percent, days_to_run, output, till_balance) -> None:
        self.initial_investment = 0.0
        self.days_to_run = days_to_run
        self.output = output
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
            sub_accounts.append(SubAccount(value, value, i, percent))
            self.initial_investment += value
                
        self.initial_investment += firstline_balance
        self.primary_account = PrimaryAccount(firstline_balance, firstline_balance, sub_accounts, percent)


    def estimate(self):
        self.weeks = int(self.days_to_run / 7)
        for _ in range(1, self.weeks+1):
            for i in range(1, 4+1):
                self.add_interest_for_day(i)


    def estimate_weeks_till_value(self):
        running = True
        week = 0
        while running:
            for i in range(1, 4+1):
                self.add_interest_for_day(i)
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
        months = self.weeks / 7
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
        if(self.output):
            f = open("paraiba_estimates_{}.txt".format(datetime.datetime.now().strftime("%Y%m%d%H%M%S")), "x")
            f.write(output)
            f.close
        input("Press enter to exit...")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("-a", "--subaccounts", type=str, default="20", help="add = with number to set default for all account example: 20=100")
    parser.add_argument("-f", "--firstline-balance", type=float, default=1000, help="Default is 1000")
    parser.add_argument("-p", "--percent", type=float, default=0.003, help="Default 0.3")
    parser.add_argument("-d", "--days", type=int, default=365, help="Default 365 days")
    parser.add_argument("-o", "--output", type=bool, default=False, help="Output to file")
    parser.add_argument("-b", "--till-balance", type=float, help="Weeks until balance equals to input")

    args = parser.parse_args()

    calc = ParaibaEstimate(args.subaccounts, args.firstline_balance, args.percent, args.days, args.output, args.till_balance)

    if args.till_balance is not None:
        if args.till_balance > 0.0: calc.estimate_weeks_till_value()
    else: calc.estimate()
    calc.print_summary()
