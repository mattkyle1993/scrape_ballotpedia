from selenium import webdriver      
# from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.keys import Keys
import time
import psutil
import os
from lxml import etree
from lxml import html
import urllib.request
import http
import urllib
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
import math
from piapy import PiaVpn
import random
import json
from dateutil import parser
import pandas as pd
import http.cookiejar as cookiejar
from urllib.request import urlopen
import requests
import cv2
import pytesseract
from fuzzywuzzy import fuzz, string_processing
from fuzzywuzzy import process

# URLS
# https://ballotpedia.org/List_of_current_members_of_the_U.S._Congress

# IDEALLY
# grab table element
# grab each column and their elements, append to list (name, office name, party, state, legislator url)
# zip up the lists and each row is a different legislator
# go through each legislator url, grab facebook links, make a dictionary and append to list
# merge all dictionaries togother into dataframe
# save as CSV

def save_final_csv(curr_direct,final_name):
    df_list = []
    for filename in os.listdir(f"{curr_direct}"):
        if filename.endswith(".csv"):
            filename = f"{curr_direct}" + filename
            df = pd.read_csv(filename)
            df_list.append(df)
    final_df = pd.concat(df_list,ignore_index=True)
    final_csv_name = curr_direct + final_name + ".csv"
    final_df.to_csv(final_csv_name)
    print("saved final_df to:",final_csv_name)

def get_selenium_driver(minimize=True):
    """
    returns webdriver so selenium can be implemented more easily
    """
    WEBDRIVER_PATH = r"C:\Users\mattk\Documents\GitHub\ballotpedia\webdriver\chromedriver-win64\chromedriver.exe"
    webdriver_path = WEBDRIVER_PATH
    service = Service(executable_path=webdriver_path)
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    # options.add_argument("--headless")
    # options.add_argument("--use_subprocess")
    driver = webdriver.Chrome(service=service, options=options)    
    if minimize == True:
        driver.minimize_window()
    return driver

def get_beautiful_soup(url,):
    params = {
                    "building_condition": "3%7C8%7C4",
                    "category_main_cb": "1",
                    "category_sub_cb": "2%7C3%7C4%7C5%7C6%7C7%7C8%7C9%7C10%7C11%7C12%7C16",
                    "category_type_cb": "1",
                    "locality_region_id": "10",
                    "per_page": "20",
                    "tms": "1592389441017"
            }
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    prettyHTML = soup.prettify()  
    soup = BeautifulSoup(prettyHTML, 'html.parser')
    return soup

def run_vpn(chromedriver=False):
    
    program_directory = [
        "C:\\Program Files\Private Internet Access\pia-client.exe",
        "C:\\Users\mattk\Desktop\streaming_data_experiment\chromedriver_win32\chromedriver.exe"]
    program_name = ["VPN","CHROMEDRIVER"]
    if chromedriver == True:
        program_list = ["pia-client.exe","chromedriver.exe"]
    if chromedriver == False:
        program_list = ["pia-client.exe"]
    
    ct = -1
    for program in program_list:
        ct += 1
        wait_seconds = 10
        process_list = [p.name() for p in psutil.process_iter()]
        print("checking if VPN is running:")
        print("---------------------------"*5)
        if program not in process_list:
            print(f"...{program_name[ct]} not running...")
            print(f"...starting {program}...")
            os.startfile(program_directory[ct])
            print(f"...waiting for program {program_name[ct]} to start before scraping...")
            time.sleep(wait_seconds)
            process_list = [p.name() for p in psutil.process_iter()]
            if program in process_list:
                if "pia" in program:
                    print("...vpn has started. now activating private IP address...")
                    print(f"...waiting for {wait_seconds} seconds vpn to activate private IP addess...")
                    time.sleep(wait_seconds)
                    print("...wait complete!")
            if "pia" in program:
                print("error")
            else:
                pass
        else:
            print(f"...{program_name[ct]} running!")

# class BallotpediaGrabSchoolBoard():
class ScrollThePage():
    def __init__(self):
        self.scroll_range = 1000
        self.latter_height = 0
        self.current_url_ = ""
    def scroll_the_page(self,driver,scroll_fresh_start=False,scroll_start_insert=0):
        """
        Scrolls a page by certain incremental ranges. Will scroll the same page if it's the same URL and same driver as long as it's called properly. 
        I.e., implement this throughout the code and it should work throughout the logic.

        driver : selenium driver to take and return
        scroll_fresh_start (bool) : resets self.latter_height range to 0 so it scrolls from the top of the page.
        scroll_start_insert (int) : if 0, scrolls from top of page. Else, that's the starting bound for the scroll to start on.
        """
        self.current_url_ = driver.current_url
        if driver.current_url == self.current_url_:
            self.latter_height = self.latter_height
        else:
            print("detecting new url. reseting self.latter_height to 0")
            self.latter_height = 0
        total_height = int(driver.execute_script("return document.body.scrollHeight"))
        shorter_height = total_height * .65
        shorter_height = math.floor(shorter_height)
        # self.scroll_range = self.scroll_range + self.latter_height
        pass_up = False
        if scroll_fresh_start == True:
            self.latter_height = 0
        if self.latter_height == 0:
            if scroll_start_insert == 0:
                scroll_bound_start = 0
            if scroll_start_insert > 0:
                scroll_bound_start = scroll_start_insert
                self.latter_height = scroll_bound_start
                pass_up = True
        if pass_up == False:
            if self.latter_height > 0:
                scroll_bound_start = self.latter_height
        for i in range(1, shorter_height, 3):
            if i < self.scroll_range:
                driver.execute_script("window.scrollTo({scroll_bound_start}, {range_increment});".format(scroll_bound_start=scroll_bound_start,range_increment=i))
            else:
                break
        self.latter_height += self.scroll_range
        return driver

