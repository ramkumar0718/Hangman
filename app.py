import pygame
import string
import math
import random
from os import path
pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 900, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman")

RADIUS = 26
START_BTN_X = 70
START_BTN_Y = (HEIGHT + 380) // 2
PADDING = 12
COLUMNS = 13

WHITE = (255,255,255)
BLACK = (0, 0, 0)
BLUE = (80, 80, 80)

HANGMAN_PICS = [pygame.image.load(r"imgs/img1.png"), pygame.image.load(r"imgs/img2.png"), pygame.image.load(r"imgs/img3.png"), pygame.image.load(r"imgs/img4.png"), pygame.image.load(r"imgs/img5.png"), pygame.image.load(r"imgs/img6.png"), pygame.image.load(r"imgs/img7.png")]
HANGMAN_PIC_NO = 0
BUTTONS = []
LETTERS = list(string.ascii_uppercase)
SELECTED_WORD = ""
SELECTED_HINT = ""
SELECTED_WORD_SPLIT = []
GUESS_TEXT = []
RESULT = ""
PLAY_AGAIN = False

FPS = 15

BTN_FONT = pygame.font.SysFont("arial", 20)
WORD_FONT = pygame.font.SysFont("monospace", 30)
END_FONT = lambda font_size : pygame.font.SysFont("monospace", font_size)

def make_lines():
	select_word()
	global SELECTED_WORD, GUESS_TEXT

	for i in SELECTED_WORD_SPLIT:
		if i != " ":
			GUESS_TEXT.append("_ ")
		else:
			GUESS_TEXT.append(" ")

def display_lines():
	word_surface = WORD_FONT.render("".join(GUESS_TEXT), True, WHITE)
	word_rect = word_surface.get_rect(center=(WIDTH//2, HEIGHT//2 + 90))
	WIN.blit(word_surface, word_rect)

def select_word():
	global SELECTED_WORD, SELECTED_HINT, SELECTED_WORD_SPLIT

	file = open("words.txt", "r")
	file_reader = file.readlines()
	word = random.choice(file_reader)
	word_start = word.index("|") + 1
	SELECTED_HINT = word[:word_start - 1]
	if word == file_reader[-1]:
		SELECTED_WORD = word[word_start:].upper()
	else:
		SELECTED_WORD = word[word_start:-1].upper()
	SELECTED_WORD_SPLIT = list(SELECTED_WORD)

def display_image():
	if HANGMAN_PIC_NO <= 6:
		WIN.blit(pygame.transform.scale(HANGMAN_PICS[HANGMAN_PIC_NO], (280, 280)), (WIDTH//2 - 120, HEIGHT//2 - 250))
	else:
		end_game()

def display_hint():
	hint_phase = END_FONT(40).render(f"Hint : {SELECTED_HINT}", True, WHITE)
	WIN.blit(hint_phase, hint_phase.get_rect(center = (WIDTH//2, HEIGHT//3 - 180)))

def is_pointer_inside_circle(x, y, circle_x, circle_y):
    return math.sqrt((x - circle_x)**2 + (y - circle_y)**2) < RADIUS

def mouse_event():
	global HANGMAN_PIC_NO

	mouse_x, mouse_y = pygame.mouse.get_pos()
	for letter, (x, y) in BUTTONS:
		if is_pointer_inside_circle(mouse_x, mouse_y, x, y):
			if letter in SELECTED_WORD:
				letter_index = [i for i, char in enumerate(SELECTED_WORD) if char == letter]
				for i in letter_index:
					GUESS_TEXT[i] = letter
			else:
				HANGMAN_PIC_NO += 1
			BUTTONS.remove((letter, (x, y)))

def create_buttons():
	global BUTTONS

	for i, letter in enumerate(LETTERS):
		row = i // COLUMNS
		col = i % COLUMNS
		x = START_BTN_X + col * (2 * RADIUS + PADDING)
		y = START_BTN_Y + row * (2 * RADIUS + PADDING)
		BUTTONS.append((letter, (x, y)))

def display_buttons(x, y, text):
	pygame.draw.circle(WIN, BLUE, (x, y), RADIUS)
	btn_surface = BTN_FONT.render(text, True, WHITE)
	btn_rect = btn_surface.get_rect(center = (x, y))
	WIN.blit(btn_surface, btn_rect)

def check_winner():
	global RESULT

	if HANGMAN_PIC_NO <= 6 and SELECTED_WORD == "".join(GUESS_TEXT):
		RESULT = "Winner !!!"
		end_game()
	else:
		RESULT = "You Lost :)"

def end_game():
	global PLAY_AGAIN

	pygame.time.delay(1000)
	WIN.fill(BLACK)
	word_end = END_FONT(70).render(f"{RESULT}", True, WHITE)
	word_PLAY_AGAIN = END_FONT(45).render("Press any key to play again...", True, WHITE)
	word_phase = END_FONT(35).render(f"Word : {SELECTED_WORD}", True, WHITE)

	WIN.blit(word_end, word_end.get_rect(center=(WIDTH//2, HEIGHT//3 - 150)))
	WIN.blit(word_PLAY_AGAIN, word_PLAY_AGAIN.get_rect(center=(WIDTH//2, 300)))
	WIN.blit(word_phase, word_phase.get_rect(center=(WIDTH//2, 400)))
	PLAY_AGAIN = True

def reset_game():
	global HANGMAN_PIC_NO, LETTERS, SELECTED_WORD, SELECTED_HINT, SELECTED_WORD_SPLIT, GUESS_TEXT, RESULT, PLAY_AGAIN
	
	HANGMAN_PIC_NO = 0
	BUTTONS.clear()
	LETTERS = list(string.ascii_uppercase)
	SELECTED_WORD = ""
	SELECTED_HINT = ""
	SELECTED_WORD_SPLIT.clear()
	GUESS_TEXT.clear()
	RESULT = ""
	PLAY_AGAIN = False
	main()


def main():
	run = True
	clock = pygame.time.Clock()
	make_lines()
	create_buttons()

	while run:
		clock.tick()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				quit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_event()
			elif PLAY_AGAIN == True and event.type == pygame.KEYDOWN:
				reset_game()

		WIN.fill(BLACK)
		for letter, (x, y) in BUTTONS:
			display_buttons(x, y, letter)

		display_image()
		display_lines()
		display_hint()
		check_winner()
		if HANGMAN_PIC_NO >= 6:
			end_game()
		pygame.display.update()

if __name__ == "__main__":
	main()