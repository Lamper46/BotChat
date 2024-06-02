import time
import random
import winsound
import datetime
import requests, json
from bs4 import BeautifulSoup
import lxml

command_list = ["date", "search", "numfact", "nameage", "define", "quote", "datatype", "multtable", "addtable", "time", "rand", "wiki", "delete", "about", "help", "learn", "remind", "mult", "div", "keyword", "sum", "sub", "repeat", "quit", "remove"]

def dad_joke(word):
    if "i'm " in word.lower() or "im " in word.lower():
        word_list = word.split()
        amount = len(word_list) - 1
        print(f"Hello, {word_list[amount]}, I'm BotChat!")
        done = True
        return done

def search_google(word):
    word.replace("/search ", "")
    params = {
        "q": word,  # Your query
        "hl": "en",          # Language
        "gl": "us",          # Country (e.g., UK -> United Kingdom)
        "start": 0,          # Starting page (default is 0)
        "num": 5          # Maximum number of results to return (optional)
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }

    page_limit = 10  # Set the desired page limit
    page_num = 0
    data = []

    while True:
        page_num += 1
        print(f"Page: {page_num}")
        html = requests.get("https://www.google.com/search", params=params, headers=headers, timeout=30)
        soup = BeautifulSoup(html.text, 'lxml')

        for result in soup.select(".tF2Cxc"):
            title = result.select_one(".DKV0Md").text
            try:
                snippet = result.select_one(".lEBKkf span").text
            except:
                snippet = None
            links = result.select_one(".yuRUbf a")["href"]

            data.append({
                "title": title,
                "snippet": snippet,
                "links": links
            })
    
        if page_num == page_limit:
            break
        
        if soup.select_one(".d6cvqb a[id=pnnext]"):
            params["start"] += 10
        else:
            break

    print(json.dumps(data, indent=2, ensure_ascii=False))


def get_number_fact(number):
    number = number.replace("/numfact ", "")
    url = f"http://numbersapi.com/{number}"
    response = requests.get(url)
    if response.status_code == 200:
        fact = response.text
        print(f"Fact for {number}: {fact}")
    else:
        print("Error fetching number fact.")

def name_age_guess(name):
    name = name.replace("/nameage ", "")
    base_url = f"https://api.agify.io/?name={name}"
    response = requests.get(base_url)
    data = response.json()
    print(data)


def get_word_definition(word):
    word = word.replace("/define ", "")
    try:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        response = requests.get(url)
        data = response.json()

        if isinstance(data, list):
            # Assuming the first item in the list contains the definition
            meanings = data[0].get("meanings", [])
            if meanings:
                definition = meanings[0].get("definitions", ["No definition found"])[0]
                print(f"Definition of '{word}': {definition['definition']}")
            else:
                return "No definition found"
        else:
            return "No definition found"
    except Exception as e:
        return f"Error fetching definition: {e}"

def data_type(data):
    data = data.replace("/datatype ", "")
    if data == "None":
        print("Represents the absence of a value or a null value.")
        print("Often used to indicate that a variable has not been assigned a value.")
        
    elif data == "bool" or data == "boolean":
        print("Represents a binary value: either True or False.")
        print("Used for logical operations and control flow (e.g., conditionals, loops).")

    elif data == "str" or data == "string":
        print("Represents a sequence of characters (text).")
        print('Enclosed in single or double quotes (e.g., "Hello, World!").')

    elif data == "int" or data == "integer":
        print("Represents whole numbers (positive, negative, or zero).")

    elif data == "float":
        print("Represents decimal numbers (floating-point numbers).")

    else:
        print("Datatype not found.")

def get_random_quote():
    url = "https://api.quotable.io/random"  # Use the Quotable API endpoint for random quotes
    response = requests.get(url)
    data = response.json()

    if "content" in data and "author" in data:
        quote = data["content"]
        author = data["author"]
        print(f'"{quote}" \n— {author}')
    else:
        print("Oops! Unable to fetch a quote.")
        
