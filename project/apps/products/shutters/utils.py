
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
