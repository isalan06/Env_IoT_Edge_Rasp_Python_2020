from datetime import datetime

print(datetime.now().strftime("%H"))
if datetime.now().strftime("%H") == "14":
    print("14")
if datetime.now().start_time("%H") == "15":
    print("15")
            