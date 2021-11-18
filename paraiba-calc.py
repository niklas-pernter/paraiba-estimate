class ParaibaCalculator:

    def __init__(self):
        self.number_of_days_to_run = 0
        self.first_line_balance = 0.0
        self.always_reinvest = True
        self.percent = 0.003
        self.current_balance = 0.0
        self.OK = False
        self.always_deposit_if_weekly_balance_greater_than_25 = False
        self.daily_payout = 0
        self.weekly_balance = 0

    def get_user_input(self):
        self.first_line_balance = int(input("Your Paraiba fistline balance: ") or 245)
        self.number_of_days_to_run = int(input("Number of days to calculate (default 365): ") or 365)
        self.number_of_days_to_run = int(input("Number of days to calculate (default 365): ") or 365)
        self.always_deposit_if_weekly_balance_greater_than_25 = bool(
            input("Always deposit to firstline if weekly balance greater than 25$? (default false): ") or False)

        self.current_balance = self.first_line_balance
        self.percent = float(input("Daily percentage: ") or 0.003)

        self.OK = True

    def calculate(self):
        self.get_user_input()
        if not self.OK: return

        weekly_balance = 0
        for i in range(int(self.number_of_days_to_run / 7) * 4):
            daily_amount = self.current_balance * self.percent + 6
            self.add_daily_payout_to_weekly(daily_amount)
            self.weekly_balance += self.daily_payout
            if weekly_balance >= 25:
                self.deposit_to_firstline(weekly_balance)

        print("After {0} days you will have {1}$ with a daily payout of {2}$".format(self.number_of_days_to_run,
                                                                                     round(self.current_balance),
                                                                                     round(self.daily_payout)))

    def add_daily_payout_to_weekly(self, daily_amount):
        self.daily_payout = daily_amount
        print("Daily Payout: " + str(self.daily_payout))
        self.weekly_balance += daily_amount

    def deposit_to_firstline(self, weekly_amount):
        print("Deposit to firstline: " + str(weekly_amount))
        self.current_balance += weekly_amount
        self.weekly_balance = 0


if __name__ == "__main__":
    ParaibaCalculator().calculate()
