# lrc File Fetcher
A command line tool to create .lrc file for MP3 music files using synced lyrics fetched from the internet.

.lrc files contain lyrics for music along with timestamps to provie lyrics during playback. Generally music players (especially on smartphones) require that .lrc file  to be in the same directory as the mp3 music file and to have same name as the MP3 file.


## lrc-fetcher
lrc-file-fetcher searches for .mp3 files in the current directory and then searches for their synced lyrics one by one. The following sources are used for lyrics scrapping:
<ul>
<li>www.megalobiz.com</li>
<li>www.syair.info</li>
</ul>

It uses MP3 file names to create a query to search and displays a list of search results (destination url of search results, to be exact) from both websites. From there, the user can either select a search result or skip the prompt(no .lrc file will be created). If an url is selected, synced lyrics present in that destination url will be scraped to create a .lrc file with same name as the mp3 file. The same will be done for all the mp3 files in the current directory (provided they were not added after running the program).

  
## lrc-fetcher-automated
Automated file fetcher is a variation of original lrc file fetcher which does not depend on user input. It uses mp3 file name to search for song lyrics on www.syair.info and scraps lyrics from the first search result to create .lrc file.

 
## Prerequisites
<ul>
<li>Python 3 and above</li>
<li>Internet Connection</li>
</ul>

  
## Usage
Just execute the required python file : lrc_fetcher.py (or lrc_fetcher_automated.py for automated version)
~~~
python lrc_fetcher.py
~~~


## Effectiveness
.lrc files were created using lrc-fetcher-automated.py for around 420 songs:
<ul>
<li>Most of the .lrc files created were out of sync (mostly by a second or 2). Later, lrc file editor was used to sync them correctly.</li>
<li>For some of the songs, incorrect lyrics were fetched.</li>
<li>Correct and synced lyrics were also fetched (mostly for popular songs).</li>
</ul>

  
## Tips for getting more aacurate lyrics
<ul>
<li>Include both song title and artist name in Mp3 file name. (In above test, MP3 Tag was be used to rename MP3 files according to title and artist tags)  </li>
<li>Use non-automated version to manually choose right link from which lyrics will scrapped.</li>
</ul>


## Contribution
Feel free to review code, raise issues, make changes or enhance this project.
