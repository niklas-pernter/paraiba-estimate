import argparse


class Account:
    def __init__(self, value) -> None:
        self.value = value
        self.daily_balance = 0.0
        self.waiting_to_deposit = 0.0


class SubAccount(Account):
    def __init__(self, value, id) -> None:
        super().__init__(value)
        self.id = id


class FirstLine(Account):
    def __init__(self, value) -> None:
        super().__init__(value)


class Color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


class ParaibaEstimate:
    def __init__(self, num_of_subaccounts, firstline_balance, percent, days_to_run) -> None:
        self.number_of_subaccounts = num_of_subaccounts
        self.firstline = FirstLine(firstline_balance)
        self.percent = percent
        self.initial_investment = 0.0
        self.days_to_run = days_to_run
        self.sub_accounts = []
        for i in range(1, num_of_subaccounts+1):
            value = float(input("Value of Sub-Account #{0}: ".format(i)) or 100)
            self.sub_accounts.append(SubAccount(value, i))
            self.initial_investment += value
        self.initial_investment += firstline_balance


    def estimate(self):
        for _ in range(1, int((self.days_to_run / 7)+1)):
            for i in range(1, 4+1):
                self.add_interest_to_firstline_account()
                self.add_interest_to_subaccounts()
                if self.firstline.daily_balance >= 25: self.deposit_to_firstline()
                elif i % 4 == 0:
                    if self.firstline.waiting_to_deposit >= 25: self.deposit_to_firstline()
                for account in self.sub_accounts:
                    if account.daily_balance >= 25: self.deposit_from_sub_account_to_firstline(account)
                    elif account.waiting_to_deposit >= 25: self.deposit_from_sub_account_to_firstline(account)

        
    def add_interest_to_firstline_account(self):
        daily_interest = self.get_deposit_bonus(self.firstline.value) + self.get_firstline_bonus() + self.get_downline_bonus()
        self.firstline.daily_balance = daily_interest
        self.firstline.waiting_to_deposit += daily_interest
    

    def add_interest_to_subaccounts(self):
        for account in self.sub_accounts:
            daily_interest = self.get_deposit_bonus(account.value)
            account.daily_balance = daily_interest
            account.waiting_to_deposit += daily_interest


    def get_firstline_bonus(self):
        return sum(e.value for e in self.sub_accounts) * self.percent


    def get_deposit_bonus(self, balance):
        return balance * self.percent


    def get_downline_bonus(self):
        return 0.001 if self.firstline.value > 1000 else 0.0


    def deposit_to_firstline(self):
        self.firstline.value += self.firstline.waiting_to_deposit
        self.firstline.waiting_to_deposit = 0.0
        self.firstline.daily_balance = 0.0
    

    def deposit_from_sub_account_to_firstline(self, account):
        self.firstline.value += account.waiting_to_deposit
        account.waiting_to_deposit = 0.0
        account.daily_balance = 0.0


    def print_summary(self):
        total_investment = self.firstline.value + sum(a.value for a in self.sub_accounts)
        total_waiting_to_deposit = self.firstline.waiting_to_deposit + sum(a.waiting_to_deposit for a in self.sub_accounts)
        print("\nSummary")

        print("\tFirstline")
        print("\t\t↳ Value: {}$".format(round(self.firstline.value, 2)))
        print("\t\t↳ Waiting to deposit: {}$".format(round(self.firstline.waiting_to_deposit, 2)))

        print("\tTotal Investment")
        print("\t\t↳ Value: {}$".format(round(total_investment, 2)))
        print("\t\t↳ Initial investment: {}$".format(round(self.initial_investment, 2)))
        print("\t\t↳ Total waiting to deposit: {}$".format(round(total_waiting_to_deposit, 2)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("-a", "--subaccounts", type=int, default=20, help="Default 20")
    parser.add_argument("-f", "--firstline-balance", type=float, default=1000)
    parser.add_argument("-p", "--percent", type=float, default=0.003, help="Default 0.3")
    parser.add_argument("-d", "--days", type=int, default=365, help="Default 365 days")

    args = parser.parse_args()

    calc = ParaibaEstimate(args.subaccounts, args.firstline_balance, args.percent, args.days)
    calc.estimate()
    calc.print_summary()
    
