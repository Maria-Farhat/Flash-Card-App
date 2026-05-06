import random
from tkinter import messagebox
from tkinter import *
import pandas

BACKGROUND_COLOR = "#B1DDC6"

current_card = {}
to_learn = {}

def save_progress():
	pandas.DataFrame(to_learn).to_csv('data/words_to_learn.csv', index=False)
	
# ---------------------------- WORD SELECTION ------------------------------- #

def next_card():
	"""Pick a new random card and display the front then flip it."""
	global current_card, flip_timer, to_learn
	if not to_learn:
		restart = messagebox.askyesno(
			title="Done!",
			message=" Restart from beginning?"
		)
		if restart:
			original_data = pandas.read_csv('data/Frequent arabic words - Sheet1.csv')
			to_learn = original_data.to_dict(orient='records')
		else:
			window.quit()

	save_progress()
	window.after_cancel(flip_timer)
	current_card = random.choice(to_learn)
	canvas.itemconfig(card_title, text='Arabic', fill='black')
	canvas.itemconfig(card_word, text= current_card['Arabic'], fill='black')
	canvas.itemconfig(card, image=front)
	flip_timer = window.after(3000, flip_card)


def flip_card():
	"""Flip the card to show the English translation."""
	canvas.itemconfig(card_title, text='English', fill='white')
	canvas.itemconfig(card_word, text=current_card['English'], fill='white')
	canvas.itemconfig(card, image=back)

# ---------------------------- USER ACTIONS ------------------------------- #

def remove_card():
	"""Remove known word from list and save progress."""
	to_learn.remove(current_card)
	data = pandas.DataFrame(to_learn)
	data.to_csv('data/words_to_learn.csv', index=False)
	next_card()

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title('Flashy')
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

canvas = Canvas(width=800, height=526)

front = PhotoImage(file='images/card_front.png')
back = PhotoImage(file='images/card_back.png')

card = canvas.create_image(400, 263, image=front)
card_title = canvas.create_text(400, 150, text='', font=('Ariel', 40, 'italic'))
card_word = canvas.create_text(400, 263, text='', font=('Ariel', 60, 'bold'))
canvas.config(bg=BACKGROUND_COLOR, highlightbackground=BACKGROUND_COLOR)
canvas.grid(row=0, column=0, columnspan=2)

# ---------------------------- BUTTONS ------------------------------- #

x_image = PhotoImage(file='images/wrong.png')
# Wrong answer button (skip word)
unknown_button = Button(image=x_image, highlightthickness=0, bd=0, command=next_card)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file='images/right.png')
# Correct answer button (mark as known)
known_button = Button(image=check_image, highlightthickness=0, bd=0, command=remove_card)
known_button.grid(row=1, column=1)


# Try to load words the user still needs to learn
try:
	data = pandas.read_csv('data/words_to_learn.csv')
except FileNotFoundError:
	# If no progress file exists, load the original dataset
	original_data = pandas.read_csv('data/Frequent arabic words - Sheet1.csv')
	to_learn = original_data.to_dict(orient='records')
else:
	to_learn = data.to_dict(orient='records')
	
# Start with first card
next_card()

window.mainloop()
