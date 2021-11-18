import argparse


class ParaibaCalculator:

    def __init__(self):
        self.number_of_days_to_run = 0
        self.total_investment = 0.0
        self.always_reinvest_on_sundays = True
        self.percent = 0.003
        self.current_balance = 0.0
        self.OK = False
        self.daily_payout = 0
        self.weekly_balance = 0
        self.always_reinvest_if_possible = False

    def parse_args(self, args):
        self.total_investment = args.total_investment
        self.number_of_days_to_run = args.days
        self.percent = args.percent
        self.current_balance = self.total_investment
        self.always_reinvest_on_sundays = args.always_reinvest_sunday
        self.always_reinvest_if_possible = args.always_reinvest

        self.OK = True

    def calculate(self):
        if not self.OK: return

        for i in range(int(self.number_of_days_to_run / 7) * 4):
            daily_amount = self.current_balance * self.percent + 6
            self.add_daily_payout_to_weekly(daily_amount)
            if self.always_reinvest_if_possible:
                if self.weekly_balance >= 25:
                    self.deposit_to_firstline(daily_amount)
            else:
                if i % 4 == 0:
                    if self.weekly_balance >= 25:
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
        print("Deposit to accounts: " + str(weekly_amount))
        self.current_balance += weekly_amount
        self.weekly_balance = 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--total-investment", type=float, default=2100, help="Default 2000$")
    parser.add_argument("-rs", "--always-reinvest-sunday", type=bool, default=True,
                        help="always reinvest on sundays (if possible) (default True)")
    parser.add_argument("-r", "--always-reinvest", type=bool, default=False,
                        help="always reinvest (if possible) (default False)")
    parser.add_argument("-p", "--percent", type=float, default=0.003, help="Default 0.3%")
    parser.add_argument("-d", "--days", type=int, default=365, help="Default 365 days")

    args = parser.parse_args()

    calc = ParaibaCalculator()
    calc.parse_args(parser.parse_args())
    calc.calculate()
    calc.print_summary()
