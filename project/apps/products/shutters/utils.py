import math


# custom round for shutter pricing
# if inches/12 = x.5 or less, round to 0.5. else, round to next integer
# ex. 34/12 = 2.83 --> round to 3
# ex. 28/12 = 2.33 --> round to 2.5
def custom_round(num):
    dec = round(num % 1, 2)

    if dec <= .5:
        r = (round(num*2))/2
    else:
        r = round(num)
    return r

# display decimals as fractions
def as_fraction(n):
    number = int(n)
    dec = round(n % 1, 4)

    if (dec == 0):
        return number
    else:
        ratio = dec.as_integer_ratio()
        frac = '{}/{}'.format(ratio[0], ratio[1])
        final = '{} {}'.format(number, frac)

        return final

# round up to next even number
def round_up_to_even(f):
    return math.ceil(f / 2.) * 2