def addition_table(n):
    try:
        n = n.replace("/addtable", "")
        n = int(n)
        if n > 13:
            print("That is too large and will not render correctly.")
            done = True
            return done
        print("   |", end="")
        for j in range(1, n + 1):
            print(f" {j:3d} |", end="")
        print("\n" + "-" * (6 * n + 2))
        # Print the table rows
        for i in range(1, n + 1):
            print(f"{i:2d} |", end="")
            for j in range(1, n + 1):
                total = i + j
                print(f" {total:3d} |", end="")
            print("\n" + "-" * (6 * n + 2))
    except(ValueError):
        print("Incorrect syntax! Try typing /help addtable")


def multiplication_table(n):
    try:
        n = n.replace("/multtable ", "")
        n = int(n)
        if n > 13:
            print("That is too large and will not render correctly.")
            done = True
            return done
        for i in range(1, n + 1):
            row = []
            for j in range(1, n + 1):
                product = i * j
                row.append(f"{product:3d}")
            print(" | ".join(row))
            if i < n:
                print("-" * (5 * n + 4))  # Adjust the width based on the number of columns
    except(ValueError):
        print("Incorrect syntax! Try typing /help multtable")
    
def read_file():
    commands_txt = open("learned_commands.txt")
    commands = commands_txt.read()
    #Turning the text into a list. This will create a blank entry at the end
    commands_list = commands.split("\n")
    dictionary = {}
    #For each entry (besides the blank entry at the end)
    for count in range(0, (len(commands_list) - 1)):
        #Creating a dictionary with the name and contact
        entry = commands_list[count].split(",")
        name = entry[0]
        command = (entry[1])
        dictionary[name] = command
    #Return the dictionary
    return dictionary

def date():
    print(f'Today is {datetime.date.today()}')
    done = True
    return done

def print_time():
    print(f'It is {time.strftime("%H:%M:%S", time.gmtime())} UTC')

def random_num(num):
    try:
        num = num.replace("/rand ", "")
        num = num.split(", ")
        print(f"A number in that range is: {random.randrange(int(num[0]), int(num[1]))}.")
    except(ValueError, KeyError) as error:
        print("Incorrect syntax! Try typing /help rand")

#Function for writing to the file
def write_file():
    commands_txt = open("learned_commands.txt", "w")
    dictlist = []
    #Writing everything to the file in the form "key,value\n"
    for key, value in learned_dict.items():
        commands_txt.write(key + "," + str(value) + "\n")

def wikipedia(topic):
    if "/wiki" in topic:
        topic = topic.replace("/wiki ", "")
        topic = topic.replace(" ", "-")
        print(f"en.wikipedia.org/wiki/{topic}")

def delete_command(command):
    if "/delete" in command:
        command = command.replace("/delete ", "")
        command = "/" + command
        if command in learned_dict.keys():
            del learned_dict[command]
            print("Learned command deleted!")
        else:
            print("Command not found")
   
def about(word):
    if word == "/about":
        print("I am a test to see if it is possible to make a Python chatbot without OpenAI.")
        print("My Creator is Michael Meidan.")
        print("I was started as a side project on April 22nd, 2024.")
        done = True
        return done

def learn(command):
    if "/learn" in command:
        try:
            new_learn = command.split(" | ")
            no_slash = list(learned_dict)
            no_slash = [w.replace('/', '') for w in no_slash]
            if new_learn[1] in no_slash or new_learn[1] in command_list:
                print("A command with that name already exists.")
                done = True
                return done
            del new_learn[0]
            new_learn[0] = '/' + new_learn[0]
            learned_dict[new_learn[0]] = new_learn[1]
            print("Command learned!")
            done = True
            return done
        except IndexError:
            print("Incorrect syntax! Try typing /help learn")
            
def mult_nums(numbers):
    if "/mult" in numbers:
        try:
            multiply = 1
            numbers = numbers.replace("/mult ", "")
            num_list = numbers.split(", ")
            for count in range(0, len(num_list)):
                multiply = multiply * float(num_list[count])
            print(f"The answer is {multiply:.2f}.")
            done = True
            return done
        except ValueError:
            print("Incorrect syntax! Try typing /help mult")

