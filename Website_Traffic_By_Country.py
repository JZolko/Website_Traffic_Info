'''This project reads a CSV file, sorts the data, and returns specific lists based on what values are needed.'''



import csv
import operator
from operator import itemgetter


acceptable = ['1', '2', '3', 'q', 'Q']

PROMPT = '''
Choose
         (1) Top sites by country
         (2) Search by web site name
         (3) Top sites by views
         (q) Quit
         
Choice:
'''

def open_file(fp):
    '''This function tries to open the file and returns False if there isnt a file'''
    
    try:
        test = open(fp,encoding="ISO-8859-1") # try to open the file, if it doesn't then the function returns false
        return test
    
    except FileNotFoundError:
        return False


def read_file(fp):
    '''This reads the file for manipulation and creates a list based on the variables needed'''
    dest, new, test = [], [], []
    need = [0, 1, 5, 14, 30]
    
    #file = open(fp,'r')
    reader = csv.reader(fp) # attaches a reader to the file fp
    next(reader,None) # skips a line, such as a header line
    
    for i, k in enumerate(reader): #skips the first line and adds the rest to a list
        
        if i == 0:
            pass
        else:
            dest.append(k)

    for i in range(len(dest)): # removes any spaces so the number can be converted to an int
        dest[i][5] = str(dest[i][5]).replace(' ', '')
        dest[i][14] = str(dest[i][14]).replace(' ', '')
    
    for i in range(len(dest)): # tests for the 'N/A' in the line and if it sees N/A, it skips that row
        try:
            x= int(dest[i][5])
            y= int(dest[i][14])
            
            test = (int(dest[i][0]), dest[i][1],y ,x , dest[i][30])
            
            new.append(test)
            
        except ValueError:
            pass
        
    new = sorted(new, key= operator.itemgetter(0,4)) #returns a sorted list, sorts by country rank and country name
    return new
      

def remove_duplicate_sites(lol):
    '''This looks at the URL and adds any new URL to a list and skips over existing URLS'''
    
    dest, ref, new = [], [], []
    test = set()
    
    for i in range(len(lol)):
        ref = [lol[i][0],lol[i][1] ,lol[i][2] ,lol[i][3] ,lol[i][4]]
        dest.append(ref)
        
    
    for i in range(len(dest)):
        dest[i][1] = dest[i][1].split('.')

    
    for a, b, c, d, e in dest:
        if not b[1] in test:
            test.add(b[1])
            try:  # this accounts for any url with multiple endings like ".co.uk"
                b = str(b[0] + '.' + b[1] + '.' + b[2] + '.' + b[3])
            except:
                b = str(b[0] + '.' + b[1] + '.' + b[2])
            
            
            trout = (a, b, c, d, e) #this is the concatinated tuple with all the variables put back into place
            new.append((trout))
    
    new = sorted(new, key= operator.itemgetter(0,1))  #sorts the list based on country rank and URL
    
    
    return new
    

def top_sites_per_country(lst,country):
    '''This function iterates through the list and looks at the top sites per country'''
    new = []
    
    lst = sorted(lst, key= operator.itemgetter(0, 3), reverse= False) # initially sort the list based on country rank and view rank
    
    for tup in lst: # this adds any website with the same country name to a list
            if tup[4] == str(country):
                new.append(tup)
            else:
                pass
    
        
    return new[:20] # returns the specific range of a very long list


def top_sites_per_views(lol):
    '''Docstring goes here.'''
    
    lol = sorted(lol, key= operator.itemgetter(3), reverse=True)  # sorts by views in decending order
    
    lol = remove_duplicate_sites(lol)   #removes any duplicates
       
    lol = sorted(lol, key= operator.itemgetter(3), reverse=True) # re sorts the list into descending order
    
    return lol[:20] # returns a small portion of a large list

def main():
    '''Docstring goes here.'''
    recursion = True
    print("----- Web Data -----")
    file_name = input("Input a filename: ")
    
    while recursion == True: # this probably isn't necessary, but it works to keep the loop going
        
        
        
        salmon = open_file(file_name) # tries to open the file
        
        if file_name == 'q':
            break
        
        while not(salmon): #while the file is unable to be opened
            print("Error: file not found.")
            file_name = input("Input a filename: ")
            salmon = open_file(file_name)
        
        print(PROMPT) # this is the menu
        choice = input() # inpur for the menu
        
        
        rede = open(file_name, encoding="ISO-8859-1")
        file = read_file(rede) # removes the need to open in each if statement
        
        
        
        while not choice in acceptable: # if the input isnt 1, 2, 3, or q
            print("Incorrect input. Try again.")
            print(PROMPT)
            choice = input()
            
        if choice == '1': #==================================================================================================
            '''This will take an input and display the top 20 sites of the inputed country'''
            
            print("--------- Top 20 by Country -----------")
            
            country = input("Country: ")
            
            file = top_sites_per_country(file, country) 
            
            processed = remove_duplicate_sites(file)
    
            
            final = remove_duplicate_sites(processed)
            
            
            
            print('{:30s} {:>15s}{:>30s}'.format("Website","Traffic Rank","Average Daily Page Views"))
            
            for i in range(len(final)): #the shortest way I could find to print a bunch of stuff at once
                
                print('{:30s} {:>15d}{:>30,d}'.format(final[i][1], final[i][2], final[i][3]))
        
        elif choice == '2': #================================================================================================
            '''This will search for any websites that contain the string input'''
            
            new = []
            site = input("Search: ")
        
            print("{:^50s}".format("Websites Matching Query"))
            
            
            try:
                
                for i in range(len(file)): # if the characters are in the URL it appends to a list
                    if site.lower() in file[i][1]:
                        new.append(file[i][1])
                
                sent = new[0]
                sent = new[1]
                
                for i in range(len(new)): # if the list has a value, the results will print
                    print('{:<10s}'.format(new[i]))   
            except: # if the list is empty, it prints  no sites are found
                print('{:<10s}'.format('None found'))
            
        
        elif choice == '3': #================================================================================================
            '''This will look for the top sites and print the list'''
            
            final = top_sites_per_views(file) 
            
            test = sorted(final, key= operator.itemgetter(3)) # sorts the list by view count
            
            sent = remove_duplicate_sites(test)
            
            full = sorted(sent, key= operator.itemgetter(3), reverse= True) # sorts the list againa after duplicate removal
             
            
            print("--------- Top 20 by Page View -----------")
            print('{:30s}{:>25s}'.format("Website", "Ave Daily Page Views"))
            
            
            for i in range(len(full)):
                print('{:30s} {:>20,d}'.format(full[i][1], full[i][3]))
        
        
        
        elif choice.lower() == 'q': #========================================================================================
            break # quit the program


if __name__ == "__main__":
     main()
