from django.test import TestCase
import random
def card_no():
    no = 4187
    no2 = random.randint(111111111111, 999999999999)
    n = f'{no}{no2}'
    c1 = n[0:4]
    c2 = n[4:8]
    c3 = n[8:12]
    c4 = n[12:16]
    print(c1)
    print(c2)
    print(c3)
    print(c4)
    return n
print(card_no())