def div_nums(numbers):
    if "/div" in numbers:
        try:
            numbers = numbers.replace("/div ", "")
            num_list = numbers.split(", ")
            divide = float(num_list[0])
            for count in range(1, len(num_list)):
                divide = divide / float(num_list[count])
            print(f"The answer is {divide:.2f}.")
            done = True
            return done
        except ValueError:
            print("Incorrect syntax! Try typing /help div")
        except ZeroDivisionError:
            print("Division by zero is not allowed.")

def keyword(word):
    word = word.replace("/keyword ", "")
    if word == "and":
        print("A keyword used to say that something must happen if two expressions are True.")
        
    elif word == "as":
        print("A keyword used to give another name to an imported module.")

    elif word == "assert":
        print("A keyword used to say that some code must be True.")

    elif word == "break":
        print("A keyword used to stop some code from running.")

    elif word == "class":
        print("A keyword used to define a type of object, like an animal or a vehicle.")

    elif word == "continue":
        print("A keyword used to jump to the next item in a loop.")

    elif word == "def":
        print("A keyword used to define a funtion.")

    elif word == "del":
        print("A keyword used to delete something in a list.")

    elif word == "elif":
        print("A keyword used to have another if statement related to another.")

    elif word == "else":
        print("A keyword used to say that something should happen if a consition is not met.")

    elif word == "except":
        print("A keyword used to do something when an error happens.")

    elif word == "finally":
        print("A keyword used to make sure that if an error happens, certain code runs.")

    elif word == "for":
        print("A keyword used to create a loop that runs a certain amount of times.")

    elif word == "from":
        print("A keyword used to import part of a module.")

    elif word == "global":
        print("A keyword that lets a variable defined in a function be used anywhere.")

    elif word == "if":
        print("A keyword used to make a decision about something.")

    elif word == "import":
        print("A keyword used to load a module so that it can be used.")

    elif word == "in":
        print("A keyword used to see if an item is in a collection of items.")

    elif word == "is":
        print("A keyword used to see if two things are equal.")

    elif word == "lambda":
        print("A keyword used to create anonymous, inline functions.")

    elif word == "not":
        print("A keyword used to say that something must be opposite.")

    elif word == "or":
        print("A keyword used to say that one of two or more things must be true.")

    elif word == "pass":
        print("A keyword used as a placeholder for other code.")

    elif word == "raise":
        print("A keyword used to cause an error.")

    elif word == "return":
        print("A keyword used to return a value from a function.")

    elif word == "try":
        print("A keyword that works with except and finally to handle errors.")

    elif word == "while":
        print("A keyword used to make a loop run while a condition is True.")

    elif word == "with":
        print("A keyword used with an object to create a block of code.")

    elif word == "yield":
        print("A keyword used with a class of objects called a generator.")

    else:
        print("I don't know that word.")
    
def add_nums(numbers):
    if "/sum" in numbers:
        try:
            numbers = numbers.replace("/sum ", "")
            num_list = numbers.split(", ")
            new_list = []
            for count in range(0, len(num_list)):
                new_list.append(float(num_list[count]))
            print(f"The answer is {sum(new_list):.2f}.")
            done = True
            return done
        except ValueError:
            print("Incorrect syntax! Try typing /help sum")

def use_learn(command):
    if " " in command:
        command_parts = command.split(" ")
        command_parts[0].remove()
        if command_parts[0] in learned_dict.keys():
            print(learned_dict[command])
    if command in learned_dict.keys():
            print(learned_dict[command])

    else:
        print("Command not found")

def sub_nums(numbers):
    if "/sub" in numbers:
        try:
            numbers = numbers.replace("/sub ", "")
            num_list = numbers.split(", ")
            new_list = []
            for count in range(0, len(num_list)):
                new_list.append(float(num_list[count]))
            total = new_list[0]
            for count in range(0, len(new_list)):
                total = total - new_list[count]
            print(f"The answer is {total:.2f}.")
            done = True
            return done
        except ValueError:
            print("Incorrect syntax! Try typing /help sub")

