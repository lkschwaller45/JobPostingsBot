import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time


class Scraping:

    def __init__(self):



        results_per_city = 10
        cities = ["New+York", "Chicago", "San+Francisco", "Austin", "Seattle", "Los+Angeles", "Philadelphia", "Atlanta",
                  "Dallas", "Pittsburgh", "Portland", "Phoenix", "Denver", "Houston", "Miami", "Washington+DC",
                  "Boulder"]
        columns = ["Area Searched", "Job Title", "Company", "location", "Salary", "Summary"]
        job_post_original = []
        dataframe = pd.DataFrame(columns=columns)
        for city in cities:
            for start in range(0,results_per_city,10):
                page = requests.get("http://www.indeed.com/jobs?q=aerospace+engineer+%2420%2C000&l=" + str(city) + "&start=" + str(start))
                print("http://www.indeed.com/jobs?q=aerospace+engineer+%2420%2C000&l=" + str(city) + "&start=" + str(start))
                time.sleep(1)
                soup = BeautifulSoup(page.text, "lxml", from_encoding ="utf - 8")
                job_post = self.find_job_titles(soup,city)
                job_post_original.append(job_post)
        data = pd.DataFrame(job_post_original,columns=columns)
        data.set_index(["Area Searched"],inplace=True)
        data.to_csv("data.csv")
        #print(dataframe)

    def find_job_titles(self,soup,city):
         for div in soup.find_all(name="div", attrs={"class":"row"}):

             job_post = []
             job_post.append(city)
             for a in div.find_all(name="a",attrs={"data-tn-element":"jobTitle"}):
                 job_post.append(a["title"])
             job_post = self.find_companies_for_jobs(div,job_post)
             job_post_clone = job_post
             job_post = self.find_location_for_job(div,job_post)
             #job_post = self.check_for_location_bug(job_post,city,job_post_clone)
             job_post = self.find_salary(job_post,div)
             job_post = self.find_summaries(div,job_post)
             if len(job_post) == 5:
                 job_post.insert(3,("Near " + str(city)))
         return(job_post)
    def find_companies_for_jobs(self,div,job_post):
             company =  div.find_all(name="span",attrs={"class":"company"})
             if len(company) > 0 :
                 for b in company:
                     job_post.append(b.text.strip())
                 else:
                     sec_try = div.find_all(name= "span", attrs={"class":"result-link-source"})
                     for span in sec_try:
                         job_post.append(span.text.strip())
             return(job_post)
    def find_location_for_job(self,div,job_post):
        div3 = div.findAll("span",attrs={"class":"location accessible-contrast-color-location"})
        for span in div3:
            job_post.append(span.text)
        return(job_post)
    def check_for_location_bug(self,job_post,city,job_post_clone):
        print(job_post)
        print(job_post_clone)

        return(job_post)
    def find_salary(self,job_post,div):

        try:
            job_post.append(div.find("nobr").text)
        except:
            try:
                div_two = div.find(name="div", attrs = {"class":"salarySnippet"})
                div_three = div_two.find(name="span", attrs = {"class":"salaryText"})
                job_post.append(div_three.text.strip())
            except:
                job_post.append("Nothing_found")
            return (job_post)
    def find_summaries(self,div,job_post):
         spans = div.find_all(name="div",attrs={"class":"summary"})
         for span in spans:
             job_post.append(span.text.strip())
         return (job_post)
search_one = Scraping()