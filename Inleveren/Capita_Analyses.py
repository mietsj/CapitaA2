import json
from tld import get_fld
from tabulate import tabulate
import statistics
import matplotlib.pyplot as plt
import pandas as pd
import csv


#Crawl-accept, Crawl-Noop
error_type = [[],[]]
page_load_times = [[],[]]
number_requests = [[],[]]
number_dist_third_parties = [[],[]]
number_dist_tracker_domains = [[],[]]
number_dist_tracker_entities = [[],[]]

#crawl-accept: third party domain;websites present;isTracker?, crawl-noop: third party domain;websites present;isTracker?
exercise4 = [[[],[],[]],[[],[],[]]]

#crawl-accept: X=tranco rank;Y=number of distinct tracker domains, crawl-noop: X;Y
exercise5 = [[[],[]],[[],[]]]

#crawl-accept: tracker entity; websites present, crawl-noop: tracker entity; websites present
exercise6 = [[[],[]],[[],[]]]

request_most_cookies = [[],[]]

def analyses_domain(filename, tracker_list, crawl):
    #Open json file
    with open(filename, "r") as read_file:
        data = json.load(read_file)

    #Get page load time
    page_load_times[crawl].append(data["pageload_end_ts"] - data["pageload_start_ts"])

    third_party_domains = []
    tracker_domains = []
    requests = []
    number_of_requests = 0
    #Sort through requests for number of requests and distinct third parties
    for index, request in enumerate(data["requests"]):
        if "request_url" in request:
            if  request["request_url"].startswith("http"):
                if get_fld(request["request_url"]) not in requests:
                    requests.append(get_fld(request["request_url"]))

                number_of_requests = number_of_requests + 1
                if (get_fld(request["request_url"]) not in third_party_domains) and (get_fld(request["request_url"]) != get_fld(data["website_domain"])):
                    third_party_domains.append(get_fld(request["request_url"]))

    number_requests[crawl].append(number_of_requests)
    number_dist_third_parties[crawl].append(len(third_party_domains))

    #Number of distinct tracker domains
    for request in requests:
        for tracker in tracker_list:
            if (request not in tracker_domains):
                if request == tracker:
                    tracker_domains.append(request)

                #Exercise 4 part
                if (request != get_fld(data["website_domain"])):
                    if crawl == 0:
                        if (request not in exercise4[crawl][0]):
                            if request == tracker:
                                exercise4[crawl][0].append(get_fld(data["website_domain"]))
                                exercise4[crawl][1].append(1)
                                exercise4[crawl][2].append(True)
                                exercise4[crawl + 1][0].append(get_fld(data["website_domain"]))
                                exercise4[crawl + 1][1].append(0)
                                exercise4[crawl + 1][2].append(True)                      
                            elif request != tracker:
                                exercise4[crawl][0].append(get_fld(data["website_domain"]))
                                exercise4[crawl][1].append(1)
                                exercise4[crawl][2].append(False)
                                exercise4[crawl + 1][0].append(get_fld(data["website_domain"]))
                                exercise4[crawl + 1][1].append(0)
                                exercise4[crawl + 1][2].append(False)    
                        elif (request in exercise4[crawl][0]):
                            exercise4[crawl][1][exercise4[crawl][0].index(request)] = exercise4[crawl][1][exercise4[crawl][0].index(request)] + 1
                    elif crawl == 1:
                        if (request not in exercise4[crawl][0]):
                            if request == tracker:
                                exercise4[crawl][0].append(get_fld(data["website_domain"]))
                                exercise4[crawl][1].append(1)
                                exercise4[crawl][2].append(True)
                                exercise4[crawl - 1][0].append(get_fld(data["website_domain"]))
                                exercise4[crawl - 1][1].append(0)
                                exercise4[crawl - 1][2].append(True)                      
                            elif request != tracker:
                                exercise4[crawl][0].append(get_fld(data["website_domain"]))
                                exercise4[crawl][1].append(1)
                                exercise4[crawl][2].append(False)
                                exercise4[crawl - 1][0].append(get_fld(data["website_domain"]))
                                exercise4[crawl - 1][1].append(0)
                                exercise4[crawl - 1][2].append(False)    
                        elif (request in exercise4[crawl][0]):
                            exercise4[crawl][1][exercise4[crawl][0].index(request)] = exercise4[crawl][1][exercise4[crawl][0].index(request)] + 1  

    number_dist_tracker_domains[crawl].append(len(tracker_domains))

    #Fill list for question 5
    exercise5[crawl][0].append(data["tranco_rank"])
    exercise5[crawl][1].append(len(tracker_domains))

    #Number of distinct tracker entities/companies
    tracker_entities = []
    #Open json file
    with open("Inleveren\domain_map.json", encoding="utf8") as read_file:
        domains_map = json.load(read_file)

    for tracker_domain in tracker_domains:
        if domains_map[tracker_domain]["displayName"] not in tracker_entities:
            tracker_entities.append(domains_map[tracker_domain]["displayName"])
            #Exercise 6 part
            if crawl == 0:
                if (domains_map[tracker_domain]["displayName"] not in exercise6[crawl][0]):
                    exercise6[crawl][0].append(domains_map[tracker_domain]["displayName"])
                    exercise6[crawl][1].append(1)
                    exercise6[crawl + 1][0].append(domains_map[tracker_domain]["displayName"])
                    exercise6[crawl + 1][1].append(0)                   
                elif (domains_map[tracker_domain]["displayName"] in exercise6[crawl][0]):
                    exercise6[crawl][1][exercise6[crawl][0].index(domains_map[tracker_domain]["displayName"])] = exercise6[crawl][1][exercise6[crawl][0].index(domains_map[tracker_domain]["displayName"])] + 1
            elif crawl == 1:
                if (domains_map[tracker_domain]["displayName"] not in exercise6[crawl][0]):
                    exercise6[crawl][0].append(domains_map[tracker_domain]["displayName"])
                    exercise6[crawl][1].append(1)
                    exercise6[crawl - 1][0].append(domains_map[tracker_domain]["displayName"])
                    exercise6[crawl - 1][1].append(0)                   
                elif (domains_map[tracker_domain]["displayName"] in exercise6[crawl][0]):
                    exercise6[crawl][1][exercise6[crawl][0].index(domains_map[tracker_domain]["displayName"])] = exercise6[crawl][1][exercise6[crawl][0].index(domains_map[tracker_domain]["displayName"])] + 1


    number_dist_tracker_entities[crawl].append(len(tracker_entities))

