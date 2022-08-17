from bs4 import BeautifulSoup
import requests
import pandas as pd


url = "https://www.imdb.com/chart/top/"
r = requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")


df = pd.DataFrame(columns=['Name','Year','Gener','Rating','Vote','Desciption','Stars','Director','Writers'])
a = 0
movieList = soup.find("tbody", attrs={"class":"lister-list"}).find_all("tr")
for movie in movieList:
    movieName = movie.find("td", class_ = "titleColumn").find("a").text
    movieYear = movie.find("td", class_ = "titleColumn").find("span").text.replace(")","").replace("(","")
    link = "https://www.imdb.com/" + movie.find("td", class_ = "titleColumn").a.get("href")
    
    urlOfMovie = requests.get(link)
    soup1 = BeautifulSoup(urlOfMovie.content,"html.parser")
    movDetails = soup1.find("div", class_ = "sc-2a827f80-10 fVYbpg")
    
    allMovieGener = movDetails.find("div", class_ = "ipc-chip-list__scroller").find_all("a")
    gener = []
    for n in allMovieGener:
        gener.append(n.span.text)
    movieGener = (",".join(gener))
    try:
        descirption = movDetails.find("p", class_ = "sc-16ede01-6 cXGXRR").span.text
    except AttributeError:
        descirption = "None"


    movieRate = movDetails.find("span", class_ = "sc-7ab21ed2-1 jGRxWM").text
    vote = movDetails.find("div", class_ = "sc-7ab21ed2-3 dPVcnq").text
    director = movDetails.ul.li.div.text
    writers = movDetails.ul.li.find_next_sibling().div.text
    allStars = movDetails.ul.li.find_next_sibling().find_next_sibling().div.ul.find_all("a")
    star = []
    for x in allStars:
        star.append(x.text)
    stars = (",".join(star))
    df = df.append({'Name': movieName,
                    'Year': movieYear,
                    'Gener' :movieGener,
                    'Rating' :movieRate,
                    'Vote': vote,
                    'Desciption' :descirption,
                    'Stars' : stars,
                    'Director' : director,
                    'Writers': writers}, ignore_index=True)
    a += 1
    print(a)
    df.to_csv("IMDbMovies.csv", index=False)