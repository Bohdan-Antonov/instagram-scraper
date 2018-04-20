import time
import tkMessageBox
import ttk
from Tkinter import *
from datetime import datetime
import selenium_engine
import threading


POST_TYPE = ["Top", "Recent", "Top and Recent"]
USER_TYPE = ["Post Owner", "Commenters"]


# =========================== #


def start_thread():
    newthread = threading.Thread(target=engine)
    newthread.start()

def engine():
    try:
        print ('Collecting... Might take few minutes depending on amount of users\n')
        time.sleep(0.5)
        allUsers = []
        hashtag = hashtag_entry.get().replace('#', '')
        post_type = cb1.get()
        amount = int(count_entry.get())
        user_type = cb2.get()
        if post_type == 'Top':
            if user_type == 'Post Owner':
                allUsers = selenium_engine.get_top_posts_owners(hashtag)
            elif user_type == 'Commenters':
                allUsers = selenium_engine.get_top_posts_commenters(hashtag, amount)
        elif post_type == 'Recent':            
            if user_type == 'Post Owner':                
                allUsers = selenium_engine.get_recent_posts_owners(hashtag, amount)
            elif user_type == 'Commenters':
                allUsers = selenium_engine.get_recent_posts_commenters(hashtag, amount)
        elif post_type == 'Top and Recent':
            allUsers = []
            if user_type == 'Post Owner':
                topPosts = selenium_engine.get_top_posts_owners(hashtag)
                for user in topPosts:
                    allUsers.append(user)
                if len(allUsers) < amount:
                    recentPosts = selenium_engine.get_recent_posts_owners(hashtag, (amount - 9))
                    for user in recentPosts:
                        allUsers.append(user)
            elif user_type == 'Commenters':
                topPosts = selenium_engine.get_top_posts_commenters(hashtag, amount)
                for user in topPosts:
                    allUsers.append(user)
                if len(allUsers) < amount:
                    recentPosts = selenium_engine.get_recent_posts_commenters(hashtag, (amount - len(topPosts)))
                    for user in recentPosts:
                        allUsers.append(user)
        if allUsers is False:
            pass
        else:
            save(allUsers, user_type, post_type, hashtag)
    except ValueError as e:
        if str(e) == 'No JSON object could be decoded':
            tkMessageBox.showinfo("Error", "No hashtag given")
        else:
            tkMessageBox.showinfo("Error", "Incorrect amount")


# =========================== #


# Save to excel


# =========================== Tkinter =========================== #


master = Tk()
master.title('Instabot')
master.geometry('250x250')
master.resizable(width=False, height=False)


# ========== Hashtag input ========== #


hashtag_label = Label(master, text='Hashtag')
hashtag_entry = Entry(master, justify='center')

hashtag_label.pack()
hashtag_entry.pack()



# ========== Post Type ========== #


cb1_label = Label(master, text='Post Type')
cb1 = ttk.Combobox(master, values=POST_TYPE, justify='center')
cb1.set(POST_TYPE[0])

cb1_label.pack()
cb1.pack(padx=5, pady=3)


# ========== Amount Of Users ========== #


count_label = Label(master, text='Number of accounts')
count_entry = Entry(master, justify='center')
count_entry.insert(END, '100')

count_label.pack()
count_entry.pack()


# ========== Users Type ========== #


cb2_label = Label(master, text='User Type')
cb2 = ttk.Combobox(master, values=USER_TYPE, justify='center')
cb2.set(USER_TYPE[0])

cb2_label.pack()
cb2.pack(padx=5, pady=3)


# ========== Start Button ========== #



btn = Button(master, text='START', command=start_thread)
btn.pack(fill=X, padx=5, pady=15)


# =============================================================== #


if __name__ == '__main__':
    master.mainloop()
