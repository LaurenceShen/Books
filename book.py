import matplotlib as mp
import random
book_data = []
for i in range(10000):
    book_data.append(i)

record = []
books = []
ID_MAX = 512
stamp_postcard = {}
for i in range(ID_MAX):
    stamp_postcard[i] = [0, 0]

def add_record(ID): #紀錄已借書籍
    print("Please input your the book you've borrowed.")
    book = input() #輸入想建立的書籍
    record.append(book)
    books[ID][book] = [0, 1, 0, 0, 0, 0] #建立書籍資料：[判斷是否閱讀完成, 書籍分類, 閱讀心得, 個人喜愛程度, 目前頁數, 總頁數]
    while 1:
        print("Press C to continue.\nPress E to exit.")
        choice = input()
        if (choice == 'C'): #如果輸入C，則再次進行「增加借書紀錄」的服務
            add_record(ID)
        elif (choice == 'E'): #如果輸入E，則跳回至「起始畫面」
            start_menu()
            return
        else:
            print("Error! Please input again.")	

def personal_profile(ID): #回憶頁面
    while 1:
        print("Press A if you want to update your bookmarks.\nPress B if you want to know the books you\'ve finnished reading.\nPress E to exit.")
        choice = input()
        if choice == "A": #如果輸入A，則進行「更新閱讀進度」的服務
            print("Input the book you want to update.")
            book = input()
            bookmark(ID, book) #呼叫函式「更新書籤」
        elif choice == "B": #如果輸入B，則進行「查詢已完成閱讀書籍」的服務
            print("Books You've Finished Reading:")
            for i in books[ID].keys(): #將以輸入書名全遍歷以查看哪些書完成閱讀
                if books[ID][i][0] == 1:
                    print(i, "comment: ", books[ID][i][2], "preference:", books[ID][i][3]) #輸出完成書籍的閱讀心得及喜愛程度
            while 1:
                print("Input the book's title if you want to go to the book's profile.\nPress E to exit:") #讓使用者選擇是否進入手札
                book = input()
                if (book in books[ID].keys()): #確認輸入書名有在紀錄裡面
                    book_profile(ID, book) #呼叫函式「手札」
                    return
                elif (book == 'E'): #退回至「回憶頁面」
                    personal_profile(ID)
                    return
                else:
                    print("Error! Please input again.")
            return
        elif (choice == 'E'):
            start_menu()
            return
        else:
            print("Error! Please input again.")

def book_profile(ID, title): #書的手札
    print("___________________" + title + "_______________________\ncomment:")
    for i in range(ID_MAX):
        if title in books[i].keys():
            print(ID, ":" , books[i][title][2]) #輸出個人已留下的閱讀心得

    print("\nPress A if you want to leave your reading comment and preference.\nPress E to exit.")
    choice = input()
    while 1:
        if (choice == 'A'): #輸入A則留下閱讀心得及喜愛程度
            print("Leave your comment.")
            books[ID][title][2] = input() #更改書籍資料中閱讀心得的部分
            print("Leave your like degree(0~5).")
            books[ID][title][3] = int(input()) #更改書籍資料中喜愛程度的部分
            book_profile(ID, title)
            return
        elif (choice == 'E'):
            start_menu()
            return
        else:
            print("Error! Please input again.")
            choice = input()
def start_menu(): #起始畫面選項
    ID = 0 #因尚未有使用者資料，所以先預設使用者ID為0
    while 1:
        print("Press A to add your borrowing record.\nPress B to see your personal profile.\nPress E to exit.") #跳出選項
        choice = input() #記錄使用者輸入之選項
        if choice == 'A': #如果輸入A，則進行「增加借書紀錄」的服務
            add_record(ID)
            return
        elif choice == 'B': #如果輸入B，則進行「查看回憶頁面」的服務
            personal_profile(ID)
            return
        elif choice == 'E': #如果輸入E，則進行「離開」的服務
            return
        else: #如果輸入其他東西，則跳出「錯誤」訊息
            print("Error! Please input again.")

def bookmark(ID, title): #更新看書進度
    print("How many pages you've read?")
    pages_read = int(input()) #輸入已閱讀到的頁面
    books[ID][title][5] = 100 #因尚未有完整的資料庫，所以每本書先預設為100頁
    books[ID][title][4] = pages_read
    print("You\'ve finished " + str(books[ID][title][4] / books[ID][title][5] * 100) + "%" + " of the book.") #以%數表示閱讀進度
    gain_stamp(ID, title) #如果閱讀完書籍則自動獲取郵票
    return

def gain_stamp(ID, title): #獲取郵票
    if books[ID][title][4] == books[ID][title][5]: #判斷是否閱讀完書籍
        stamp_postcard[ID][0] += 1 #記錄個人郵票數量
        books[ID][title][0] = 1
    if stamp_postcard[ID][0] == 3: #每三張郵票換一張明信片
        stamp_postcard[ID][0] = 0
        stamp_postcard[ID][1] += 1
    return
def show_stamp(ID): #展示郵票
    print("Now, you've got " + str(stamp[ID][0]) + " stamps and " + str(stamp[ID][1]) + " postcards!")
    return

def random_recommandation(): #隨機推薦書本
    random_num = random.randint(1,10000) #隨機生出一個數字當作資料庫中書的次序
    return (book_data[random_num]) #回傳資料庫中的書

#def chart(ID):


for i in range(512):
    books.append({})
start_menu()
print("thanks for your using")
