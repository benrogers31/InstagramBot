from main import InstaBot
import sys

class Run:
    
    def __init__(self):
        print("Enter your username")
        username = input()
        print("Enter your password")
        pwd = input()
        #here we are ensuring we there was a valid account inputed
        try:
            self.myBot = InstaBot(username, pwd)
            self.myBot.start()
        except Exception as e:
            print(e)
            self.myBot.driver.quit()
            sys.exit()
        #Here we have our prompt for people user to work with 
        while True:
            print("What do you want to do?\n")
            print("Enter 1 find out who doesnt follow you back?")
            print("Enter 2 to unfollow a certain amount of people")
            print("Enter 3 to follow a certain number of users")
            print("Enter 4 to generate a list of people to follow in the future")
            print("Enter anything else to exit")

            descison_input = int(input())
            
            if descison_input == 1:
                if self.myBot.lists_have_been_updated == False:
                    self.update_lists()

                list_of_unfollowers  = self.myBot.get_unfollowers()

                print("Do you want to unfollow these people? ")
                print(" [Y] to unfollow anything else for no")
                unfollow_users = input()
                if unfollow_users == 'Y':
                    for name in list_of_unfollowers['User']:
                        try:
                            self.myBot.unfollow(name)
                        except Exception as e:
                            print(e)
                            self.myBot.driver.find_element_by_xpath("/html/body/div[1]/section/nav/div[2]/div/div/div[2]/input").send_keys(self.myBot.backspaces)
                            
                else:
                    continue
            
            
            # We are unfollowing people here
            elif descison_input == 2: 
                if self.myBot.lists_have_been_updated == False:
                    self.update_lists()
                print("How many people you trying to unfollow?")
                num_users =  self.get_number()
                self.myBot.unfollow_users(num_users)
            
            # Here we are following people
            elif descison_input == 3:
                if self.myBot.lists_have_been_updated == False:
                    self.update_lists()
                print("How many people you trying to Follow")
                num_users =  self.get_number()
                self.myBot.follow_users(num_users)

            elif descison_input == 4:
                if self.myBot.lists_have_been_updated == False:
                    self.update_lists()
                print("What is the name of the account you want to take followers of from")
                name_account = input()
                print("Begining to Generate the list") 
                try:
                    self.myBot.generate_follow_list("name_account")  
                except:
                    print("this wasn't a real account") 
                
            else: 
                print("shutting down")
                self.myBot.driver.quit()
                sys.exit()


    #time to start building the UI 
    def get_number(self):
        while True: 
            number_of_users = int(input())
            if not number_of_users.isdigit() :
                print("Put in a number pls, try again")
            elif number_of_users > 250:
                print("that number is probably too big for insta, try something lower")
            else:
                break
        return number_of_users
        
    #checks if the lists have been updated for the bot
    def update_lists(self):
        print("Getting account followers\n")
        self.myBot.get_my_followers()
        print("Getting accounts this account follows\n")
        self.myBot.get_my_following()
        print("list of unfollowers: ")
        self.myBot.lists_have_been_updated = True
        
Run()