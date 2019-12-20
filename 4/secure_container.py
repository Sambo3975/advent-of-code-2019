# Part 1
def check_password(code, prev_digit=10, repeated=False):
    if code == 0:
        return repeated
    digit = code % 10
    if digit > prev_digit:
        return False
    return check_password(code // 10, digit, repeated or digit == prev_digit)


def count_possible_passwords(checker, lo, hi):
    count = 0
    for password in range(lo, hi+1):
        count += 1 if checker(password) else 0
    return count


def check_password_2(code, prev_digit=10, repeats=0):
    if code == 0:
        return repeats in [-1, 1]
    digit = code % 10
    if digit > prev_digit:
        return False
    if repeats != -1:
        if digit == prev_digit:
            repeats += 1
        else:
            repeats = -1 if repeats == 1 else 0
    return check_password_2(code // 10, digit, repeats)


if __name__ == '__main__':
    print(count_possible_passwords(check_password, 206938, 679128))
    print(count_possible_passwords(check_password_2, 206938, 679128))
