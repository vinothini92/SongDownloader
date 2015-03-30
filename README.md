# SongDownloader

A script to automate the download of songs from rss feeds. To eliminate the manual way of downloading songs every time.

##How to use?
If you intend to use this script,install the packages and run the script

`# sudo pip install -r requirements.txt`

`$ python download.py "rss_feed_url" "destination_folder_to_save"`

#####Example:

`python download.py "http://songspka.in/tamil/tamil-mp3/feed/" "./songs"`

Add cron to run the script automatically.
---
`$ crontab -e`

`30 20 * * * python /path/to/script`

log file is created to monitor the run status.