def repeat(word):
    word = word.replace("/repeat ", "")
    print(word)
        
def help(word):
    learned_list = list(learned_dict.keys())
    if word == "/help":
        command = "{command}"
        print(f'''Here is a list of all my commands:
/sum - adds numbers
/about - explains my purpose
/sub - subtracts numbers
/mult - multiplies numbers
/div - divides numbers
/help - brings you to this screen
/learn - learns a command
/remind - sets a reminder
/wiki - shows you a wikipedia entry
/numfact - gives you a random fact about a number
/delete - removes a learned command
/repeat - repeats something back to you
/time - says the current time in UTC
/date - says the current date
/remove - removes a learned command
/quit - allows you to leave
/rand - gives you a random number in a range
/keyword - tells you about a Python keyword
/multtable - shows you a multiplication table
/addtable - shows you an addition table
/search - lets you search Google
/quote - gives you a quote from Quotable
/datatype - tells you about a Python data type
/define - gives you the definition of a word from DictionaryAPI
/nameage - tells you what age you might be based off of your first name
Learned commands: {', '.join(learned_list)}
Type /help {command} to see more about a command.''')
        done = True
        return done

def help_indepth(word):
    word = word.replace("/help ", "")
    if word == "sum":
        print('''Adds multiple  numbers.
Syntax: /sum {num1}, {num2}, {num3}, ect
Does: num1 + num2 + num3, ect''')

    elif word == "define":
        print('''Gives you the definition of a word from Dictionary API
Syntax: /define {word}
Does: Gives you the definition of word
Notes: If no definition is found, nothing will be printed.''')

    elif word == "nameage":
        print('''Says what age you might be based off your name
Syntax: /nameage {name}
Does: Tells you the most likely age of somebody named name
Notes: Better with older names''')

    elif word == "multtable":
        print('''Shows you the multiplication table up to a specific value
Syntax: /multtable {number}
Does: Shows you multiplication up to number * number''')

    elif word == "addtable":
        print('''Shows you the addition table up to a specific value
Syntax: /addtable {number}
Does: Shows you addition up to number + number''')

    elif word == "sub":
        print('''Subtracts numbers from a starting number.
Syntax: /sub {num1}, {num2}, {num3}, ect
Does: num1 - num2 - num3, ect''')

    elif word == "numfact":
        print('''Gives you a fact about a number you choose.
Syntax: /numfact {number}
DOes: Tells you a fact about number''')

    elif word == "about":
        print("Displays the about page")

    elif word == "time":
        print("Displays current time in UTC")

    elif word == "date":
        print("Displays the current date")
        
    elif word == "learn":
        print('''Learns a command.
Syntax: /learn | {Command Name} | {Function}
Does: Function when command name used''')

    elif word == "remind":
        print('''Sets a reminder.
Syntax: /remind | {Minutes} | {Reminder}
Does: Reminds Reminder in Minutes minutes
Notes: You must actively be using BotChat for the reminder to go off
       Do not enter 0 as the time''')
        
    elif word == "wiki":
        print('''Shows you a wikipedia entry of your choosing
Syntax: /wiki topic
Does: en.wikipedia.org/wiki/topic''')

    elif word == "mult":
        print('''Multiplies numbers.
Syntax: /mult {num1}, {num2}, {num3}, ect
Does: num1 * num2 * num3, ect''')

    elif word == "datatype":
        print('''Tells you about a Python datatype.
Syntax: /datatype {datatype}
Does: Tells you about datatype''')
        
    elif word == "div":
        print('''Divides numbers from a starting number.
Syntax: /div {num1}, {num2}, {num3}, ect
Does: num1 / num2 / num3, ect''')

    elif word == "delete":
        print('''Deletes a learned command
Syntax: /delete {command}
Does: Deletes command''')

    elif word == "quote":
        print("Gives you a quote from Quotable.")

    elif word == "rand":
        print('''Gives you a number in a range you specify
Syntax: /rand {num1}, {num2}
Does: Gives you a random number between num1 and num2''')
        
    elif word == "repeat":
        print('''Says your words back to you
Syntax: /repeat {word}
Does: Prints word''')

    elif word == "remove":
        print('''Removes a learned command
Syntax: /remove {command"
Does: Removes command''')

    elif word == "keyword":
        print('''Tells you about a Python keyword
Syntax: /keyword {word}
Does: tells you about the keyword word''')

    elif word == "search":
        print('''Lets you search on Google
Syntax: /search {topic}
Does: Gives you results for the search query "topic"
Notes: Query does not currently work''')

    elif word == "quit":
        print("Lets you leave BotChat")
        
    else:
        print("I don't know how to do that.")

