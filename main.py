from tkinter import *
import pandas
import random
from tkinter import messagebox

BACKGROUND_COLOR = "#B1DDC6"

current_card = None
timer = None
try:
    data_file = pandas.read_csv('./data/words_to_learn.csv')
except FileNotFoundError:
    data_file = pandas.read_csv('./data/french_words.csv')
else:
    pass
finally:
    to_learn = data_file.to_dict(orient='records')


def close():
    if messagebox.askokcancel('Do you want to exit'):
        save_data = pandas.DataFrame(to_learn)
        save_data.to_csv('./data/words_to_learn.csv', index=False)
        window.destroy()



def word_slection2():
    col = random.randint(0, len(data_file['French']))
    dic = data_file.iloc[[col]]
    new_eng_word2 = dic['English'].item()
    new_fr_word2 = dic['French'].item()
    return new_fr_word2, new_eng_word2


def word_selection():
    new_french_word = random.choice(data_file['French'])
    selected_row = data_file[data_file.French == new_french_word]
    english_meaning = selected_row['English'].item()
    return new_french_word, english_meaning


def right_pressed():
    to_learn.remove(current_card)
    next_word()
    # messagebox.showinfo(message='Card removed from the deck')


def flip():
    flashcard.itemconfig(front_back, image=card_back)
    flashcard.itemconfig(front_back_lang, text='English', fill='white')
    flashcard.itemconfig(fr_en_word, text=current_card['English'], fill='white')


def next_word():
    global timer
    if timer is not None:
        window.after_cancel(timer)
    print(to_learn)
    random_words = random.choice(to_learn)
    next_french_word = random_words['French']
    global current_card
    current_card = random_words
    flashcard.itemconfig(front_back, image=card_front)
    flashcard.itemconfig(fr_en_word, text=next_french_word, fill='black')
    flashcard.itemconfig(front_back_lang, text='French', fill='black')

    timer = window.after(3000, flip)


window = Tk()
window.title('Flash Card')
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flashcard = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file='./images/card_front.png')
front_back = flashcard.create_image(400, 263, image=card_front)
card_back = PhotoImage(file='./images/card_back.png')
french_word, english_word = word_selection()
fr_en_word = flashcard.create_text(400, 263, fill='black', text=french_word, font=('Arial', 60, 'bold'))
front_back_lang = flashcard.create_text(400, 150, fill='black', text='French', font=('Arial', 40, 'italic'))
flashcard.grid(row=0, column=0, columnspan=2)

right_image = PhotoImage(file='./images/right.png')
right_button = Button(image=right_image, highlightthickness=0, command=right_pressed)
right_button.grid(row=1, column=1)

wrong_image = PhotoImage(file='./images/wrong.png')
wrong_button = Button(image=wrong_image, highlightthickness=0, command=next_word)
wrong_button.grid(row=1, column=0)

next_word()

window.protocol('WM_DELETE_WINDOW', close)
window.mainloop()
