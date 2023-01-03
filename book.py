record = []
books = []
ID_MAX = 512

def add_record(ID):
    print("Please input your the book you've borrowed")
    book = input();#type is keyed by user?
    record.append(book);
    books[ID][book] = [0, 1, 0, 0];#done, type, comment, preference
    print("Press C to continue. Press E to exit.")
    choice = input()
    while 1:
        if (choice == 'C'):
            add_record(ID)
        elif (choice == 'E'):
            start_menu()
        choice = input()
	

def personal_profile(ID):
    print("books you've finished reading")
    for i in books[ID].keys():
        print(i, "comment: ", books[ID][i][2], "preference:", books[ID][i][3])
    print("input the book's title if you want to go to the book's profile, or press E to exit:")
    choice = input()
    while 1:
        if (choice in books[ID].keys()):
            book_profile(ID, choice)
        elif (choice == 'E'):
            start_menu()
        else:
            print("error, please input again")
        choice = input()

def book_profile(ID, title):
    print("___________________" + title + "_______________________\ncomment:")
    for i in range(ID_MAX):
        if title in books[i].keys():
            print(ID, ":" , books[i][title][2])

    print("\ninput A if u want to leave your reading comment and preference, or press E to exit")
    choice = input()
    while 1:
        if (choice == 'A'):
            print("leave ur comment")
            books[ID][title][2] = input()
            print("leave ur like degree(0~5)")
            books[ID][title][3] = int(input())
            book_profile(ID, title)
        elif (choice == 'E'):
            start_menu()
        else:
            print("error, please input again")
            choice = input()
def start_menu():
    print("Press A to add your borrowing record. Press B to see your personal profile. Press E to exit.")
    ID = 0
    choice = input();
    while 1:
        if choice == 'A':
            add_record(ID)
        elif choice == 'B':
            personal_profile(ID)
		
        elif choice == 'E':
            return
        
        else:
            print("error, please input again")
            choice = input()
for i in range(512):
    books.append({})
start_menu()
print("thanks for your using")
