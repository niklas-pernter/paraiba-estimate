import argparse


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

    def parse_args(self, args):
        self.first_line_balance = args.firstline_balance
        self.number_of_days_to_run = args.days
        self.percent = args.percent
        self.current_balance = self.first_line_balance

        self.OK = True

    def calculate(self):
        if not self.OK: return

        for i in range(int(self.number_of_days_to_run / 7) * 4):
            daily_amount = self.current_balance * self.percent + 6
            self.add_daily_payout_to_weekly(daily_amount)
            if self.weekly_balance >= 25 or (
                    self.always_deposit_if_weekly_balance_greater_than_25 and self.daily_payout >= 25):
                self.deposit_to_firstline(self.weekly_balance)

    def print_summary(self):
        print("---------------------")
        print("After {0} days: {1}$ \nDaily payout: {2}$ \nWeekly payout: {3}".format(self.number_of_days_to_run,
                                                                                      round(self.current_balance),

                                                                                      round(self.daily_payout),
                                                                                      round(self.daily_payout * 4)))

    def add_daily_payout_to_weekly(self, daily_amount):
        self.daily_payout = daily_amount
        print("Daily Payout: " + str(self.daily_payout))
        self.weekly_balance += daily_amount

    def deposit_to_firstline(self, weekly_amount):
        print("Deposit to firstline: " + str(weekly_amount))
        self.current_balance += weekly_amount
        self.weekly_balance = 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--firstline-balance", type=float, default=300)
    parser.add_argument("-r", "--always-reinvest", type=bool, default=True,
                        help="always reinvest after one week (if possible)")
    parser.add_argument("-p", "--percent", type=float, default=0.003)
    parser.add_argument("-d", "--days", type=int, default=365)

    args = parser.parse_args()

    calc = ParaibaCalculator()
    calc.parse_args(parser.parse_args())
    calc.calculate()
    calc.print_summary()
