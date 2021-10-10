import urllib.parse
import requests
from requests.structures import CaseInsensitiveDict
from prettytable import PrettyTable


# Setting the standard variables needed for this program
baseurl = "https://api.themoviedb.org/4"
headers = CaseInsensitiveDict()
output = PrettyTable()
json_status = ""
movie_status = 0

loginURL = baseurl + "/auth/request_token"

# Printing the start and asking for the personal API key. If this key is not correct, the program will ask again.
print("Welcome to The Movie Database.\nSearch for any movie you like!\nMade by Brent Van der Steen - R0704384\n")

while json_status != 1:
    key = input("Please enter your personal API key: ")
    headers["Authorization"] = "Bearer " + key
    login_data = requests.post(loginURL, headers=headers).json()
    json_status = login_data["status_code"]

    # If the user entered a valid API key the program will continue.
    if json_status != 1:
        print("There seems to be something wrong with your API key. Please try again.")
    else:
        print("You have successfully logged in.\n")
        break

# The user is asked to enter a title of a movie they are searching for. If there are no results found, the program will retry.
while movie_status == 0:
    moviequery = input("What movie are you searching for? ")
    movieurl = baseurl + "/search/movie?" + urllib.parse.urlencode({"query":moviequery})
    movie_data = requests.get(movieurl, headers=headers).json()
    movie_status = movie_data["total_results"]
    if movie_status == 0:
        print("There are no movies found for this name.")
    else:
        output.field_names = ["Movie Title", "Popularity", "Release date", "Score"]
        for results in movie_data["results"]:
            output.add_row([results["title"], results["popularity"], results["release_date"], results["vote_average"]])
        print(output)
        break

print("Thank you for using my program. Made by Brent Van der Steen")
