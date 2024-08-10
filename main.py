import pygame
import nltk
from nltk.corpus import words
import random

nltk.download('words')
word_list = words.words()
pygame.font.init()

WIDTH, HEIGHT = 1000, 800
LINE_LENGTH = 20
LINE_SPACING = 15
START_MISTAKE = 50
HANGMAN_START_X = WIDTH - 300
HANGMAN_START_Y = 70

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hanging Man")

BG = pygame.transform.scale(pygame.image.load("Hanging_man_BG.jpg"), (WIDTH, HEIGHT))

FONT = pygame.font.SysFont("comicsans", 30)

def random_word():
   return random.choice(word_list)

def draw_title():
    title_text = FONT.render("six mistakes and you out ;)", 1, "red")
    WIN.blit(title_text, (WIDTH / 2 - title_text.get_width() / 2, 50))

def draw_hangman(count_mistakes):
    # Base
    pygame.draw.line(WIN, (255, 255, 255), (HANGMAN_START_X, HANGMAN_START_Y + 300), (HANGMAN_START_X + 100, HANGMAN_START_Y + 300), 5)
    # Pole
    pygame.draw.line(WIN, (255, 255, 255), (HANGMAN_START_X + 50, HANGMAN_START_Y + 300), (HANGMAN_START_X + 50, HANGMAN_START_Y), 5)
    # Beam
    pygame.draw.line(WIN, (255, 255, 255), (HANGMAN_START_X + 50, HANGMAN_START_Y), (HANGMAN_START_X + 150, HANGMAN_START_Y), 5)
    # Rope
    pygame.draw.line(WIN, (255, 255, 255), (HANGMAN_START_X + 150, HANGMAN_START_Y), (HANGMAN_START_X + 150, HANGMAN_START_Y + 50), 5)

    if count_mistakes >= 1:  # Head
        pygame.draw.circle(WIN, (255, 255, 255), (HANGMAN_START_X + 150, HANGMAN_START_Y + 80), 30, 5)
    if count_mistakes >= 2:  # Body
        pygame.draw.line(WIN, (255, 255, 255), (HANGMAN_START_X + 150, HANGMAN_START_Y + 110), (HANGMAN_START_X + 150, HANGMAN_START_Y + 200), 5)
    if count_mistakes >= 3:  # Left Arm
        pygame.draw.line(WIN, (255, 255, 255), (HANGMAN_START_X + 150, HANGMAN_START_Y + 140), (HANGMAN_START_X + 120, HANGMAN_START_Y + 170), 5)
    if count_mistakes >= 4:  # Right Arm
        pygame.draw.line(WIN, (255, 255, 255), (HANGMAN_START_X + 150, HANGMAN_START_Y + 140), (HANGMAN_START_X + 180, HANGMAN_START_Y + 170), 5)
    if count_mistakes >= 5:  # Left Leg
        pygame.draw.line(WIN, (255, 255, 255), (HANGMAN_START_X + 150, HANGMAN_START_Y + 200), (HANGMAN_START_X + 120, HANGMAN_START_Y + 250), 5)
    if count_mistakes >= 6:  # Right Leg
        pygame.draw.line(WIN, (255, 255, 255), (HANGMAN_START_X + 150, HANGMAN_START_Y + 200), (HANGMAN_START_X + 180, HANGMAN_START_Y + 250), 5)

def find_letter_positions(word, letter):
    positions = [index for index, char in enumerate(word) if char == letter]
    return positions

def draw_lines_for_word(word):
    word_length = len(word)
    x = 50
    y = 700

    for char in range(word_length):
        pygame.draw.line(WIN, (0,255,0), (x, y), (x + LINE_LENGTH, y), 2)
        x += LINE_LENGTH + LINE_SPACING

def draw_letters(word, guessed_letters):
    x = 50
    y = 700 - 50
    for char in word:
        if char in guessed_letters:
            text_surface = FONT.render(char, True, (0, 255, 0))
            WIN.blit(text_surface, (x, y))
        x += LINE_LENGTH + LINE_SPACING

def draw_mistake_letters(guessed_letters,word, START_MISTAKE):
    y = 700
    incorrect_letters = [letter for letter in guessed_letters if letter not in word]
    incorrect_letters_str = ", ".join(incorrect_letters)
    text_surface = FONT.render(incorrect_letters_str, True, (255, 0, 0))
    WIN.blit(text_surface, (START_MISTAKE, y))


def draw(word, guessed_letters,count_mistakes):
    WIN.blit(BG, (0, 0))
    draw_title()
    draw_lines_for_word(word)
    draw_mistake_letters(guessed_letters,word, START_MISTAKE)
    draw_letters(word, guessed_letters)
    draw_hangman(count_mistakes)
    pygame.display.update()

def main():
    word = random_word().lower()
    guessed_letters = set()


    print(word)
    still_play = True
    word_len = len(word)
    count_mistakes = 0
    draw(word, guessed_letters, count_mistakes)

    while still_play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                still_play = False
                break
            print(f"count_mistakes =  '{count_mistakes}")
            print(f"word_len =  '{word_len}")

            if event.type == pygame.KEYDOWN:
                if pygame.K_a <= event.key <= pygame.K_z:
                    letter = pygame.key.name(event.key)

                if len(letter) == 1 and letter.isalpha() and letter not in guessed_letters:
                    print(f"Letter '{letter}' pressed!")
                    guessed_letters.add(letter)
                    if letter in word:
                        word_len -= word.count(letter)
                    else:
                        count_mistakes += 1
                        print(f"count_mistakes =  '{count_mistakes}")
                        print(f"word_len =  '{word_len}")
                    if(word_len ==0):
                       draw(word, guessed_letters, count_mistakes)
                       win_text = FONT.render("You win! :)", 1, "white")
                       WIN.blit(win_text, (WIDTH / 2 - win_text.get_width() / 2, HEIGHT / 2 - win_text.get_height() / 2))
                       pygame.display.update()
                       pygame.time.delay(4000)
                       still_play = False

                    elif (count_mistakes == 6):
                      draw(word, guessed_letters, count_mistakes)
                      lose_text = FONT.render("You lose! :(", 1, "white")
                      WIN.blit(lose_text, (WIDTH / 2 - lose_text.get_width() / 2, HEIGHT / 2 - lose_text.get_height() / 2))
                      pygame.display.update()
                      pygame.time.delay(4000)

                else:
                    invalid_text = FONT.render("Invalid input. you already try this  key", 1, "white")
                    WIN.blit(invalid_text, (WIDTH / 2 - invalid_text.get_width() / 2, HEIGHT / 2 - invalid_text.get_height() / 2))
                    pygame.display.update()
                    pygame.time.delay(1000)
        draw(word, guessed_letters, count_mistakes)
    pygame.quit()

if __name__ == "__main__":
    main()