def retrieve_tracker_list():
    #Open json file
    with open("Inleveren\services.json", encoding="utf8") as read_file:
        data = json.load(read_file)

    tracker_domains = []

    for categorie in data["categories"]:
        for tracker in data["categories"][categorie]:
            for name, domains in tracker.items():
                for domain, sub_domains in domains.items():
                    if "http:" in domain or "https:" in domain:
                        tracker_domains.append(get_fld(domain))
                    elif "www." in domain:
                        tracker_domains.append(domain[4:])
                    else:
                        tracker_domains.append(domain)
                    for sub_domain in sub_domains:
                        if "www" in sub_domain or "http:" in sub_domain or "https:" in sub_domain:
                            tracker_domains.append(get_fld(sub_domain))
                        elif "www." in sub_domain:
                            tracker_domains.append(sub_domain[4:])
                        else:
                            tracker_domains.append(sub_domain)
    return tracker_domains


#1 Create table, number of failures/error Error type | Crawl-Accept | Crawl-noop


#2 Create boxplots for crawl accept and crawl noop
#2.1 page load time
#2.2 number of requests
#2.3 number of distinct third parties
#2.4 number of disctinct tracker domains
#2.5 number of disctinct tracker entities/companies
def create_boxplots_2():
    data = pd.DataFrame({"Crawl-accept": page_load_times[0], "Crawl-noop": page_load_times[1]})
    ax = data[['Crawl-accept', 'Crawl-noop']].plot(kind='box', title='page_load_times')
    #plt.show()
    plt.savefig('page_load_times.png')
    plt.close()

    data = pd.DataFrame({"Crawl-accept": number_requests[0], "Crawl-noop": number_requests[1]})
    ax = data[['Crawl-accept', 'Crawl-noop']].plot(kind='box', title='number_requests')
    #plt.show()
    plt.savefig('number_requests.png')
    plt.close()

    data = pd.DataFrame({"Crawl-accept": number_dist_third_parties[0], "Crawl-noop": number_dist_third_parties[1]})
    ax = data[['Crawl-accept', 'Crawl-noop']].plot(kind='box', title='number_dist_third_parties')
    #plt.show()
    plt.savefig('number_dist_third_parties.png')
    plt.close()

    data = pd.DataFrame({"Crawl-accept": number_dist_tracker_domains[0], "Crawl-noop": number_dist_tracker_domains[1]})
    ax = data[['Crawl-accept', 'Crawl-noop']].plot(kind='box', title='number_dist_tracker_domains')
    #plt.show()
    plt.savefig('number_dist_tracker_domains.png')
    plt.close()

    data = pd.DataFrame({"Crawl-accept": number_dist_tracker_entities[0], "Crawl-noop": number_dist_tracker_entities[1]})
    ax = data[['Crawl-accept', 'Crawl-noop']].plot(kind='box', title='number_dist_tracker_entities')
    #plt.show()
    plt.savefig('number_dist_tracker_entities.png')
    plt.close()

