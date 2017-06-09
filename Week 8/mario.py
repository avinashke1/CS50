import sys
import cs50

print ("Enter the Height--")
n=cs50.get_int()
k = 30
for i in range(0, n):
	for j in range(0, k):
		print(end=" ")
	k = k - 2
	for j in range(0, i+1):
		print("# ", end="")
	print()
