import csv
import os
import pandas as pd
from datetime import datetime
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class DataTarget:
    def __init__(self, name, url, filename, sleeptime, cumulative_data=True):
        self.name = name
        self.url = url
        self.filename = filename
        self.sleeptime = sleeptime
        self.cumulative_data = cumulative_data


jobs_accepted = DataTarget("job accepted", "Plot?data=JOBIN&x=all", 'jobs_accepted.csv', 4)
inventory = DataTarget("inventory", "Plot?data=INV&x=all", 'inventory_level.csv', 4)
sta1_queue = DataTarget("station 1 queue", "Plot?data=S1Q&x=all", 'sta1_queue.csv', 4)
sta2_queue = DataTarget("station 2 queue", "Plot?data=S2Q&x=all", 'sta2_queue.csv', 4)
sta3_queue = DataTarget("station 3 queue", "Plot?data=S3Q&x=all", 'sta3_queue.csv', 4)
sta1_util = DataTarget("station 1 util", "Plot?data=S1UTIL&x=all", 'sta1_util.csv', 4)
sta2_util = DataTarget("station 2 util", "Plot?data=S2UTIL&x=all", 'sta2_util.csv', 4)
sta3_util = DataTarget("station 3 util", "Plot?data=S3UTIL&x=all", 'sta3_util.csv', 4)
jobs_completed = DataTarget("jobs completed", "Plot?data=JOBOUT&x=all", 'jobs_completed.csv', 4)
jobs_lead_time = DataTarget("jobs lead time", "Plot?data=JOBT&x=all", 'jobs_leadTime.csv', 4)
jobs_revenue = DataTarget("jobs revenue", "Plot?data=JOBREV&x=all", 'jobs_avg_revenue_per_job.csv', 4)
standings = DataTarget("standings", "Standing", 'standings.csv', 10, False)
things_to_scrape = [jobs_accepted, jobs_accepted, inventory,
                    sta1_queue, sta2_queue, sta3_queue,
                    sta1_util, sta2_util, sta3_util,
                    jobs_completed, jobs_lead_time, jobs_revenue,
                    standings]


def scrape(Group):
    ## login
    url = "http://op.responsive.net/lt/chicago/entry.html"
    driver = webdriver.Chrome()
    driver.get(url)

    elem = driver.find_element_by_name("id")
    elem.clear()
    elem.send_keys(Group.id)

    elem = driver.find_element_by_name("password")
    elem.clear()
    elem.send_keys(Group.pw)

    elem.send_keys(Keys.RETURN)

    ##  begin scraping
    prefix = "http://op.responsive.net/Littlefield/"

    if not os.path.isdir(Group.id):
        os.mkdir(Group.id)
    for x in things_to_scrape:
        try:
            driver.get(prefix + x.url)
            out = []
            sleep(x.sleeptime)
            try:
                driver.find_element_by_name("data").click()
            except:
                pass
            trs = driver.find_elements_by_tag_name("tr")
            for tr in trs:
                tds = tr.find_elements_by_tag_name('td')
                if tds:
                    out.append([td.text.replace(",", "") for td in tds])
            fn = Group.id + "/" + x.filename
            if x.cumulative_data:
                with open(fn, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerows(out)
            else:
                df = pd.read_csv(fn, delimiter=',')
                df = df[1:]
                out[0][0] = "rank_" + datetime.now().strftime('%Y-%m-%d %H:%M')
                out[0][2] = "cash_" + datetime.now().strftime('%Y-%m-%d %H:%M')
                newdata = pd.DataFrame(out)
                newdata.columns = newdata.iloc[0]
                newdata = newdata[1:]
                result = pd.merge(df, newdata, on='Team')
                result.to_csv(fn, index=False, sep=',')

        except Exception as e:
            print(f'failed on {x.name} for {Group.name} | {e}')


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
    scrape(groups[0])
