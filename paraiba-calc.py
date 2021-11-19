import argparse



class Account():
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


class ParaibaCalculator:

    def __init__(self):
        self.number_of_days_to_run = 0
        self.always_reinvest_on_sundays = True
        self.percent = 0.003
        self.always_reinvest_if_possible = False

        self.initial_investment = 0.0

        self.subaccounts = []
        self.firstline = None

    def parse_args(self, args):
        self.number_of_days_to_run = args.days
        self.percent = args.percent
        self.always_reinvest_on_sundays = args.always_reinvest_sunday
        self.always_reinvest_if_possible = args.always_reinvest
        self.number_of_subaccounts = args.subaccounts
        self.firstline = FirstLine(args.firstline_balance) 
        for i in range(1, args.subaccounts+1):
            balance = float(input(("Value of Account #{0}: ".format(i))) or 100.0)
            self.subaccounts.append(SubAccount(balance, i))
        
        self.initial_investment += args.firstline_balance
        self.initial_investment += sum(a.value for a in self.subaccounts)

    def calculate(self):
        for i in range(1, (int(self.number_of_days_to_run / 7) * 4)+1):
            self.add_interest_to_firstline()
            self.add_interest_to_subaccounts()
            if self.firstline.waiting_to_deposit >= 25:
                if self.always_reinvest_if_possible: 
                    self.deposit_to_firstline(self.firstline.waiting_to_deposit, i)
                elif i % 4 == 0: 
                    self.deposit_to_firstline(self.firstline.waiting_to_deposit, i)
            for index, sub_account in enumerate(self.subaccounts, start=1):
                if sub_account.waiting_to_deposit >= 25:
                    if i % 4 == 0: 
                        self.deposit_to_subaccount(sub_account.waiting_to_deposit, index, i)


    def add_interest_to_firstline(self):
        val = self.firstline.value * self.percent + 6
        self.firstline.waiting_to_deposit += val
        self.firstline.daily_balance = val


    def add_interest_to_subaccounts(self):
        for account in self.subaccounts:
            interest = account.value * self.percent
            account.waiting_to_deposit += interest
            account.daily_balance = interest


    def print_summary_firstline(self):
        print("\n-----Firstline-----")
        print("After {0} days: {1}$ \nDaily payout: {2}$ \nWeekly payout: {3}$".format(self.number_of_days_to_run,
                                                                                      round(self.firstline.value, 2),
                                                                                      round(self.firstline.daily_balance, 2),
                                                                                      round(self.firstline.daily_balance*4, 2)))


    def print_summary_subaccounts(self):
        print("\n-----Subaccounts-----")
        for account in self.subaccounts:
            print("After {0} days: {1}$ \nDaily payout: {2}$ \nWeekly payout: {3}$".format(self.number_of_days_to_run,
                                                                                        round(account.value, 2),
                                                                                        round(account.daily_balance,2),
                                                                                        round(account.daily_balance*4, 2)))


    def print_total_summary(self):
        total_value = 0
        total_value += self.firstline.value
        for account in self.subaccounts:
            total_value += account.value
        print("\n-----Total Balance-----")
        print("Resulting Balance: " + str(round(total_value, 2)) + "$")
        print("Initial investment: " + str(round(self.initial_investment, 2)) + "$") 


    def get_week_day_from_number(self, n):
        if(n % 4 == 0): return "Sunday" 
        elif(n % 4 == 1): return "Saturday"
        elif(n % 4 == 2): return "Friday"
        elif(n % 4 == 3): return "Thursday" 


    def deposit_to_firstline(self, weekly_amount, day):
        print("Deposit to firstline on {0} (day {1}): {2}$".format(self.get_week_day_from_number(day), str(day), str(round(weekly_amount,2))))
        self.firstline.value += self.firstline.waiting_to_deposit
        self.firstline.waiting_to_deposit = 0


    def deposit_to_subaccount(self, weekly_amount, acc_number, day):
        print("Deposit to Account #{0} on {1} (day {2}): {3}$".format(acc_number, self.get_week_day_from_number(day), str(day), str(round(weekly_amount, 2))))
        account = list(filter(lambda e: e.id == acc_number, self.subaccounts))[0]
        self.firstline.value += account.waiting_to_deposit
        account.waiting_to_deposit = 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("-rs", "--always-reinvest-sunday", type=bool, default=True,
                        help="always reinvest on sundays (if possible) (default True)")
    parser.add_argument("-r", "--always-reinvest", type=bool, default=False,
                        help="always reinvest (if possible) (default False)")
    parser.add_argument("-sn", "--subaccounts", type=int, default=20, help="Default 20")
    parser.add_argument("-fb", "--firstline-balance", type=float, default=300, help="Default is 1000")
    parser.add_argument("-p", "--percent", type=float, default=0.003, help="Default 0.3")
    parser.add_argument("-d", "--days", type=int, default=365, help="Default 365 days")

    args = parser.parse_args()

    calc = ParaibaCalculator()
    calc.parse_args(args)
    calc.calculate()
    calc.print_summary_firstline()
    calc.print_summary_subaccounts()
    calc.print_total_summary()
