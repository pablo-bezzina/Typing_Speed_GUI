import tkinter
from tkinter import messagebox
import random
import time
import datetime

NUMBER_OF_WORDS = 12
WHITE = '#FBFBFB'
SHUT_DOWN_AFTER_MINUTES = 10


class MachineBrain(tkinter.Tk):

    def __init__(self):
        super().__init__()

        self.title("Keystroke Counter.")
        self.minsize(width=500, height=500)
        self.config(padx=70, pady=70)

        self.game_text = tkinter.Label(text='Press START to begin testing your keyboard speed and accuracy.\n')
        self.game_text.grid(row=0, column=0, columnspan=3)

        with open('words.txt') as file:
            self.all_words = file.read().split('\n')

        self.words_to_display = []
        self.current_position = 0
        self.typing_in_progress = ''

        self.canvas = tkinter.Canvas(self, width=300, height=200, highlightthickness=0, bg=WHITE)
        self.this_word = self.canvas.create_text(150, 100, width=300, text='Press START!', justify='center',
                                                 anchor='center', font=('Roboto', 36, 'bold'))
        self.up_next = self.canvas.create_text(150, 120, width=300, text='',
                                               justify='center', anchor='center', font=('Roboto', 16, 'italic'))
        self.next_word = self.canvas.create_text(150, 150, width=300, text='',
                                                 justify='center', anchor='center', font=('Roboto', 20, 'bold'))
        self.canvas.grid(row=1, column=0, columnspan=3)

        self.ghost_label = tkinter.Label(text="")
        self.ghost_label.grid(column=1, columnspan=1, row=2)

        self.start_game_btt = tkinter.Button(text='START', command=self.countdown)
        self.start_game_btt.grid(row=3, column=0)

        self.reset_button = tkinter.Button(text='Reset', command=self.reset_game, state='disabled')
        self.reset_button.grid(row=3, column=2)

        self.stopper = False
        self.start_time = ''
        self.total_keys_pressed = 0
        self.unbind("<Key>")
        self.mainloop()

    def countdown(self):
        self.words_to_display = random.choices(self.all_words, k=NUMBER_OF_WORDS)
        self.current_position = 0
        self.total_keys_pressed = 0

        for item in ['3', '2', '1', 'GO!']:
            self.canvas.itemconfig(self.this_word, text=item)
            self.update()
            time.sleep(1)
        self.start_game()
        self.stopper = False
        self.timer()

    def start_game(self):
        self.canvas.itemconfig(self.this_word, text=self.words_to_display[0])
        self.canvas.coords(self.this_word, 150, 50)
        self.canvas.itemconfig(self.up_next, text='Up next:')
        self.canvas.itemconfig(self.next_word, text=self.words_to_display[1])
        self.reset_button.config(state='normal')
        self.start_game_btt.config(state='disabled')

        self.typing_in_progress = self.words_to_display[0]
        self.update()
        self.bind("<Key>", self.key_handler)
        self.start_time = datetime.datetime.now()

    def reset_game(self):
        answer = messagebox.askyesno('Are you sure?',
                                     "Please confirm you want to reset your game.")
        if answer:
            self.stopper = True
            self.canvas.itemconfig(self.up_next, text='')
            self.canvas.itemconfig(self.next_word, text='')
            self.countdown()

    def key_handler(self, event):
        self.total_keys_pressed += 1

        if self.typing_in_progress[0] == event.char.lower():
            self.typing_in_progress = self.typing_in_progress[1:]
            if self.typing_in_progress == '':
                self.change_word()
        else:
            self.typing_in_progress = self.words_to_display[self.current_position]

    def change_word(self):
        self.current_position += 1
        try:
            self.typing_in_progress = self.words_to_display[self.current_position]
        except IndexError:
            self.victory()
        else:
            self.canvas.itemconfig(self.this_word, text=self.words_to_display[self.current_position])
            if self.current_position != len(self.words_to_display) - 1:
                self.canvas.itemconfig(self.next_word, text=self.words_to_display[self.current_position + 1])
            else:
                self.canvas.itemconfig(self.next_word, text='')

    def count_letters(self):
        counter = 0
        for item in self.words_to_display:
            counter += len(item)
        return counter

    def victory(self):
        finish_time = datetime.datetime.now()
        time_elapsed = (finish_time - self.start_time).total_seconds()
        minutes = int(time_elapsed // 60)
        seconds = round(time_elapsed % 60, 1)
        right_keys = self.count_letters()
        keys_per_second = round(right_keys / seconds, 2)
        accuracy = round(100 * right_keys / self.total_keys_pressed, 2)
        messagebox.showinfo('You completed your challenge!',
                            f"Total letters displayed: {right_keys}.\n"
                            f"Total keystrokes: {self.total_keys_pressed}.\n"
                            f"Your accuracy is: {accuracy}%.\n\n"
                            f"It took you {minutes} minutes and {seconds} seconds.\n"
                            f"Your speed is: {keys_per_second} keys/sec.")
        answer = messagebox.askyesno('Want to go again?',
                                     "Do you want to play another round?")
        if answer:
            self.stopper = True
            self.canvas.itemconfig(self.up_next, text='')
            self.canvas.itemconfig(self.next_word, text='')
            self.countdown()
        else:
            self.quit()

    def timer(self, count=0):
        if self.stopper:
            pass
        else:
            if count == 60 * 2 * SHUT_DOWN_AFTER_MINUTES:
                self.quit()
            else:
                self.after(500, self.timer, count + 0.5)
