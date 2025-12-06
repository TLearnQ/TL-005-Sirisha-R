data = [45, 67, 89, 23, 56]
avg = sum(data) / len(data)

if avg >= 80:
    status = "Excellent"
elif avg >= 60:
    status = "On Track"
elif avg >= 40:
    status = "At Risk"
else:
    status = "Failing"
print("Average:", avg)
print("Category:", status)

