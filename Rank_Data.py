import requests
from bs4 import BeautifulSoup

# NOTE: For all the Data Retrieval Functions, a while loop is utilized to parse through the multiple pages
# of data. The "if not" statement at the end of each loop checks the existence of data to parse through. If
# the data does not exist, the loop will break. The race variable at the end of each loop is used to navigate
# to the next page of available data in RuneClan.


# ========================================= DATA RETRIEVAL FUNCTIONS =================================================


# Opens RuneClan Hiscores page for our clan and scrapes RSN's and Total Levels. Information placed into lists
# for use by main.

def name_and_level(race, list1, list2):

    while requests.get('http://www.runeclan.com/clan/the_nameless_crusade/hiscores/' + str(race) + '?skill=2'):

        raw_html1 = requests.get('http://www.runeclan.com/clan/the_nameless_crusade/hiscores/' + str(race) + '?skill=2')
        soup1 = BeautifulSoup(raw_html1.text, "html.parser")

        rsn = soup1.findAll("td", {"class": "clan_td clan_rsn2"})
        total_lvl = soup1.findAll("td", {"class": "clan_td clan_xpgain_hs"})

        for name in rsn:
            list1.append(name.find("a").text)
        for level in total_lvl:
            list2.append(level.text.strip().replace(",", ""))

        if not rsn:
            break

        race += 1

    del list2[1::2]


# Opens RuneClan Members page for our clan and scrapes the date in which players joined the clan.
# Also scrapes the name associated with the date to match the data to the Total Level and RSN
# scraped earlier. More on this in the combine_and_print function. All data is placed into lists
# for use by main.

def date_joined(race, list1, list2):

    while requests.get('http://www.runeclan.com/clan/the_nameless_crusade/members/' + str(race) + "?"):

        raw_html2 = requests.get('http://www.runeclan.com/clan/the_nameless_crusade/members/' + str(race) + "?")
        soup2 = BeautifulSoup(raw_html2.text, "html.parser")

        player_name = soup2.findAll("span", {"class": "clan_rsn3_name"})
        date_joined_ = soup2.findAll("span", {"class": "clan_rsn3_joined"})

        for date in date_joined_:
            list1.append(date.text.strip())

        for name in player_name:
            list2.append(name.find("a").text)

        if not date_joined_:
            break

        race += 1


# Again, opens the RuneClan members page for our clan and scrapes the rank of each player. Rank is
# placed into a list for main.

def get_rank(race, list1):

    while requests.get('http://www.runeclan.com/clan/the_nameless_crusade/members/' + str(race) + "?"):

        raw_html2 = requests.get('http://www.runeclan.com/clan/the_nameless_crusade/members/' + str(race) + "?")
        soup2 = BeautifulSoup(raw_html2.text, "html.parser")

        player_level = soup2.findAll("td", {"class": "clan_td clan_rank"})

        for level in player_level:
            list1.append(level.text.strip())

        if not player_level:
            break

        race += 1


# ======================================== DATA MANIPULATION FUNCTIONS ================================================


# Takes the lists of information provided by previous functions, and matches it
# using the sorting_funct so that all information can be iterated through together. list5 and
# list6 are the reorganized versions of list5 and list2 (original join dates and original starting
# ranks. These new lists are returned to main and rewrite the old lists.

def combine_and_reorganize(list1, list2, list3, list4):

    list5 = []
    list6 = []

    for name in list4:
        sorting_funct(name, list1, list3, list5, list6, list2)

    return list5, list6


# Compares the name from the original list of names gathered and matches it to the same name in the second
# list of names gathered. Then, the position of the name in the second list is recorded and used to index
# the corresponding join date and rank. That information is then appended to the new lists to match the
# initial list of names when printed.

def sorting_funct(value, compared_value, starting_date, end_result, end_result2, starting_rank):

    for index, name in enumerate(compared_value):
        if value == name:
            end_result.append(starting_date[index])
            end_result2.append(starting_rank[index])


# Compares the rank, total level, and, where applicable, asks if the player is in discord for each player
# and determines if an adjustment in rank needs to be made. This function DOES NOT take into account the date
# joined aspect of our clan's ranking system. Thus, the date must be checked to match our criteria on a case
# by case basis.

def rank_changes(list1, list2, list4):

    list5 = []

    for index, name in enumerate(list1):

        level = int(list2[index])

        if list4[index] == "Admin" or list4[index] == "Organiser" or list4[index] == "Coordinator" or list4[index] == "Deputy Owner" or list4[index] == "Owner":
            list5.append("N/A")
            continue

        elif list4[index] == "Captain":
            response = input("Is " + name + " in the Discord? ")
            if response == "Yes" or response == "yes":
                list5.append("General")
            if response == "No" or response == "no":
                list5.append("N/A")

        elif (list4[index] == "Recruit" or list4[index] == "Corporal") and level > 599:
            list5.append("Sergeant")

        elif list4[index] == "Sergeant" and level > 899:
            list5.append("Lieutenant")

        elif list4[index] == "Lieutenant" and level > 1499:
            list5.append("Captain")

        else:
            list5.append("N/A")

        if list4[index] == list5[index]:
            list5[index] = "N/A"

    return list5


# ======================================== DATA PRINTING FUNCTION ===================================================


# Simply iterates through the relevant lists and prints out the data for each player. Also, adds a header to the
# table and formats the output to be more aesthetically pleasing.

def print_to_file(list1, list2, list3, list4, list5):

    file = open("TNC_Data.txt", "w+")

    file.write(
        "RSN               TOTAL LEVEL   DATE JOINED                              RANK                         NEW RANK\n")
    file.write(
        "==============================================================================================================\n")

    for i, j, k, m, n in zip(list1, list2, list3, list4, list5):
        line_print = "{:<15} {:^15} {:<40} {:<20} {:>15}".format(i, j, k, m, n)
        file.write(line_print + "\n")

    file.close()