#3 Compare the data from 2 in a table, with their min median max
def create_table_3():
    table = tabulate({'Metric': ["Page load time (s)", "requests", "distinct third parties", "distinct tracker domains", "distinct tracker entities"], 
                    'Min-accept': [min(page_load_times[0]), min(number_requests[0]), min(number_dist_third_parties[0]), min(number_dist_tracker_domains[0]), min(number_dist_tracker_entities[0])], 
                    'Median-accept': [statistics.median(page_load_times[0]), statistics.median(number_requests[0]), statistics.median(number_dist_third_parties[0]), statistics.median(number_dist_tracker_domains[0]), statistics.median(number_dist_tracker_entities[0])],
                    'Max-accept': [max(page_load_times[0]), max(number_requests[0]), max(number_dist_third_parties[0]), max(number_dist_tracker_domains[0]), max(number_dist_tracker_entities[0])],
                    'Min-noop': [min(page_load_times[1]), min(number_requests[1]), min(number_dist_third_parties[1]), min(number_dist_tracker_domains[1]), min(number_dist_tracker_entities[1])],
                    'Median-noop': [statistics.median(page_load_times[1]), statistics.median(number_requests[1]), statistics.median(number_dist_third_parties[1]), statistics.median(number_dist_tracker_domains[1]), statistics.median(number_dist_tracker_entities[1])],
                    'Max-noop': [max(page_load_times[1]), max(number_requests[1]), max(number_dist_third_parties[1]), max(number_dist_tracker_domains[1]), max(number_dist_tracker_entities[1])],
                    }, 
                    headers='keys', 
                    tablefmt='fancy_grid', 
                    missingval='N/A')

    with open('table3.txt', 'w', encoding="utf-8") as f:
        f.write(table)

#4 Table: third-party domain | crawl-accept | crawl-noop | isTracker?
def create_table_4():
    #The most used third party domain combined of both crawls
    exercise4_combined = []
   
    i = 0
    while i < len(exercise4[0][0]):
        exercise4_combined.append([exercise4[0][0][i], exercise4[0][1][i] + exercise4[1][1][i]])
        i = i + 1

    new_list = sorted(exercise4_combined, key=lambda l:l[1], reverse=True)
    print(new_list)

    table = tabulate({'Third-party domain': [new_list[0][0], new_list[1][0], new_list[2][0], new_list[3][0], new_list[4][0],new_list[5][0],new_list[6][0],new_list[7][0],new_list[8][0],new_list[9][0]], 
                    'Crawl-accept': [exercise4[0][1][exercise4[0][0].index(new_list[0][0])], exercise4[0][1][exercise4[0][0].index(new_list[1][0])], exercise4[0][1][exercise4[0][0].index(new_list[2][0])], exercise4[0][1][exercise4[0][0].index(new_list[3][0])], exercise4[0][1][exercise4[0][0].index(new_list[4][0])], exercise4[0][1][exercise4[0][0].index(new_list[5][0])], exercise4[0][1][exercise4[0][0].index(new_list[6][0])], exercise4[0][1][exercise4[0][0].index(new_list[7][0])], exercise4[0][1][exercise4[0][0].index(new_list[8][0])], exercise4[0][1][exercise4[0][0].index(new_list[9][0])]], 
                    'Crawl-noop': [exercise4[1][1][exercise4[0][0].index(new_list[0][0])], exercise4[1][1][exercise4[0][0].index(new_list[1][0])], exercise4[1][1][exercise4[0][0].index(new_list[2][0])], exercise4[1][1][exercise4[0][0].index(new_list[3][0])], exercise4[1][1][exercise4[0][0].index(new_list[4][0])], exercise4[1][1][exercise4[0][0].index(new_list[5][0])], exercise4[1][1][exercise4[0][0].index(new_list[6][0])], exercise4[1][1][exercise4[0][0].index(new_list[7][0])], exercise4[1][1][exercise4[0][0].index(new_list[8][0])], exercise4[1][1][exercise4[0][0].index(new_list[9][0])]],
                    'isTracker?': [exercise4[1][2][exercise4[0][0].index(new_list[0][0])], exercise4[1][2][exercise4[0][0].index(new_list[1][0])], exercise4[1][2][exercise4[0][0].index(new_list[2][0])], exercise4[1][2][exercise4[0][0].index(new_list[3][0])], exercise4[1][2][exercise4[0][0].index(new_list[4][0])], exercise4[1][2][exercise4[0][0].index(new_list[5][0])], exercise4[1][2][exercise4[0][0].index(new_list[6][0])], exercise4[1][2][exercise4[0][0].index(new_list[7][0])], exercise4[1][2][exercise4[0][0].index(new_list[8][0])], exercise4[1][2][exercise4[0][0].index(new_list[9][0])]],
                    }, 
                    headers='keys', 
                    tablefmt='fancy_grid', 
                    missingval='N/A')

    with open('table4.txt', 'w', encoding="utf-8") as f:
        f.write(table)


