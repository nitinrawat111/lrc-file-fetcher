import requests
import os
from string import punctuation
import time

search_link_iteration_count = 5

website1 = "https://www.megalobiz.com"
website2 = "https://www.syair.info"

clear_screen_command = "cls" if  os.name == "nt" else "clear"

def clear_screen():
    os.system(clear_screen_command)

def getDataFromURL(url):
    # Site 2 rejects GET requests from python that do not identify as user agent
    # Thus, custom user-agent header needs to be defined to open the link properly 
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    webpage = requests.get(url, headers=headers)
    return webpage.text

def extractSongQueryFromFileName(mp3_file_name):
    mp3_file = mp3_file_name.replace(".mp3", "")
    for ch in mp3_file:
        if ch in punctuation or ch.isnumeric():
            mp3_file = mp3_file.replace(ch, " ")
    mp3_file = "+".join(mp3_file.split())
    return mp3_file

def scrap_search_result_links_from_site_1(first_search_page_data):
    linksarr = [] 
    link_start_index = 0
    link_end_index = 0
    iteration = 0
    while iteration <= search_link_iteration_count:  
                        link_start_index = first_search_page_data.find("href=\"/lrc", link_end_index) + 6
                        link_end_index = first_search_page_data.find("\"", link_start_index)
                        linksarr.append(first_search_page_data[link_start_index : link_end_index])
                        iteration = iteration + 1
    linksarr.pop(0)         #first link is not useful
    return linksarr

def scrap_search_result_links_from_site_2(second_search_page_data):
    linksarr = [] 
    link_start_index = 0
    link_end_index = 0
    iteration = 0
    while iteration < search_link_iteration_count:  
                        link_start_index = second_search_page_data.find("href=\"/lyrics", link_end_index) + 6
                        link_end_index = second_search_page_data.find("\"", link_start_index)
                        linksarr.append(second_search_page_data[link_start_index : link_end_index])
                        iteration = iteration + 1
    return linksarr

def scrap_lyrics_from_site_1(first_lyrics_page_data):
    lyrics_start_index = first_lyrics_page_data.find("[ve:v1.2.3]<br>") + 15
    lyrics_end_index = first_lyrics_page_data.find("</span>", lyrics_start_index)
    
    lyrics = first_lyrics_page_data[lyrics_start_index:lyrics_end_index].replace("<br>","")
    return lyrics

def scrap_lyrics_from_site_2(second_lyrics_page_data):
    lyrics_start_index = second_lyrics_page_data.find("class=\"entry\">") + 14
    lyrics_end_index = second_lyrics_page_data.find("<div class=\"line\">", lyrics_start_index)

    lyrics = second_lyrics_page_data[lyrics_start_index:lyrics_end_index].replace("<br>","")
    return lyrics


def extractSearchResultLinks(mp3_to_search):
    song_query = extractSongQueryFromFileName(mp3_to_search)
    search_link1 = "https://www.megalobiz.com/search/all?qry=" + song_query
    search_link2 = "https://www.syair.info/search?q=" + song_query
    
    first_search_page_data = getDataFromURL(search_link1)
    second_search_page_data = getDataFromURL(search_link2)

    linksarr = []
    linksarr.extend( scrap_search_result_links_from_site_1(first_search_page_data) )
    linksarr.extend( scrap_search_result_links_from_site_2(second_search_page_data) )
    return linksarr
    
def getLyricsLink(mp3_file):
    search_result_links = extractSearchResultLinks(mp3_file)
    serialnumber = 1
    for link in search_result_links:
        print(str(serialnumber) + ". "+ link)
        serialnumber += 1
    
    choice = int(input("Select any lyrics link (Press any other number to skip) : "))
    if(choice > 0 and choice <= search_link_iteration_count):
        return (website1 + search_result_links[choice - 1], "1")    #Return tuple containing link and another member to indicate website
    elif (choice > search_link_iteration_count and choice <= 2*search_link_iteration_count):
        return (website2 + search_result_links[choice - 1], "2")
    else:
        return ("", "0")

def getlyrics(mp3_file):
    lyrics_link_tuple = getLyricsLink(mp3_file)
    if(lyrics_link_tuple[0] == ""):
        return ""
    lyrics_page_data = getDataFromURL(lyrics_link_tuple[0])

    lyrics = ""

    if lyrics_link_tuple[1] == "1":
        lyrics = scrap_lyrics_from_site_1(lyrics_page_data)
    else:
        lyrics = scrap_lyrics_from_site_2(lyrics_page_data)

    return lyrics

def create_lrc(mp3_file_name):
    lyrics = getlyrics(mp3_file_name)
    if lyrics == "":
        print("Skipped!")
        return

    lrc_file_name = mp3_file_name.replace(".mp3", "")
    lrc_file_name = lrc_file_name + ".lrc"
    try:
        lrc_file = open(lrc_file_name, "x", encoding='utf-8')      #Need to open in encoded format to facilitate writing of web-scrapped data
    except:
        print("lrc file already exists!")
        return
    
    lrc_file.write(lyrics)
    lrc_file.close()
    print("lrc file created for " + mp3_file_name)


mp3_files_list = [file for file in os.listdir(".") if file.endswith(".mp3")]
print(str(len(mp3_files_list)) +" MP3 files found in current directory!")

choice = "a"
valid_choices = ["n", "N", "Y", "y"]

for mp3_file in mp3_files_list:
    while choice not in valid_choices:
        clear_screen()
        print("Mp3 file name : " + mp3_file)
        choice = input("Do you want to create .lrc file for this file(y/n) : ")
        if choice == "y" or choice == "Y":
            create_lrc(mp3_file)
        elif choice == "n" or choice == "N":
            print("Ok")
        else:
            print("Invalid input!")
        
        input("Press Enter to continue..")
    
    choice = "a"

print("Finished!!!")