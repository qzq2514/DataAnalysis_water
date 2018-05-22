# def orgin(num ):
#     dest_bin = []
#     while True:
#         dest_bin.append(num % 2)
#         print(num // 2)
#         num = num // 2
#         if num==0:
#           return dest_bin

num=23
#原数变补码
def orgin(num ):
    # if num >= 0:
    #     dest_bin = [0]
    # else:
    #     dest_bin = [1]
    dest_bin = []
    num = abs(num)
    i = 32768
    while(i):
        if( num//i ):
            temp = [1]
            num -= i
        else:
            temp = [0]
        dest_bin = dest_bin + temp
        i //= 2
    return dest_bin

print(orgin(num))

#补码取反
def inverse( org_num ):
    i = 0
    while(i < len(org_num)):
        org_num[i]=1-org_num[i]
        i += 1
    return org_num
print(inverse(orgin(num)))

#加一
def add_bin( num1, num2):
    len1 = len(num1)
    sum_num = [0]*len1
    carry_flag = 0
    while(len1 >= 0):
        len1 -= 1
        sum = int(num1[len1]) + int(num2[len1]) + carry_flag
        if sum == 0:
            pass
        elif sum == 1:
            sum_num[len1] = 1
            carry_flage = 0
        elif sum == 2:
            carry_flag = 1
            sum_num[len1] = 0
        elif sum == 3:
            carry_flag = 1
            sum_num[len1] = 0
    return sum_num

Yuan=add_bin(inverse(orgin(num)), [0]*15+[1])
print(Yuan)

