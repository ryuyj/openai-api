print('openai API Project')

def odd_or_even(number):
    if number % 2 == 0:
        print(f"{number}은(는) 짝수입니다.")
    else:
        print(f"{number}은(는) 홀수입니다.")

# 예제 사용
odd_or_even(4)  # 출력: 4은(는) 짝수입니다.
odd_or_even(7)  # 출력: 7은(는) 홀수입니다.


def check_number_type(number):
    result = "짝수" if number % 2 == 0 else "홀수"
    return f"{number}은(는) {result}입니다."

# 예제 사용
print(check_number_type(4))  # 출력: 4은(는) 짝수입니다.
print(check_number_type(7))  # 출력: 7은(는) 홀수입니다.

