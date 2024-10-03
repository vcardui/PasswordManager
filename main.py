from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- CONSTANTS ------------------------------- #
WHITE = "#ffffff"
BLACK = "#000000"
FONT = ("Arial", 14)


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def create_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for i in range(randint(8, 10))]
    password_symbols = [choice(symbols) for i in range(randint(2, 4))]
    password_numbers = [choice(numbers) for i in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)

    password_input.delete(0, END)
    pyperclip.copy(f"{password}")
    password_input.insert(0, f"{password}")

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_data():
    website_var = website_input.get()
    email_username_var = email_username_input.get()
    password_var = password_input.get()
    new_data = {
        website_var.lower(): {
            "email": email_username_var,
            "password": password_var,
        }
    }

    if "" in (website_var, email_username_var, password_var):
        messagebox.showinfo(title="Wait!", message="Watch out! Please don't leave any fields empty")
    else:
        # save_data_OK = messagebox.askokcancel(title=website_var, message=f"Entered data is:\nWebsite: {website_var}\n
        # User:{email_username_var}\nPassword:{password_var}\nProceed to save data?")
        # if save_data_OK:
        try:
            with open(f"myPass_record.json", mode="r") as passwordRecord:
                # Reading old data
                data = json.load(passwordRecord)
        except FileNotFoundError:
            with open(f"myPass_record.json", mode="w") as passwordRecord:
                json.dump(new_data, passwordRecord, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open(f"myPass_record.json", mode="w") as passwordRecord:
                # Saving updated data
                json.dump(data, passwordRecord, indent=4)
        finally:
            messagebox.showinfo(title="Task complete", message="New registry has been successfully added")

            website_input.delete(0, END)
            email_username_input.delete(0, END)
            email_username_input.insert(0, "vanessa@reteguin.com")
            password_input.delete(0, END)

# ----------------------- SEARCH FOR PASSWORD ------------------------- #
def search_password():
    website_var = website_input.get()
    website_var.lower()

    with open(f"myPass_record.json", mode="r") as passwordRecord:
        # Reading old data
        data = json.load(passwordRecord)
        if website_var in data:
            email_search_var = data[website_var]["email"]
            password_search_var = data[website_var]["password"]
            messagebox.showinfo(title="Success", message=f"User: {email_search_var}\nPassword: {password_search_var}")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20, background=WHITE)

# MyPass Logo
canvas = Canvas(width=200, height=200, bg=WHITE, highlightthickness=0)
myPass_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=myPass_img)
canvas.grid(column=1, row=0)

# Label
website = Label(text="Website:", font=FONT, fg=BLACK, bg=WHITE)
website.grid(column=0, row=1)

email_username = Label(text="Email/Username:", fg=BLACK, font=FONT, bg=WHITE)
email_username.grid(column=0, row=2)

password = Label(text="Password:", font=FONT, fg=BLACK, bg=WHITE)
password.grid(column=0, row=3)

# Entry
website_input = Entry(width=21, highlightbackground=WHITE, fg=BLACK, bg=WHITE)
website_input.grid(column=1, row=1)
website_input.focus()

email_username_input = Entry(width=38, highlightbackground=WHITE, fg=BLACK, bg=WHITE)
email_username_input.grid(row=2, column=1, columnspan=2)
email_username_input.insert(0, "vanessa@reteguin.com")

password_input = Entry(width=21, highlightbackground=WHITE, fg=BLACK, bg=WHITE)
password_input.grid(column=1, row=3)

# Button
search = Button(width=13, text="Search", highlightbackground=WHITE, command=search_password)
search.grid(column=2, row=1)

generate_password = Button(text="Generate Password", highlightbackground=WHITE, command=create_password)
generate_password.grid(column=2, row=3)

add = Button(width=36, text="Add", highlightbackground=WHITE, command=save_data)
add.grid(column=1, row=4, columnspan=2)

window.mainloop()
