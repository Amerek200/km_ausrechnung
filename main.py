import csv

#TODO: query for input file.
#TODO: Export results in something useful.
#TODO: Make GUI
#TODO: Apply min/max values.
#DONE: Check if different years work.
#DONE: work with any number of columns -> use dictreader
#CHECK: any reason to format Start into correct datetime?

def main():
	results = {}
	#set min and max km for a given day, days out of this range will be filtered out.
	min_km = 10
	max_km = 700

	with open("Wagen39.csv", "r") as file:
		reader = csv.DictReader(file, delimiter=";") #first row = fieldnames, gets skipped by default.
		#needed: "Start" -> datetime, "Strecke (Plan) [Km]" -> km
		
		for line_dict in reader:
			#line_dict = next(reader)
			d, m, y = formatStart(line_dict["Start"])
			km = int(line_dict["Strecke (Plan) [Km]"])
			#would the other way around be easier? check if not and create?
			if y in results:
				if m in results[y]:
					if d in results[y][m]:

						results[y][m][d] += km
					else:
						results[y][m][d] = km
				else:
					results[y][m] = {}
					results[y][m][d] = km
			else:
				results[y] = {}
				results[y][m] = {}
				results[y][m][d] = km
	


	output = getMonthTotal(results)
	writeOutput(output)
	

def getMonthTotal(results_dict):
	#total = dict filled with month : total_km.
	totals = {}
	output = []
	for year, months in results_dict.items():
		#print(year)
		#print(months)
		
		totals[year] = {}
		for month, days in months.items():
			#create a total k, v for each dictionary of days,km
			#problem with iterating over this.. total would be included.
			#better plan to create a new total dict 
			#[0, 0] = km, days
			totals[year][month] = [0, len(days)]
			#work_days = len(days)
			#print(len(days))
			for day, km in days.items():
				totals[year][month][0] += km
				pass
	#print(totals)
	for year, months in totals.items():
		for month, results in months.items():
			output.append({
				"Jahr": year, "Monat": month, 
				"km pro Tag": int(results[0]/results[1]),
				"Einsatztage": results[1]})
	#print(output)
	return output

def checkValues(results, min_km, max_km):
	"""
	filters out days which are outside of given min/max range.
	"""



def formatStart(start_str):
	#casting to "int" removes leading "0"s
	#splits date and time, date = splitted[0]
	date = start_str.split(" ")[0]
	date_splitted = date.split(".")
	date_splitted = [int(x) for x in date_splitted]
	#return: [8, 1, 2020]  
	return date_splitted


def writeOutput(output):
	f = ["Jahr", "Monat", "km pro Tag", "Einsatztage"]
	with open("output.csv", "w") as file:
		writer = csv.DictWriter(file, fieldnames = f)
		writer.writeheader()
		for element in output:
			writer.writerow(element)



	
	
if __name__ == "__main__":
	main()