#5 crawl-noop and crawl-accept: scatter plot Y=number of distinct tracker domain, X=Website tranco
def create_scatter_5():
    plt.scatter(exercise5[0][0], exercise5[0][1])
    #plt.show()
    plt.savefig('question5_crawlaccept')
    plt.close()

    plt.scatter(exercise5[1][0], exercise5[1][1])
    #plt.show()
    plt.savefig('question5_crawlnoop')
    plt.close()

#6 Add a table of top ten tracker entities (companies) and their prevalence (based on the
#number of distinct websites where the entity is present). Similar to the table in 4, but
#should only contain tracker entities). The Tips section below explains how to match
#domains to entities.
def create_table_6():
    #The most used third party domain combined of both crawls
    exercise6_combined = []
   
    i = 0
    while i < len(exercise6[0][0]):
        exercise6_combined.append([exercise6[0][0][i], exercise6[0][1][i] + exercise6[1][1][i]])
        i = i + 1

    new_list = sorted(exercise6_combined, key=lambda l:l[1], reverse=True)
    print(new_list)

    table = tabulate({'Third-party domain': [new_list[0][0], new_list[1][0], new_list[2][0], new_list[3][0], new_list[4][0],new_list[5][0],new_list[6][0],new_list[7][0],new_list[8][0],new_list[9][0]], 
                    'Crawl-accept': [exercise6[0][1][exercise6[0][0].index(new_list[0][0])], exercise6[0][1][exercise6[0][0].index(new_list[1][0])], exercise6[0][1][exercise6[0][0].index(new_list[2][0])], exercise6[0][1][exercise6[0][0].index(new_list[3][0])], exercise6[0][1][exercise6[0][0].index(new_list[4][0])], exercise6[0][1][exercise6[0][0].index(new_list[5][0])], exercise6[0][1][exercise6[0][0].index(new_list[6][0])], exercise6[0][1][exercise6[0][0].index(new_list[7][0])], exercise6[0][1][exercise6[0][0].index(new_list[8][0])], exercise6[0][1][exercise6[0][0].index(new_list[9][0])]], 
                    'Crawl-noop'  : [exercise6[1][1][exercise6[0][0].index(new_list[0][0])], exercise6[1][1][exercise6[0][0].index(new_list[1][0])], exercise6[1][1][exercise6[0][0].index(new_list[2][0])], exercise6[1][1][exercise6[0][0].index(new_list[3][0])], exercise6[1][1][exercise6[0][0].index(new_list[4][0])], exercise6[1][1][exercise6[0][0].index(new_list[5][0])], exercise6[1][1][exercise6[0][0].index(new_list[6][0])], exercise6[1][1][exercise6[0][0].index(new_list[7][0])], exercise6[1][1][exercise6[0][0].index(new_list[8][0])], exercise6[1][1][exercise6[0][0].index(new_list[9][0])]],
                    }, 
                    headers='keys', 
                    tablefmt='fancy_grid', 
                    missingval='N/A')

    with open('table6.txt', 'w', encoding="utf-8") as f:
        f.write(table)

#7 3 cookies with the longest lifespans for each crawl, only include first 5 char of Value
# Name | Value | Domain | Path | Expires/Max-Age | Size | HttpOnly | Secure | SameSite

#8 3 requests with the most cookies 
#for each crawl: Request hostname | Website | Number of cookies| First-party request

if __name__ == "__main__":
    tracker_list = retrieve_tracker_list()
    
    
    with open("tranco-top-500-safe.csv", 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            if row[1] != "domain" and int(row[0]) < 11:
                if int(row[0]) == 11:
                    print("break")
                    break

                print(row[0], row[1])
                analyses_domain("Data_New/accept-data/" + row[1] + "_accept.json", tracker_list, 0)
                analyses_domain("Data_New/noop-data/" + row[1] + "_noop.json", tracker_list, 1)

    #Create boxplots and table
    print("Starting exercise 2")
    create_boxplots_2()
    print("Starting exercise 3")
    create_table_3()

    #Need more data for this to work
    print("Starting exercise 4")
    create_table_4()
    print("Starting exercise 5")
    create_scatter_5()
    print("Starting exercise 6")
    create_table_6()

    
    

