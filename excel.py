import pandas as pd
import os
import csv


def consolidate_data_excel(Group):
    d = Group.id + '/'
    writer = pd.ExcelWriter(d + f'hourly_summary_{Group.id}.xlsx',
                            engine='xlsxwriter')
    # temp hack for Sofi's order of sheets
    filename_list = ['standings.csv', 'jobs_leadTime.csv', 'jobs_avg_revenue_per_job.csv', 'jobs_completed.csv', 'inventory_level.csv', 'jobs_accepted.csv', 'sta1_queue.csv', 'sta1_util.csv', 'sta2_queue.csv', 'sta2_util.csv', 'sta3_queue.csv', 'sta3_util.csv']
    # for filename in os.listdir(d):
    for filename in filename_list:
        if ".xlsx" not in filename:
            try:
                df = pd.read_csv(d + filename)
                sheet_name = filename.replace(".csv", "")
                df.to_excel(writer, index=False,
                            sheet_name=sheet_name)
            except Exception as e:
                print(f"Failed on {filename} | {e}")
    writer.save()


if __name__ == '__main__':

    class Group:
        def __init__(self, name, id, pw, emails):
            self.name = name
            self.id = id
            self.pw = pw
            self.emails = emails


    groups = []
    with open("groups.csv") as csvfile:  # not tracked
        rows = csv.reader(csvfile)
        for row in rows:
            groups.append(Group(row[0], row[1], row[2], [x for x in row[3:]]))
    consolidate_data_excel(groups[0])
