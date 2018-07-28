class Payment:

    def __init__(self, pay_to, pay_amount):
        self.pay_to = pay_to
        self.pay_amount = pay_amount


class Person:
    def __init__(self, money_spent, name, members) -> None:
        self.payments = []
        self.lack_of_money: int = None
        self.spent = money_spent
        self.name = name
        self.members = members

    def __repr__(self) -> str:
        return f'<Person name: {self.name} spent: {self.spent}, money: {self.lack_of_money}'

    def __str__(self):
        return self.name

    def pay(self, payer: 'Person'):
        if self.lack_of_money + payer.lack_of_money >= 0:
            payment = Payment(pay_to=payer.name, pay_amount=int(self.lack_of_money))
            payer.lack_of_money = payer.lack_of_money + self.lack_of_money
            self.lack_of_money = 0
            self.payments.append(payment)
        else:
            payment = Payment(pay_to=payer.name, pay_amount=int(payer.lack_of_money))
            self.lack_of_money = self.lack_of_money + payer.lack_of_money
            payer.lack_of_money = 0
            self.payments.append(payment)


def calculate():
    q = input('Input numbers of families ')

    persons_num = int(q)
    persons = []
    for person in range(0, persons_num):
        ok = False
        while not ok:
            try:
                person_name = input(f'Input person name\n')
                spent = input(f'Input moneys spent\n')
                members = input(f'Input members\n')
                spent_int = sum([int(i) for i in spent.split(',') if i != ''])
                members_int = int(members)
                persons.append(
                    Person(
                        money_spent=spent_int,
                        name=person_name,
                        members=members_int
                    )
                )
                ok = True
            except ValueError:
                print(f'Cant parse input {spent}, only numeric value available')
                pass

    total_spent = sum([person.spent for person in persons])
    median_spent = total_spent/sum([person.members for person in persons])*-1

    for person in persons:
        person.lack_of_money = person.spent + (median_spent*person.members)

    while not all(map(lambda x: x == 0, [int(person.lack_of_money) for person in persons])):
        try:
            prof_person = next(proficit_person(persons))
            def_person = next(deficit_person(persons))
            if prof_person is not def_person:
                prof_person.pay(def_person)
            else:
                def_person = next(deficit_person(persons))
                prof_person.pay(def_person)
        except StopIteration:
            pass

    return persons, median_spent


def deficit_person(persons: [Person]):
    for person in persons:
        if person.lack_of_money > 0:
            yield person
    else:
        return None


def proficit_person(persons: [Person]):
    for person in persons:
        if person.lack_of_money < 0:
            yield person
    else:
        return None


if __name__ == '__main__':
    calculated_persons, median_spent = calculate()
    print('Calculating')
    print(f'Total spent {sum([person.spent for person in calculated_persons])}')
    print(f'Median spent {int(median_spent)}')
    print('*'*20)
    for person in calculated_persons:
        print(f'{person} spent {person.spent}')
        for payment in person.payments:
            print(f'{person} should pay to {payment.pay_to} amount of {abs(payment.pay_amount)}')
        print('*'*20)
