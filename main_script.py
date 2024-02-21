from scrape_ballotpedia import *

def main_func(search_for="",searched_level="federal",total_grab="federal",save_as_final_csv=False,federal_read_images=False,test_run=True,test_run_count=15,school_district_state="",selenium_minimize=True):
    """
    federal_read_images = False (default). Doesn't run CV program just goes to screencap directory.
    """
    run_vpn() # run VPN

    if search_for != "":
        print("Searching for:",search_for)
        BALLOTGRABBER = BallotpediaDataGrabber(selenium_minimize=selenium_minimize)
        BALLOTGRABBER.search_for_state_or_federal_legislator(searched_name=search_for,government_level=searched_level)
        total_grab = "NOT!"
    if save_as_final_csv==True:
        if search_for == "":
            print(f"saving final data for [{total_grab}]-level as a csv.")
    if total_grab == "federal":
        BALLOTGRABBER = BallotpediaDataGrabber(test_run=test_run,test_run_count=test_run_count,selenium_minimize=selenium_minimize)
        BALLOTGRABBER.ballotpedia_grab_federal_level_computer_vision(read_image=federal_read_images)
        if save_as_final_csv == True:
            save_final_csv(curr_direct=BALLOTGRABBER.curr_direct,final_name="federal")
    if total_grab == "state":
        BALLOTGRABBER = BallotpediaDataGrabber(test_run=test_run,test_run_count=test_run_count,selenium_minimize=selenium_minimize)
        BALLOTGRABBER.ballotpedia_grab_state_level()
        if save_as_final_csv == True:
            save_final_csv(curr_direct=BALLOTGRABBER.curr_direct,final_name="all_states")
    if total_grab == "school":
        BALLOTGRABBER = BallotpediaDataGrabber(test_run=test_run,selenium_minimize=selenium_minimize)
        BALLOTGRABBER.ballotpedia_grab_top_200_school_dists(chosen_state=school_district_state)
        if save_as_final_csv == True:
            save_final_csv(curr_direct=BALLOTGRABBER.curr_direct,final_name="top_200_school_dists")
 

 
# main_func(total_grab="school",school_district_state="kansaz",test_run=True)
    
# main_func(
#     total_grab="federal", # grab federal level data
#     save_as_final_csv=True, # sava final data as "master" csv file
#     test_run=True, # test run. just grab a handful of info.
#     test_run_count=5, # number of items to grab for a given test run
#     federal_read_images=True # CV process
#     )
    
# name spelled wrong on purpose to showcase matching capabilities.
# main_func(search_for="matthew")  # Cori Bush (rep from St Louis, MO) is correct spelling.
            
BALLOT = BallotpediaDataGrabber()
BALLOT.grab_state_executive_officeholders()