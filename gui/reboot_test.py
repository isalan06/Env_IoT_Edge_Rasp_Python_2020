from datetime import datetime

test_index = 0

print(datetime.now().strftime("%H"))
if datetime.now().strftime("%H") == "14":
    test_index = 1
    print("14")
if datetime.now().strftime("%H") == "15":
    print("15")


if (datetime.now().strftime("%H") == "14") and (test_index == 1):
    print("AAA")