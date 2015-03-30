"""
****************************************

Python script to automate the download of songs using rss feeds

****************************************

"""
# coding=utf-8

import feedparser
import os
import urllib2
import argparse
import logging
import sys
import requests

class DownloadSongs(object):
    
    song_details = dict()
    
    def __init__(self, url,OUT_DIR,root_path):
        '''Initialise url and destination directory to store songs'''
        self.url = url
        self.OUT_DIR = OUT_DIR
        self.root_path = root_path
        self.logger = self.get_logger()
        self.logger.info("*********Program started************")
        self.logger.info("FEED URL---->%s"%self.url)
    
    def get_logger(self):
        logger = logging.getLogger('log')
        hdlr = logging.FileHandler('log'+ u'.log')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        logger.addHandler(hdlr)
        logger.setLevel(logging.INFO)
        return logger

    
    def parse_rssfeed(self):
        '''Parse the rss feeds. 
        
        Fetch the songs links
        return the details of songs as dict'''

        feed = feedparser.parse(self.url)
        if feed.status == 200:
            for item in feed.entries:
                song_links = []
                item_id = item.id
                item_name = item.title
                item_updated = item.updated 
                item_links = item.enclosures
                for link in item_links:
                    link = link['href'].encode('utf-8')
                    if link.endswith('.mp3'):
                        song_links.append(link)
                    else:
                        continue
                self.song_details[item_name] = song_links
            self.logger.info("URL is parsed")
        else:
            self.logger.info("Error in establishing connection")
            exit(0)
        return self.song_details
        
    def create_dir(self,new_dir):
        '''Function to create new directory for each movie.'''
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
            self.logger.info("New directory created")
        return new_dir
    
    def download(self,song_link,song_name):
        '''Download file using urllib2.'''
        try:
            response = urllib2.urlopen(song_link)
            file = response.read()  
            writing = open(song_name,"w")
            writing.writelines(file)
            writing.close()
        except urllib2.HTTPError, err:
            if err.code == 404:
                print err
                self.logger.info("404 not found error")
            else:
                self.logger.info(err)
        return True
    
    
    def fetch_songs(self,details):
        '''Iterate through song details and fetch it.'''
        
        for movie,songs in details.iteritems():
            temp_path =os.path.join(self.root_path,self.OUT_DIR,)
            new_dir = self.create_dir(os.path.join(temp_path,movie))
            os.chdir(new_dir)
            dir_content=list(os.listdir(os.getcwd()))
            for song_link in songs:
                normalized_url = urllib2.unquote(song_link)
                song_name = normalized_url.rsplit('/')[-1]
                if not  dir_content.__contains__(song_name):
                    self.logger.info("Song url-->%s"%song_link)
                    self.logger.info("-"*50+"\n"+song_name+" is downloading in "+movie.encode('utf-8'))
                    print "-"*50+"\n"+song_name+" is downloading in "+movie.encode('utf-8')
                    self.download(song_link,song_name)
                    dir_content.append(song_name)
                    self.logger.info("Done")
                    print "Done"
                else:
                    self.logger.info("-"*50+"\n")
                    self.logger.info("{} song already downloaded".format(song_name))
                    print "-"*50+"\n"
                    print "{} song already downloaded".format(song_name)
                print "\n"
        


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("url",help="feed url",type=str)
    parser.add_argument("out_dir",help="destination directory to store songs",type=str)
    args = parser.parse_args()
    root_path = os.getcwd()
    songs = DownloadSongs(args.url,args.out_dir,root_path)
    details = songs.parse_rssfeed()
    songs.fetch_songs(details)
    self.logger.info("**********Program Ends***********")
    
    

