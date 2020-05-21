from selenium import webdriver
import time 
from datetime import datetime
import os.path
import pandas as pd
import csv

class InstaBot:



    def __init__(self,username,pwd):
        #this here is a way to store where our lists will be stored 
        self._path_to_files = "../insta_files/"
        #this is an indicator to whether or not the lists have been updated 
        self.lists_have_been_updated = True
        self.driver = webdriver.Chrome()
        self.username = username
        self.pwd = pwd
        self.backspaces = "\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b"
        self.driver.get("https://www.instagram.com/")

    def start(self):
        time.sleep(2)
        #this xpath is for the input box on the login screen
        self.driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input").send_keys(self.username)
        #xpath is for the password input 
        self.driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input").send_keys(self.pwd)
        #xpath is for login button 
        self.driver.find_element_by_xpath("/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[4]").click()
        #sleep is to let the next page load up
        time.sleep(3)
        #this is the xpath to remove notifications popup  
        e = self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")
        self.driver.execute_script("arguments[0].click();", e)
        #now we sleep to make sure thing are loaded up
        time.sleep(2)

    #this prints and returns a 
    def get_unfollowers(self):
        #this loads  self.following_df  self.followers_df self.unfollowed_df safe_list_df 
        self.load_dataframes()
        #following set difference of safe list and people I'm following ie following \ safelist
        not_following_back = self.following_df.merge(self.followers_df, indicator=True, how="left")\
            [lambda x: x._merge=='left_only'].drop('_merge',1)
        #prints to terminal the users that are not following back
        print(not_following_back)
        #also returns the list just incase it is used by other functions
        return(not_following_back)
    
    #this returns all values in a list 
    def _get_names(self):
        time.sleep(2)
        #this gets the element of the scroll box and stores it into an attribute
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")
        #initializing variables
        last_ht, ht = 0, 1
        #last height will refer to the height of the scroll box before the scroll
        #ht refers to the height of the scroll box after the scroll
        #if the script scrolls and the height doesn't change it means we are at the bottom of the scroll box 
        #hence exit condition of last_ht != ht 
        while last_ht != ht:
            last_ht = ht
            time.sleep(2)
            #this executes a comand in javascript to scrol to the scroll height and return height 
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        #gets the names as links    
        links = scroll_box.find_elements_by_tag_name('a')
        #stores the text values as names 
        names = [name.text for name in links if name.text != '']
      
        # This retrieves the close button and clicks it 
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button")\
            .click()
        time.sleep(2)
        return names
    


    def go_to_profile(self, profile_name):
        #types in the desired profile name into search bar
        self.driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input")\
            .send_keys(profile_name)
        time.sleep(4)
        #stores the popup of the link to profile after it is typed in
        name_element = self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(profile_name))
        #this is java script to click on the dropdown menu 
        self.driver.execute_script("arguments[0].click();", name_element)
        time.sleep(3)

    def go_to_my_profile(self):
        #this clicks the link on the ig web page that goes to our profile
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.username))\
            .click()
        #these sleep functions ensure everything has time to load
        time.sleep(3)

    #function that writes a csv file of people I follow
    def get_my_followers(self):
        #goes to my own profile
        self.go_to_my_profile()
        #this then clicks on our followers button
        time.sleep(3)
        #this gets the link to pop up followers and stores it in a variable
        followers_element = self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")\
        #this is java script to click on followers element 
        self.driver.execute_script("arguments[0].click();", followers_element)
        #getting names of followers and store them into followers list
        followers_list = self._get_names()
        #we are going to store data in a csv file and creating it each time
        #date = datetime.today().strftime('%Y-%m-%d')
        out_filename = self._path_to_files + "myFollowers_"+self.username+".csv"
        f = open(out_filename, "w")
        f.write("User\n")
        for follower in followers_list:
            f.write(follower + "\n")


    #function that writes a csv file of people that I follow
    def get_my_following(self):
        #goes to my own profile
        self.go_to_my_profile()
        time.sleep(3)
        #This clicks the link that goes to the people we are following 
        element = self.driver.find_element_by_xpath("//a[contains(@href,'/following')]")
        self.driver.execute_script("arguments[0].click();", element)    
        #getting names of followers 
        followers_list = self._get_names()
        #we are going to store data in a csv file and creating it each time
        
        out_filename =  self._path_to_files + "peopleIFollow_"+self.username+".csv"
        f = open(out_filename, "w")
        f.write("User\n")
        for follower in followers_list:
            f.write(follower + "\n")


    def follow(self,user):
        #goes to profile then followss
        self.go_to_profile(user)
        time.sleep(2)
        element = self.driver.find_element_by_xpath("//button[contains(text(),'Follow')]")
        self.driver.execute_script("arguments[0].click();", element)   
        out_filename = self._path_to_files + "myFollowers_"+self.username+".csv"
        f = open (out_filename, "a")
        f.write(user +"\n")
        time.sleep(2)
    
    def unfollow(self,user):
        #goes to profile then unfollowss
        self.go_to_profile(user)
        time.sleep(4)
        #this xpath is for the unfollow button
        element = self.driver.find_element_by_xpath("//button[@class='_5f5mN    -fzfL     _6VtSN     yZn4P   ']")
        self.driver.execute_script("arguments[0].click();", element)  
        time.sleep(3)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Unfollow')]").click()
        time.sleep(3)
        
        #gets the current date
        date = datetime.today().strftime('%Y-%m-%d')
        #gets the filename
        out_filename =  self._path_to_files + "users_unfollowed_"+self.username+".csv"
        #if the file exists then 
        if(not os.path.isfile(out_filename) ):
            f = open (out_filename, "a")
            f.write("NAME ,DATE\n")
        else:
            f = open (out_filename, "a")

        
        f.write(user +","+ date +"\n" )
        f.close()
    
    #Generate list of people to follow
    def generate_follow_list(self,user):
        #goes to the user profile we want to go to
        self.go_to_profile(user)
        #this then clicks on our followers button
        time.sleep(3)
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")\
            .click()
        #getting names of followers 
        names_list = self._get_names()
        #this loads  self.following_df  self.followers_df and self.unfollowed_df
        self.load_dataframes()
        #checks if the name is in any of these lists 
        out_filename =  self._path_to_files + "users_to_follow_"+self.username+".csv"
        f = open (out_filename, "w")
        f.write("User\n")
        names_added = []
        #checks if I either follow, or am followed by or have unfollowed these people 
        for name in names_list:
            if (self.followers_df['User'].str.contains(name).any() or\
                self.following_df['User'].str.contains(name).any() or\
                self.unfollowed_df['NAME'].str.contains(name).any()):
                continue
            else:
                f.write(name + "\n")
                names_added.append(name)
        f.close()
        print("Here are names that are currently in your too follow list")
        print(names_added)
        print("It is size: " + len(names_added))

    def unfollow_users(self, number):
        #this loads  self.following_df  self.followers_df self.unfollowed_df safe_list_df
        self.load_dataframes()
        #following set difference safe list 
        users_to_unfollow = self.following_df.merge(self.safe_list_df, indicator=True, how="left")[lambda x: x._merge=='left_only'].drop('_merge',1)
        print("these are the folks we are going to unfollow")
        print(users_to_unfollow.head(number))
        #unfollow all users in this list
        #print(users_to_unfollow)
        users_unfollowed = 0
        for user in users_to_unfollow["User"]:
            print(user)
            if users_unfollowed > number:
                break
            if self.safe_list_df['User'].str.contains(user).any() or\
                self.unfollowed_df['NAME'].str.contains(user).any():
                print("hi")
                continue
            else:
                try:
                    self.unfollow(user)
                    print("worked")
                    users_unfollowed += 1
                except:
                    print("can't unfollow account")
                    #this sends a bunch of backspaces to get rid of the bug where a 
                    # person can't be unfollowed but their name is still in the search bar
                    self.driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input")\
                        .send_keys(self.backspaces)
        print("number of users unfollowed: " +str(users_unfollowed))
                

    def add_to_safe_list(self,user):
        out_filename =  self._path_to_files + "safe_list_"+self.username+".csv" 
        f = open (out_filename, "a")
        f.write(user+","+"\n")

        
    def follow_users(self,numberToFollow):
        #gets users to follow
        df = pd.read_csv( self._path_to_files + "users_to_follow_"+self.username+".csv")
        self.load_dataframes()
        numberfollowed = 0
        for user in df['User']:
            if(numberfollowed > numberToFollow):
                break
            if (self.followers_df['User'].str.contains(user).any() or\
                self.following_df['User'].str.contains(user).any() or\
                self.unfollowed_df['NAME'].str.contains(user).any()):
                continue
            else:
                try:
                    self.follow(user)
                    print("worked")
                    numberfollowed += 1
                except: 
                    print("couldn't follow " + user)
                    #this sends a bunch of backspaces to get rid of the bug where a 
                    # person can't be unfollowed but their name is still in the search bar
                    self.driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input")\
                        .send_keys(self.backspaces)
        print("number of users followed: "+ str(numberfollowed))
    
    def load_dataframes(self):
        #first we are going to get list of people we follow and store into data frame
        if hasattr(self, 'following_df'):
            return
        else:
            if(os.path.isfile( self._path_to_files + "peopleIFollow_"+self.username+".csv")):
                self.following_df = pd.read_csv( self._path_to_files + "peopleIFollow_"+self.username+".csv")
            else:
                self.get_my_following()
                self.following_df = pd.read_csv( self._path_to_files + "peopleIFollow_"+self.username+".csv")
            if(os.path.isfile( self._path_to_files + "myFollowers_"+self.username+".csv")):
                self.followers_df = pd.read_csv( self._path_to_files + "myFollowers_"+self.username+".csv")
            else: 
                self.get_my_followers()
                self.followers_df = pd.read_csv( self._path_to_files + "myFollowers_"+self.username+".csv")
            #now we are going to load people we have unfollowed 
            if(os.path.isfile( self._path_to_files + "users_unfollowed_"+self.username+".csv")):
                self.unfollowed_df = pd.read_csv( self._path_to_files + "users_unfollowed_"+self.username+".csv")
            if(os.path.isfile( self._path_to_files + "safe_list_"+self.username+".csv")):
                self.safe_list_df = pd.read_csv( self._path_to_files + "safe_list_"+self.username+".csv")
        