####MAIN####

print("Welcome to BotChat!")
print("To get started, type /about or /help!")
learned_dict = read_file()
no_quit = True
start = 0
timer_list = ["","999999999999999999999999", ""]
while(no_quit):
    try:
        if time.time() - start > float(timer_list[1]) * 60:
            print(timer_list[2].upper())
            duration = 1000
            freq = 440
            winsound.Beep(freq, duration)
            timer_list = ["","999999999999999999999999", ""]
            time.sleep(0.5)
    except IndexError:
        pass
    except ValueError:
        pass

    prompt = input()
    try:
        if time.time() - start > float(timer_list[1]) * 60:
            print(timer_list[2].upper())
            duration = 1000
            freq = 440
            winsound.Beep(freq, duration)
            timer_list = ["","999999999999999999999999", ""]
            time.sleep(0.5)
    except IndexError:
        pass
    except ValueError:
        pass
    
    if "/sum" in prompt:
        add_nums(prompt)

    elif "/sub" in prompt:
        sub_nums(prompt)

    elif "i'm " in prompt.lower() or "im " in prompt.lower():
        dad_joke(prompt)

    elif prompt == "/about":
        about(prompt)

    elif prompt == "/help":
        help(prompt)

    elif "/help " in prompt:
        help_indepth(prompt)

    elif "/learn" in prompt:
        learn(prompt)
        write_file()
        read_file()

    elif "/mult" in prompt and "table" not in prompt:
        mult_nums(prompt)

    elif "/div" in prompt:
        div_nums(prompt)
        
    elif "/remind" in prompt:
        remind = True
        while remind == True:
            try:
                timer_list = prompt.split(" | ")
                if len(timer_list) == 2:
                    print("Incorrect syntax! Try typing /help remind")
                    remind = False
                    break
                else:
                    start = time.time()
                    print("Reminder set!")
                    while time.time() - start < float(timer_list[1]) * 60:
                        remind = False
                        break
            except (IndexError, ValueError) as error:
                print("Incorrect syntax! Try typing /help remind")
                remind = False

    elif "/delete" in prompt:
        delete_command(prompt)
        write_file()
        read_file()

    elif "/nameage" in prompt:
        name_age_guess(prompt)

    elif "/repeat" in prompt:
        repeat(prompt)

    elif "/search" in prompt:
        search_google(prompt)

    elif prompt == "/time":
        print_time()
        
    elif "/wiki" in prompt:
        wikipedia(prompt)
        
    elif prompt == "/date":
        date()

    elif "/rand" in prompt:
        random_num(prompt)

    elif "/keyword" in prompt:
        keyword(prompt)

    elif prompt == "/quit":
        print("Goodbye!")
        break

    elif "/define" in prompt:
        get_word_definition(prompt)

    elif "/datatype" in prompt:
        data_type(prompt)

    elif "/multtable " in prompt:
        multiplication_table(prompt)

    elif "/numfact" in prompt:
        get_number_fact(prompt)

    elif prompt == "/quote":
        get_random_quote()

    elif "/addtable" in prompt:
        addition_table(prompt)
    
    elif prompt in learned_dict.keys():
        use_learn(prompt)

    elif not "/" in prompt:
        print('All commands must start with "/".')
    
    else:
        print("I don't know that.")
