import matplotlib.pyplot as plt
import csv
epochs = []
loss = []
accuracy = []

file1 = open('23max.txt', 'r')
lines = file1.readlines()

for idx, line in enumerate(lines):
	if "val_acc" in line:
		print(line.strip())
		print(line.split("epoch: ")[1].split(" |")[0])
		epochs.append(int(line.split("epoch: ")[1].split(" |")[0]))
		print(float(line.split("loss: ")[1].split(" -")[0]))
		loss.append(line.split("loss: ")[1].split(" -")[0])
		print(line.split("acc: ")[1].split(" |")[0])
		accuracy.append(float(line.split("acc: ")[1].split(" |")[0]))




"""
# plotting the line 1 points
px = 1/plt.rcParams['figure.dpi']  # pixel in inches
plt.subplots(figsize=(1920*px, 1080*px))

plt.scatter(epochs, loss, label = "Loss")


# plotting the line 2 points
#plt.plot(epochs, accuracy, label = "Accuracy")
 
# naming the x axis
plt.xlabel('x - axis')
# naming the y axis
plt.ylabel('y - axis')
# giving a title to my graph
plt.title('Two lines on same graph!')
plt.legend()
plt.savefig('foo.png')
print(min(loss))
print(max(loss))
plt.ylim([0, 1])
plt.xlim([0, 1000])
print(loss[-1])
"""
final_data = []
for idx, value in enumerate(epochs):
	final_data.append([value, loss[idx], accuracy[idx]])

with open('23max.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(final_data)