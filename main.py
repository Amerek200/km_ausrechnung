
import csv


class TourAverage():
	def __init__(self):
		self.min_km = 5
		self.max_km = 700
		self.in_file = None
		self.out_file = None
		self.km_keyword = "Strecke (Plan) [Km]"
		self.date_keyword = "Start"
		self.delimiter = ";"

	def run(self):
		try:
			results = self.read_file()
			output = self.get_month_total(results)
			#sort via year & month.
			output.sort(key=lambda dict: (dict["Jahr"], dict["Monat"]))
			self.write_output(output)
			return True
		except (KeyError, PermissionError) as e:
			return e

	def read_file(self):
		results = {}
		with open(self.in_file, "r") as file:
			reader = csv.DictReader(file, delimiter=self.delimiter) #first row = fieldnames, gets skipped by default.
			#needed: "Start" -> datetime, "Strecke (Plan) [Km]" -> km
			for line_dict in reader:
				d, m, y = self.format_start(line_dict[self.date_keyword])
				km = int(line_dict[self.km_keyword])
				if y not in results:
					results[y] = {}
					results[y][m] = {}
					results[y][m][d] = km
				elif m not in results[y]:
					results[y][m] = {}
					results[y][m][d] = km
				elif d not in results[y][m]:
					results[y][m][d] = km
				else:
					results[y][m][d] += km
		return results

	def get_month_total(self, results_dict):
		#total = dict filled with month : total_km.
		totals = {}
		output = []
		for year, months in results_dict.items():
			totals[year] = {}
			for month, days in months.items():
				#create a total k, v for each dictionary of days,km
				#problem with iterating over this.. total would be included.
				#better plan to create a new total dict
				#[0, 0] = km, days
				totals[year][month] = [0, 0]
				for day, km in days.items():
					if self.min_km < km < self.max_km:
						totals[year][month][0] += km
						totals[year][month][1] += 1


		for year, months in totals.items():
			for month, results in months.items():
				output.append({
					"Jahr": year, "Monat": month,
					"km pro Tag": int(results[0]/results[1]),
					"Einsatztage": results[1]})
		return output

	def format_start(self, start_str):
		"""
		format "16.03.2020 08:05" cell into [d, m, y]
		"""
		date = start_str.split(" ")[0]
		date_splitted = date.split(".")
		date_splitted = [int(x) for x in date_splitted]
		return date_splitted

	def write_output(self, output): #year, month, km/day, working days
		f = ["Jahr", "Monat", "km pro Tag", "Einsatztage"]
		with open(self.out_file, "w", newline="") as file:
			writer = csv.DictWriter(file, fieldnames = f)
			writer.writeheader()
			for element in output:
				writer.writerow(element)



if __name__ == "__main__":
	t = TourAverage()
	t.in_file = "Wagen39.csv"
	t.out_file = "output39.csv"
	t.run()
