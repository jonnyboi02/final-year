class House:
    def __init__(self, price, isResidential ):
        if (price<0):
            raise Exception("Price cannot be less than 0")
        self.base_price = price
        self.isResidential = isResidential

    def getBasePrice(self):
        return self.base_price

    def getTotalPrice(self):
        if self.isResidential:
            if self.base_price<=145000:
                return self.base_price
            elif self.base_price>145000 and self.base_price<=250000:
                return self.base_price+self.base_price*0.02
            elif self.base_price>250000 and self.base_price<=325000:
                return self.base_price+self.base_price*0.05
            elif self.base_price>325000 and self.base_price<=750000:
                return self.base_price+self.base_price*0.1
            else:
                return self.base_price+self.base_price*0.12
        else:
            if self.base_price<=150000:
                return self.base_price
            elif self.base_price>150000 and self.base_price<=250000:
                return self.base_price+self.base_price*0.01
            else:
                return self.base_price+self.base_price*0.05


class Test:
    def __init__(self):
        h1 = House(75000, True)
        print(h1.base_price, " ", h1.getTotalPrice())
        h2 = House(145001, True)
        print(h2.base_price, " ", h2.getTotalPrice())
        h3 = House(325001, True)
        print(h3.base_price, " ", h3.getTotalPrice())
        h4 = House(750001, True)
        print(h4.base_price, " ", h4.getTotalPrice())

        h5 = House(1, False)
        print(h5.base_price, " ", h5.getTotalPrice())
        h6 = House(150001, False)
        print(h6.base_price, " ", h6.getTotalPrice())
        h7 = House(325001, False)
        print(h7.base_price, " ", h7.getTotalPrice())

        try:
            h7 = House(-1, False)
            print(h7.base_price, " ", h7.getTotalPrice())
        except:
            print("The house was less than 0")
def main():
    tests = Test()

if __name__ == "__main__":
    main()
