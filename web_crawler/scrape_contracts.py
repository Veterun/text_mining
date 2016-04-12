##################################################################################
#import modules

# for establishing a connection between python and the targeted website
import urllib2

# for retreiving information from websites 
from bs4 import BeautifulSoup as bs 

#convert xml as string to an ordered dictionary 
import xmltodict

# to read arguments from command line
import os 

#To use numpy arrays which are more efficient than regular data structures
import numpy as np

#To read the folder structure of the target
import sys


#import xml.etree.ElementTree as ET
#import json
##################################################################################

def get_xml_content(url):
    #Description: gets xml content from a url supplied
    #read supplied url and retrieve html
    #input: url - url to the xml version of data
    #output: An ordered dict of the xml data
    
    response = urllib2.urlopen(url).read()
    xml_dict = xmltodict.parse(response)
    return dict(xml_dict)


def scrape_contracts(xml_urls, file_prefix):
    #Uses a list of the xml url provided to scrape data from them and store to disk periodically
    #Writes various logs to monitor progress
    #input: xml_urls - a list of xml urls
    #output - None
    project_info = []
    
    for idx, url in enumerate(xml_urls):
        
        try:
            #try to retrieve information from url
            project_info.append(get_xml_content(url))
            
            #add completed url to the log of completed urls
            with open("./data/projects/completed_urls.txt", "a") as complete_file:
                complete_file.write(url + '\n')
                complete_file.close()
        except:
            #add rejected urls to the log of rejected urls
            with open("./data/projects/rejected_urls.txt", "a") as rejected_file:
                rejected_file.write(url + '\n')
                rejected_file.close()
        
        if idx % 10000 == 0 and idx != 0:
            #periodically write the data to file and reinitialise list for memory management
            file_name = './data/projects/'+ file_prefix + str(idx) + '.gz'
            np.savetxt(file_name, project_info, delimiter=',', fmt='%s')
            project_info = []
            
            #add the index of last file to be written to disk
            with open("./data/projects/saved_data_index.txt", "a") as saved_file:
                saved_file.write(file_prefix + str(idx) + '\n')
                saved_file.close()
    
    #Save remaining data to file    
    file_name = './data/projects/'+ file_prefix + str(idx) + '.gz'
    np.savetxt(file_name, project_info, delimiter=',', fmt='%s')
    with open("./data/projects/saved_data_index.txt", "a") as saved_file:
                saved_file.write(file_prefix + str(idx) + '\n')
                saved_file.close()
    
    
def main(argv):
    
    start_index = int(argv[0])
    end_index = int(argv[1])
    file_prefix = argv[2]
   
    xml_urls = np.loadtxt('./data/complete_xml_urls.gz', dtype=str)[start_index:end_index]
    scrape_contracts(xml_urls, file_prefix)
    
    
if __name__ == '__main__':
    main(sys.argv[1:])
