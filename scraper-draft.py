from bs4 import BeautifulSoup
import csv
from dateutil import parser, rrule
from datetime import datetime, time, date
import time
import requests

start_date = "2017-03-01"
end_date = "2017-03-31"
start = parser.parse(start_date)
end = parser.parse(end_date)
dates = list(rrule.rrule(rrule.DAILY, dtstart=start, until=end))
date_list = []

for date in dates:
    date_list.append(date.strftime("%Y-%m-%d"))

with open('station-list-draft.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        site_name = row["\ufeffSite Name"]
        site_code = row["Code"]
        loc_lat = row["Lat"]
        loc_long = row["Long"]

        for date in date_list:
            url = f"https://www.wunderground.com/dashboard/pws/{site_code}/table/{date}/{date}/daily"
            response = requests.get(url)
            html = response.text
            soup = BeautifulSoup(html, "html.parser")
            table = soup.find_all("table")
            table = table[3]

            output_rows = []
            header_row = table.findAll('tr')[0].findAll('th')
            header_output_row = []

            for header in header_row:
                header_output_row.append(header.text)

            header_output_row.append("Date")
            header_output_row.append("Site Name")
            header_output_row.append("Site Code")
            header_output_row.append("Lat")
            header_output_row.append("Long")
            output_rows.append(header_output_row)

            for table_row in table.findAll('tr'):
                columns = table_row.findAll('td')
                output_row = []
                if columns == []:
                    continue
                else:
                    for column in columns:
                        # identifies blank cells
                        if column.text == "":
                            output_row.append("IB")
                        else:
                            output_row.append(column.text)
                    output_row.append(date)
                    output_row.append(site_name)
                    output_row.append(site_code)
                    output_row.append(loc_lat)
                    output_row.append(loc_long)
                    output_rows.append(output_row)

            with open(f'{date}_{site_code}.csv', 'w') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(output_rows)

            # save HTML file associated with CSV data
            f = open(f"{date}_{site_code}.html", "w")
            f.write(html)
            f.close()
