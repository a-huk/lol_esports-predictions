import csv

with open('/srv/dev-disk-by-uuid-14c64766-d1ce-46c9-82f7-d1e8b371d1cb/nas/Projects/lol_predictions/results.csv', "r", newline='') as file:
    reader = csv.reader(file)
    predictions = list(reader)

print("I am writing to github csv:")
print(predictions)

with open("/srv/dev-disk-by-uuid-14c64766-d1ce-46c9-82f7-d1e8b371d1cb/nas/Projects/lol_predictions/lol_esports-predictions/results.csv", "a") as csvfile:
	writer = csv.writer(csvfile)
	writer.writerows(predictions)

with open('/srv/dev-disk-by-uuid-14c64766-d1ce-46c9-82f7-d1e8b371d1cb/nas/Projects/lol_predictions/results.csv', "w") as file2:
    pass