class BallotpediaDataGrabber():
    """
    this URL:    https://ballotpedia.org/List_of_current_members_of_the_U.S._Congress
    """
    import sys
    sys.setrecursionlimit(200000)
    def __init__(self,sleep_seconds=3,fuzzy_thresh=80,legists_fuzzy_list=[],curr_direct="",test_run=True,test_run_count=15,selenium_minimize=True):
        self.legists_fuzzy_list = legists_fuzzy_list
        self.sleep_seconds = sleep_seconds
        self.fuzzy_thresh = fuzzy_thresh
        self.curr_direct = curr_direct
        self.test_run = test_run
        self.test_run_count = test_run_count
        self.selenium_minimize = selenium_minimize
    def get_fb_urls(self,url,return_soup=False):
        soup = get_beautiful_soup(url=url)
        a_elements = soup.find_all('a')
        fb_urls = []
        for a in a_elements:
            url = a.get('href')
            if url:
                if "facebook" in url.lower():
                    if "ballotpedia" not in url.lower():
                        if url not in fb_urls:
                            fb_urls.append(url)
        if return_soup == False:
            return fb_urls
        if return_soup == True:
            return fb_urls,soup
    def search_for_state_or_federal_legislator(self,searched_name,fuzzy_threshold=80,government_level="federal"):
        """
        uses fuzzy wuzzy to search for legislator. returns a list of potential matches and their data. 
        """
        def return_legist_element_screenshot(legist_url,state_search=False):
            """
            screencap given legist url, return info
            """
            if state_search == False:
                the_url = "https://ballotpedia.org/List_of_current_members_of_the_U.S._Congress"
            else:
                the_url = legist_url[1]
            driver = get_selenium_driver(minimize=self.selenium_minimize) 
            driver.get(the_url)
            tr_element=driver.find_element(By.XPATH,f"//tr[.//td//a[@href='{legist_url}']]") 
            driver.implicitly_wait(3)
            chng_url = legist_url.replace("https://ballotpedia.org/","")
            screencap_name = f"searched_politician_screenshot/screencap_{chng_url}.png"
            tr_element.screenshot(screencap_name)
            pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"
            config = ("-l eng — oem 1 — psm 3")
            def inverte(imagem, name):
                imagem = (255-imagem)
                cv2.imwrite(name, imagem)
            filename1 = screencap_name
            filename2 = f'searched_politician_screenshot/invert/screencap_{legist_url.replace("https://ballotpedia.org/","")}.png'
            img = cv2.imread(filename1)
            inverte(img,filename2)
            img = cv2.imread(filename2)
            text = pytesseract.image_to_string(img, config=config)
            if "repub" not in text.lower():
                if "indepen" not in text.lower():
                    text = text.strip() + "Democratic Party"
                    print(f"Search results here for {searched_name}: ",text)
            else:
                print(f"Search results here for {searched_name}: ",text)

        def get_fuzz_match_individ(search_name,legist_list,f_thresh=fuzzy_threshold,print_=True):
            """
            matches legislator name from url to legislator name in table element screenshot
            """
            legist_list = legist_list
            matches = process.extract(search_name, legist_list, limit=1)
            matches = [(word, score) for word, score in matches if score >= f_thresh]
            if matches:
                for word, similarity_score in matches:
                    if print_ == True:
                        print("FUZZY WUZZY STRING MATCH SUCCESS.")
                        print(f"SEARCHED NAME: {search_name}. MATCHED AND FOUND WORD: {word}. SIMILARITY SCORE: {similarity_score}.")
                    legist_url = "https://ballotpedia.org/" + word
                    final_name = word.replace("_"," ")
                    verdict = final_name
                    return legist_url,verdict
            else:
                thresh_anty_ct=1
                curr_thresh = f_thresh
                verdict = ""
                for i in range(1,4):
                    thresh_anty_ct = i
                    step_down_thresh = curr_thresh - 5*thresh_anty_ct
                    print("step_down_thresh:",step_down_thresh)
                    legist_url, final_name = get_fuzz_match_individ(search_name,f_thresh=step_down_thresh,print_=True,legist_list=legist_list)
                    if final_name != "try_again":
                        break
                    if thresh_anty_ct == 3:
                        if verdict == "try_again":
                            verdict = "set_aside"
                            print("failed to find a match")
                            break
                return legist_url,verdict
        if government_level == "federal":
            search_federal = True
        else:
            search_federal = False
            search_states = True
        if search_federal == True:
            federal_url = "https://ballotpedia.org/List_of_current_members_of_the_U.S._Congress"
            soup = get_beautiful_soup(url=federal_url)
            table_htmls = soup.find_all('table',{"id":"officeholder-table"}) 
            federal_legist_hrefs = []
            for num in [0,1]:
                table = table_htmls[num]
                a_elements = table.find_all("a",href=True)  
                for a_element in a_elements:
                    h = a_element['href']
                    if h is not None:
                        if "List_of" not in h:
                            if "Non-Voting" not in h:
                                if "Congressional_District" not in h:
                                    if "Guam" not in h:
                                        if "Northern_Mariana" not in h:
                                            if"Virgin_Islands%27" not in h: 
                                                if "congressional_delegations_from_North_Dakota" not in h:
                                                    h = h.strip(".")
                                                    if h not in federal_legist_hrefs:
                                                        federal_legist_hrefs.append(h)    
            fed_legist_names = [nam.replace("https://ballotpedia.org/","") for nam in federal_legist_hrefs]    
            the_legist_url,verdict = get_fuzz_match_individ(search_name=searched_name,legist_list=fed_legist_names)
            if verdict != "set_aside":
                return_legist_element_screenshot(legist_url=the_legist_url)
                fb_urls = self.get_fb_urls(url=the_legist_url)
                if len(fb_urls) > 0:
                    print("fb urls found:",fb_urls)
                else:
                    print("no facebook links found")
                return True
            else:
                search_states = True
        if search_states == True:
            state_legist_hrefs = []
            states, state_groups_urls, headers = self.return_states_list_and_stage_groups_urls()
            curr_state = "n/a"
            state_house_urls = ["THESTATE_House_of_Representatives","THESTATE_State_Senate"]
            for state_url in state_groups_urls:
                for state in states:
                    if state in state_url:
                        curr_state = state
                        break
                for house_url in state_house_urls:
                    if curr_state == "Nebraska":
                        state_url = "https://ballotpedia.org/Nebraska_State_Senate_(Unicameral)"
                    else:
                        state_url = house_url.replace("THESTATE",curr_state)
                        state_url = "https://ballotpedia.org/" + state_url
                    headers['Referer'] = '{main_url}'.format(main_url=state_url)
                    request = urllib.request.Request(state_url,headers=headers)  
                    opener = urllib.request.build_opener()
                    time.sleep(self.sleep_seconds)
                    filtered_html = etree.HTML(opener.open(request).read())
                    table_element = filtered_html.xpath('//*[@id="officeholder-table"]') 
                    element = table_element[0]
                    a_elements = element.xpath(".//a") 
                    for a_element in a_elements:
                        h = a_element.get("href")
                        if h is not None:
                            if "district" not in h.lower():
                                h = h.strip(".")
                                if h not in state_legist_hrefs:
                                    state_legist_hrefs.append((h.replace("https://ballotpedia.org/",""),state_url))
            state_legist_names = [nam[0] for nam in state_legist_hrefs]
            the_legist_url,verdict = get_fuzz_match_individ(search_name=searched_name,legist_list=state_legist_names)
            if verdict != "set_aside":
                return_legist_element_screenshot(legist_url=the_legist_url)
                fb_urls = self.get_fb_urls(url=the_legist_url)
                if len(fb_urls) > 0:
                    print("fb urls found:",fb_urls)
                else:
                    print("no facebook links found")
                return True
            else:
                print("failed to find:", searched_name)
                return False


    def grab_political_recall_efforts_2024(self,):
        """
        grab candidates/legistlators for political recall elections in 2024
        """
        states = self.return_states_list_and_stage_groups_urls
        soup = get_beautiful_soup(url="https://ballotpedia.org/Political_recall_efforts,_2024")
        recall_elements = soup.find_all('a',{"title":re.compile('recall')},recursive=True)
        hrefs = []
        for recall in recall_elements:
            href = recall.get("href")
            hrefs.append(href)
        all_recall_candidates = []
        for h in hrefs:
            soup = get_beautiful_soup(h)
            for state in states:
                match = re.search(state,h)
                if match:
                    curr_state = match
                    break 
                
            voteboxes = soup.find_all("td",{"class":"votebox-results-cell--text"})
            for vote in voteboxes:
                ref = vote.get('href')
                fb_urls = self.get_fb_urls(url=ref)
                pers_dict = {
                    "name":ref.replace("https://ballotpedia.org/",""),
                    "state":curr_state,
                    "recall_campaign":h.replace("https://ballotpedia.org/","")
                }
                for i in range(1,4):
                    try:
                        pers_dict[f'Facebook Link {i}'] = fb_urls[i]
                    except:
                        pers_dict[f'Facebook Link {i}'] = "N/A"
                recall_df = pd.DataFrame(pers_dict)
                all_recall_candidates.append(recall_df)
        recall_final_df = pd.concat(all_recall_candidates,axis=1)
        recall_final_df.to_csv("recall_elections/recall_candidates_2024.csv")

    def ballotpedia_grab_federal_level_computer_vision(self,read_image=False,fuzzy_threshold=80):

        def run_grab_tr_element_screenshots(the_url):
            """
            screenshot all TR elements
            """
            driver = get_selenium_driver(minimize=self.selenium_minimize) 
            driver.get(the_url)
            tr_elements=driver.find_elements(By.XPATH,'//tbody//tr') 
            driver.implicitly_wait(3)
            ct=0
            # tr_tuple_list = []
            for tr in tr_elements:
                if ct == 10:
                    time.sleep(10)
                screencap_name = f"tr_screenshots/test_{ct}.png"
                tr.screenshot(screencap_name)
                ct+=1
                # href = tr.get_attribute("href")
                # for h in href:
                #     if "senator" not in h.lower():
                #         if "district" not in h.lower():
                #             tupe_ = (screencap_name,h)
                #             if tupe_ not in tr_tuple_list:
                #                 tr_tuple_list.append(tupe_)
        def get_fuzz_match(name,f_thresh,print_=True):
            """
            matches legislator name from url to legislator name in table element screenshot
            """
            matches = process.extract(name, self.legists_fuzzy_list, limit=1)
            matches = [(word, score) for word, score in matches if score >= f_thresh]
            if matches:
                for word, similarity_score in matches:
                    if print_ == True:
                        print(f"QUERY:{name}. {word}: {similarity_score}")
                    legist_url = "https://ballotpedia.org/" + word
                    self.legists_fuzzy_list = [leg for leg in self.legists_fuzzy_list if leg != word]
                    final_name = word.replace("_"," ")
                    return legist_url,final_name
            else:
                final_name = "try_again"
            if final_name == "try_again":
                thresh_anty_ct=1
                curr_thresh = f_thresh
                for i in range(1,4):
                    thresh_anty_ct = i
                    step_down_thresh = curr_thresh - 5*thresh_anty_ct
                    print("step_down_thresh:",step_down_thresh)
                    legist_url, final_name = get_fuzz_match(name,f_thresh=step_down_thresh,print_=True)
                    if final_name != "try_again":
                        break
                    # else:
                    #     thresh_anty_ct+=1
                    if thresh_anty_ct == 3:
                        if final_name == "try_again":
                            final_name = "set_aside"
                            break
            return legist_url,final_name

        params = {
            "building_condition": "3%7C8%7C4",
            "category_main_cb": "1",
            "category_sub_cb": "2%7C3%7C4%7C5%7C6%7C7%7C8%7C9%7C10%7C11%7C12%7C16",
            "category_type_cb": "1",
            "locality_region_id": "10",
            "per_page": "20",
            "tms": "1592389441017"
            }
        states, _,_ = self.return_states_list_and_stage_groups_urls()
        soup = get_beautiful_soup(url="https://ballotpedia.org/List_of_current_members_of_the_U.S._Congress")
        table_htmls = soup.find_all('table',{"id":"officeholder-table"})
        legist_hrefs = []
        for num in [0,1]:
            table = table_htmls[num]
            # find url for legislator # 
            a_elements = table.find_all("a",href=True)  
            for a_element in a_elements:
                h = a_element['href']
                if h is not None:
                    # etc, etc, etc.

                    if "List_of" not in h:
                        if "Non-Voting" not in h:
                            if "Congressional_District" not in h:
                                if "Guam" not in h:
                                    if "Northern_Mariana" not in h:
                                        if"Virgin_Islands%27" not in h: 
                                            if "congressional_delegations_from_North_Dakota" not in h:
                                                h = h.strip(".")
                                                if h not in legist_hrefs:
                                                    legist_hrefs.append(h)    
        if read_image == True:
            # take screen shots
            run_grab_tr_element_screenshots(the_url="https://ballotpedia.org/List_of_current_members_of_the_U.S._Congress")
            pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"
            config = ("-l eng — oem 1 — psm 3")
            senate_range = range(23,123)
            house_range = range(139,579)
            def inverte(imagem, name):
                imagem = (255-imagem)
                cv2.imwrite(name, imagem)

            the_whole_range = []
            [the_whole_range.append(i) for i in senate_range]
            [the_whole_range.append(i) for i in house_range]
            republicans = []
            independents = []
            democratics = []
            ct=0
            for i in the_whole_range:
                if self.test_run == True:
                    if ct >= self.test_run_count:
                        break
                left_num = len(the_whole_range) - ct
                print(f"Message:_{left_num}_ images left to extract text from.")
                filename1 = f'tr_screenshots/test_{i}.png'
                filename2 = f'tr_screenshots/invert/invert_images/test_{i}.png'
                img = cv2.imread(filename1)
                inverte(img,filename2)
                img = cv2.imread(filename2)
                text = pytesseract.image_to_string(img, config=config)
                if "Indepen" in text:
                    independents.append(text)
                if "Republi" in text:
                    republicans.append(text)
                if "Republi" not in text:
                    if "Indepen" not in text:
                        democratics.append(text)
                ct+=1

            all_legislators = republicans + independents + democratics
            with open("tr_screenshots/invert/all_image_texts.txt","w",encoding="utf-8") as f:
                for line in all_legislators:
                    f.write(f"{line}\n")
        if read_image == False:
            all_legislators = []
            # with open("tr_screenshots/invert/all_image_texts.txt", 'r', encoding="utf-8") as file:
            with open("tr_screenshots/invert/all_image_texts copy 3.txt", 'r', encoding="utf-8") as file:
                while line := file.readline():
                        all_legislators.append(line.rstrip().strip())
            if self.test_run == True:
                t_run_ct = self.test_run_count + 1
                all_legislators = all_legislators[0:t_run_ct]
        for all_ in all_legislators:
            for remove_ in ["Non-Voting","Guam","Mariana Islands","Samoa"]:
                if remove_ in all_:
                    all_legislators.remove(all_)
        legist_dict_list = []
        under_states, no_under_states, _, _ = self.return_states_list_and_stage_groups_urls(split_states=True)
        for i in all_legislators:
            if i.strip() != "":
                i = i.strip()
                pass_by = False
                failed = False
                if pass_by == False:
                    if "Indepen" in i:
                        pass_by = True
                        the_party = "Indepen"
                if pass_by == False:
                    if "Republi" in i:
                        the_party = "Republi"
                        pass_by = True
                if pass_by == False:
                    if "Republi" not in i:
                        if "Indepen" not in i:
                            the_party = "assume democratic"
                            pass_by = True
                text_list = i.split(" ")
                for text in text_list:
                    if text == "lowa":
                        text = "Iowa"
                    if text.startswith("Republi"):
                        text_list.remove(text)
                    if text.startswith("Indepen"):
                        text_list.remove(text)
                if "Senate" in i:
                    pass_through = False
                if "U.S. House" in i:
                    pass_through = True
                if "US. House" in i:
                    pass_through = True
                if pass_through == True:
                    fin_party = ""
                    for state in no_under_states:
                        state = state.strip()
                        if state in i:
                            house_len = 5
                            pol_test = " ".join(text_list[0:house_len])
                            if pol_test[-1].isnumeric() == True:
                                house_len = 5
                                break
                            if pol_test[-1].isnumeric() == False:
                                house_len = 6
                                break
                    for state in under_states:
                        state = state.replace("_"," ")
                        if state in i:
                            if "At-Large" in i:
                                house_len = 7
                            if "At-Large" not in i:
                                house_len = 6
                    if house_len == 1:
                        print("house len == 1:"," ".join(text_list))
                    if house_len != 1:
                        fin_party = ""
                        pol = " ".join(text_list[0:house_len])
                        name = text_list[house_len:]
                        if the_party in ["Indepen","Republi"]:
                            name = " ".join(name)
                            if the_party == "Indepen":
                                fin_party = "Independent"
                            if the_party == "Republi":
                                fin_party = "Republican party"
                        else:
                            name = " ".join(name)
                            fin_party = "Democratic Party"
                if pass_through == False:
                    sen_len = 1
                    for state in no_under_states:
                        state = state.strip()
                        if state in i:
                            sen_len = 3
                    for state in under_states:
                        state = state.replace("_"," ")
                        state = state.strip()
                        if state in i:
                            sen_len = 4
                    if sen_len != 1: 
                        fin_party = ""
                        pol = " ".join(text_list[0:sen_len])
                        name = text_list[sen_len:]
                        if the_party in ["Indepen","Republi"]:
                            name = " ".join(name)
                            if the_party == "Indepen":
                                fin_party = "Independent"
                            if the_party == "Republi":
                                fin_party = "Republican party"
                        else:
                            name = " ".join(name)
                            fin_party = "Democratic Party"
                if type(name) == type([]):
                    failed = True
                if failed == False:
                        legist_dict = {
                            "legistlator":name,
                            "political_office":pol,
                            "party":fin_party
                        }
                        legist_dict_list.append(legist_dict)
        set_aside = []
        legists = [legist.replace("https://ballotpedia.org/","") for legist in legist_hrefs]
        legists = [legist.replace("_"," ") for legist in legists]
        # get rid of quotes in the names. 
        self.legists_fuzzy_list = legists
        for legist_dict in legist_dict_list:
            name = legist_dict['legistlator'].strip()
            if "vacant" in name.lower():
                name = ["loser! ha ha"]
                name = []
            if len(name) >= 1:
                curr_thresh = fuzzy_threshold
                final_name = ""
                # set_aside = False
                try:
                    if "ea CONCHIevm" not in name:
                        if "EGC ecceme" not in name:
                            # if "Jim Baird" not in name: # Mike Brau # chris murphy/chris deluzio # mike gallagher/mike thompson # dick durbin/rick larsen # bennie Thompson/Mike thompson
                                # D. Adam Smith/ Jason Smith (Missouri)
                                legist_url, final_name = get_fuzz_match(name,f_thresh=curr_thresh)
                    if final_name == "set_aside":
                        set_aside.append(legist_url)
                    else:
                        fb_urls = self.get_fb_urls(url=legist_url)
                        url_name = name.replace("","_")
                        legist_dict['legist_url'] = "https://ballotpedia.org/" + url_name
                        # add facebook links to legislator dicts
                        for i in range(1,6):
                            try:
                                legist_dict[f'Facebook Link {i}'] = fb_urls[i]
                            except:
                                legist_dict[f'Facebook Link {i}'] = "N/A"
                        df = pd.DataFrame(legist_dict,index=['legislator'])
                        final_name = final_name.replace('"','')
                        df.to_csv(f"federal_level_csvs/house_and_senate/{final_name}_federal_legislator.csv")
                        self.curr_direct = "federal_level_csvs/house_and_senate/"
                except Exception as error:
                    print("Error in fuzz match process:",str(error))
                    print("possible name error:",name)
                    set_aside.append(name)

        print("set_aside:",[set_ for set_ in set_aside])
    def return_states_list_and_stage_groups_urls(self,split_states=False):
        urls = pd.read_excel("BPStateLegislaturePages.xlsx",)
        urls.rename(columns={"House":"ballotpedia_url"},inplace=True)
        state_groups_urls = urls['ballotpedia_url'].tolist()
        headers = {
                        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                        'Accept-Encoding': 'none',
                        'Accept-Language': 'en-US,en;q=0.8',
                        'Connection': 'keep-alive',
                        'Referer': ''
                    }
        states = [
            'alabama', 'alaska', 'arizona', 'arkansas', 'california', 'colorado', 'connecticut', 'delaware',
            'florida', 'georgia', 'hawaii', 'idaho', 'illinois', 'indiana', 'iowa', 'kansas', 'kentucky',
            'louisiana', 'maine', 'maryland', 'massachusetts', 'michigan', 'minnesota', 'mississippi', 'missouri',
            'montana', 'nebraska', 'nevada', 'new_hampshire', 'new_jersey', 'new_mexico', 'new_york',
            'north_carolina', 'north_dakota', 'ohio', 'oklahoma', 'oregon', 'pennsylvania', 'rhode_island',
            'south_carolina', 'south_dakota', 'tennessee', 'texas', 'utah', 'vermont', 'virginia', 'washington',
            'west_virginia', 'wisconsin', 'wyoming'
        ]
        states = [' '.join([part.capitalize() for part in state.split('_')]) for state in states]
        under_states = [state.replace(" ","_") for state in states if state.count(" ") == 1]
        no_under_states = [state for state in states if state.count(" ") == 0]
        states = under_states + no_under_states

        if split_states == True:
            return under_states, no_under_states, state_groups_urls,headers
        if split_states == False:
            return states, state_groups_urls,headers

    def ballotpedia_grab_state_level(self,):
        """
        grab state level legistlator data
        """
        def find_years(text):
            # Regular expression pattern for a four-digit year
            pattern = r'\b[0-9]{4}\b'
            years = re.findall(pattern, text)
            return years

        currentyear = 2024 # get years left of term 
        states, state_groups_urls, headers = self.return_states_list_and_stage_groups_urls()
        curr_state = "n/a"
        state_house_urls = ["THESTATE_House_of_Representatives","THESTATE_State_Senate"]
        vacant_ct = 0
        legist_tupes_list = []
        if self.test_run == True:
            states = states[0]
        for state_url in state_groups_urls:
            for state in states:
                if state in state_url:
                    curr_state = state
                    break
            legist_hrefs = []
            districts_list = []
            legist_term_begins = []
            for house_url in state_house_urls:
                if curr_state == "Nebraska":
                    state_url = "https://ballotpedia.org/Nebraska_State_Senate_(Unicameral)"
                else:
                    state_url = house_url.replace("THESTATE",curr_state)
                    state_url = "https://ballotpedia.org/" + state_url
                headers['Referer'] = '{main_url}'.format(main_url=state_url)
                print(state_url)
                request = urllib.request.Request(state_url,headers=headers)  
                opener = urllib.request.build_opener()
                time.sleep(self.sleep_seconds)
                filtered_html = etree.HTML(opener.open(request).read())
                table_element = filtered_html.xpath('//*[@id="officeholder-table"]') 
                # //* means by agnostic about the leading tag so long as the id of the html tag corresponds to the string
                element = table_element[0]
                a_elements = element.xpath(".//a") 
                #.// means grab all a tags
                for a_element in a_elements:
                    h = a_element.get("href")
                    if h is not None:
                        if "district" not in h.lower():
                            h = h.strip(".")
                            if h not in legist_hrefs:
                                legist_hrefs.append(h)
                                print(h)
                a_elements = element.xpath(".//a")  
                for a_element in a_elements:
                    a_elem = a_element.text
                    if "district" in a_elem.lower():
                        if a_elem not in districts_list:
                            districts_list.append(a_elem)
                td_elements = element.xpath(".//td") 
                iii=0
                for td_element in td_elements:
                    if td_element is not None:
                            td_elemen = td_element.text
                            if td_elemen != None:
                                if td_elemen == "Vacant":
                                    years_in_office = 0
                                    legist_term_begins.append((td_elemen,years_in_office))
                                    legist_hrefs.insert(iii,"www.vacantdistrict.com")
                                    print("vacant!")
                                    iii+=1
                                    vacant_ct += 1
                                td_elemen = find_years(td_elemen)
                                if td_elemen:
                                    years_in_office = currentyear - int(td_elemen[0])
                                    legist_term_begins.append((str(td_elemen[0]),years_in_office))
                                    iii+=1
                print("vacant count:",vacant_ct)
                for legist_url, district, legist_begin in zip(legist_hrefs,districts_list,legist_term_begins):
                    if (legist_url,district,legist_begin[0],legist_begin[1]) not in legist_tupes_list:
                        legist_tupes_list.append((legist_url,district,legist_begin[0],legist_begin[1]))
            params = {
                "building_condition": "3%7C8%7C4",
                "category_main_cb": "1",
                "category_sub_cb": "2%7C3%7C4%7C5%7C6%7C7%7C8%7C9%7C10%7C11%7C12%7C16",
                "category_type_cb": "1",
                "locality_region_id": "10",
                "per_page": "20",
                "tms": "1592389441017"
                }
            legis_dict_list = []
            len_legis_hrefs = len(legist_hrefs)
            for legist_tupe in legist_tupes_list:
                if legist_tupe[0] == "www.vacantdistrict.com":
                    len_legis_hrefs -= 1
                if legist_tupe[0] != "www.vacantdistrict.com":
                    fb_urls,soup = self.get_fb_urls(url=legist_tupe[0],return_soup=True)
                    prettyHTML = soup.prettify()
                    all_tags_individ = []
                    for tag in prettyHTML:
                        pattern = r'<[^>]+>'
                        tags_ = re.findall(pattern, str(tag))
                        for tag_ in tags_:
                            all_tags_individ.append(str(tag_))
                    start_tag = soup.find('div', class_='infobox person')
                    final_text = ''.join(str(start_tag).split())
                    the_parties = ['Republican','Independent','Democratic',"Independent","Nonpartisan"]
                    the_party = "n/a"
                    for party in the_parties:
                        if party.lower() in final_text.lower():
                            if party == "Republican":
                                the_party = party + " Party"
                            if party == "Democratic":
                                the_party = party + " Party"
                            else:
                                the_party = party
        
                    final_text = re.sub(r'<[^>]+>', ' ', final_text)
                    if "House" and "Representatives" in legist_tupe[1]:
                        curr_state_regex_str = curr_state.replace("_","") + "House"
                    if "State" and "Senate" in legist_tupe[1]:
                        curr_state_regex_str = curr_state.replace("_","") + "State"
                    final_text = re.sub(rf'.*?{re.escape(curr_state_regex_str)}', '', final_text)
                    final_text = re.sub(r'Contact.*', '', final_text)    
                    try:
                        pass_ = False
                        try:
                            if "Tenure" in final_text:
                                district = re.search(r".*?Tenure", final_text)   
                                district = district.group(0).replace("Tenure","").replace(" ","")
                                pass_ = True
                            if pass_ == False:
                                if "Successor" in final_text:
                                    district = re.search(r".*?Successor", final_text)   
                                    district = district.group(0).replace("Successor","").replace(" ","")
                        except:
                            district = "N/A: see url:{legis_url}".format(legis_url=legist_tupe[0])
                    except:
                        district = "N/A: see url:{legis_url}".format(legis_url=legist_tupe[0])
                    final_text_yrspstn = final_text + " Yearsinposition"
                    try:
                        start_substring = 'Tenure'
                        end_substring = 'Termends'
                        tenure = re.search(f"{re.escape(start_substring)}(.*?){re.escape(end_substring)}",final_text)
                        tenure = tenure.group(1).strip().replace(" ","")
                    except:
                        tenure = "N/A: see url:{legis_url}".format(legis_url=legist_tupe[0])
                    try:
                        start_substring = 'Termends'
                        end_substring = 'Yearsinposition'
                        term_ends = re.search(f"{re.escape(start_substring)}(.*?){re.escape(end_substring)}",final_text_yrspstn)
                        term_ends= term_ends.group(0).strip().replace('Termends',"").replace('Yearsinposition',"").replace(" ","")
                    except:
                        term_ends = "N/A: see url:{legis_url}".format(legis_url=legist_tupe[0])
                    result_dict = {}
                    result_dict['State'] = curr_state
                    legislator_ = legist_tupe[0].replace('https://ballotpedia.org/','').replace("_"," ")
                    if f"({curr_state})" not in legislator_:
                        result_dict['Legislator'] = legislator_
                    else:
                        result_dict['Legislator'] = legislator_.replace(f"({curr_state})",'')[:-1]
                    result_dict['Party'] = the_party
                    result_dict['State District'] = legist_tupe[1]
                    result_dict['Years in Office (+1/-1)'] = legist_tupe[3]
                    result_dict['Term Ends'] = term_ends
                    for i in range(6):
                        result_dict_i = i + 1
                        try:
                            result_dict[f'Facebook Link {result_dict_i}'] = fb_urls[i]
                        except:
                            result_dict[f'Facebook Link {result_dict_i}'] = "N/A"
                    print(result_dict)
                    legis_dict_list.append(result_dict)
                    len_legis_hrefs -= 1
                    print("hrefs left:",len_legis_hrefs)
            df = pd.DataFrame.from_records(legis_dict_list)
            df.to_csv(f"state_csvs/new_approach_state_csvs/{curr_state}_all_state_legislators.csv")
            self.curr_direct = "state_csvs/new_approach_state_csvs/"

    # def ballotpedia_grab_school_districts(self):
    #     driver = get_selenium_driver(minimize=False)
    #     driver.get("https://ballotpedia.org/School_board_elections,_2024")
    #     elements = driver.find_elements(By.TAG_NAME,"a") #"_elections_(2024)"
    #     school_districts =[]
    #     for el in elements:
    #         href = el.get_attribute("href")
    #         if href is not None:
    #             if "_elections_(2024)" in href:
    #                 print("href",href)
    #                 href = href.replace(",_elections_(2024)","")
    #                 school_districts.append() 
        # //*[@id="mw-content-text"]/div/div[3] # school board district ward table
            
    def ballotpedia_grab_top_200_school_dists(self,chosen_state=""):
        states_ = self.return_states_list_and_stage_groups_urls()
        THESTATES = states_[0]
        def find_state_in_states_list_with_fuzzy(chosen_state=chosen_state,f_thresh=80):
            matches = process.extract(chosen_state, THESTATES, limit=1)
            matches = [(word, score) for word, score in matches if score >= f_thresh]
            if matches:
                for word, _ in matches:
                    print(f"Searched State: {chosen_state}. Fuzzy Matched state:",word)
                    return word
            else:
                print("no match. try again.")
                return "darnit"
        driver = get_selenium_driver(minimize=self.selenium_minimize) 
        driver.get("https://ballotpedia.org/Largest_school_districts_in_the_United_States_by_enrollment")
        if chosen_state != "":
            chosen_state_fuzz = find_state_in_states_list_with_fuzzy(chosen_state=chosen_state)
            if chosen_state_fuzz != "darnit":
                THESTATES = [chose for chose in THESTATES if chosen_state_fuzz == chose]
            else:
                print("Failed to find school districts for state:",chosen_state)
                return False
        states_ = THESTATES + ['District_Of_Columbia']
        school_dists_top_200 = []
        for stat in states_:
            state_headertabs = driver.find_elements(By.XPATH, f"//div[@id='{stat}']/ol/li/a")
            for state in state_headertabs:
                href_ = state.get_attribute('href')
                if href_ != None:
                    if href_ not in school_dists_top_200:
                        pol_name = href_.replace("https://ballotpedia.org/","")
                        school_dists_top_200.append((href_,stat,pol_name))
        if self.test_run == True:
            if len(school_dists_top_200) > 0:
                print(f"Searched for State: {chosen_state}.")
                print("List of school district URLS:",[dist for dist in school_dists_top_200])
        school_dist_legists = []
        left_ct = 0
        for skoo in school_dists_top_200:
            left_to_go = len(school_dists_top_200) - left_ct
            if self.test_run == False:
                print("school districts left:",left_to_go)
            driver.get(skoo[0])
            time.sleep(2)
            for ct in range(1,50):
                try:
                    els = driver.find_element(By.XPATH, f"//*[@id='officeholder-table']/tbody/tr[{ct}]/td[2]/a")
                    els = els.get_attribute('href')
                    if els != None:
                        if "School" not in els:
                            school_dist_legists.append((els,skoo[1],skoo[2],skoo[0]))
                except:
                    left_ct+=1
                    break
        print("number of school district legislators:",len(school_dist_legists))
        with open("school_district_people/all_persons_urls.txt","w",encoding="utf-8") as f:
            for line in school_dist_legists:
                f.write(f"{line}\n")
        with open("school_district_people/all_persons_urls.txt","r",encoding="utf-8") as f:
            school_dist_legists = f.readlines()

        import ast ##To read a text file containing 
        #lines formatted as tuples in Python, you 
        #can use the ast.literal_eval method from the ast 
        #module. This method safely evaluates a string 
        #that contains a Python literal or container display. 
        #In your case, each line in the file is 
        #a string representation of a tuple.

        if self.test_run == False:
            # file_path = 'school_district_people/shortened_all.txt'  
            file_path = 'school_district_people/all_persons_urls.txt'
            school_dist_legists = []
            with open(file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    try:
                        tuple_data = ast.literal_eval(line)
                        school_dist_legists.append(tuple_data)
                    except ValueError:
                        print(f"Error processing line: {line}")
        left_ct = 0
        test_run_ct = 0
        for pers in school_dist_legists:
            test_run_ct+=1
            if self.test_run == True:
                if test_run_ct >= self.test_run_count:
                    print("Done with school legistlators for state:",chosen_state)
                    return True
            try:
                left_to_go = len(school_dist_legists) - left_ct
                print("left to go:",left_to_go)
                fb_urls = self.get_fb_urls(url=pers[0])  
                pers_name = pers[0].replace("https://ballotpedia.org/","").replace("'","").replace('"','')
                school_dist = pers[3].replace("https://ballotpedia.org/","").replace(f",_{pers[1]}","").replace("_"," ")
                pers_dict = {
                    "person":pers_name.replace("_"," "),
                    "state":pers[1],
                    "school_dist":school_dist,
                }
                for i in range(1,6):
                    try:
                        pers_dict[f'Facebook Link {i}'] = fb_urls[i]
                    except:
                        pers_dict[f'Facebook Link {i}'] = "N/A"
                df = pd.DataFrame(pers_dict,index=['person'])
                df.to_csv(f"school_district_people/{pers_name}_school_dist.csv")
                left_ct+=1
            except Exception as error:
                print("Error:",str(error))
                print("On:",pers)
                left_ct+=1
                        

# BALLOT= BallotpediaDataGrabber() 

# BALLOT.ballotpedia_grab_federal_level_computer_vision(read_image=False,fuzzy_threshold=80)
# SCOOL = BallotpediaGrabSchoolBoard()
# # SCOOL.ballotpedia_grab_school_districts()
# SCOOL.ballotpedia_grab_top_200_school_dists()
# import os

# df_list = []
# for filename in os.listdir("school_district_people/"):
#     if filename.endswith(".csv"):
#         if filename != "111_all_federal_legislators.csv":
#             # print(os.path.join(directory, filename))
#             filename = "school_district_people/" + filename
#             df = pd.read_csv(filename)
#             df_list.append(df)

# final_df = pd.concat(df_list,ignore_index=True)
# # final_df = final_df.drop(columns=['legist_url'])
# final_df.to_csv("school_district_people/top_200_school_dist_people.csv")
 
 