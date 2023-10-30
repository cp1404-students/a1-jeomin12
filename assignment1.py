"""
Name: Jeomin Gimmi
Date started: 20/10/2023
GitHub URL: https://github.com/cp1404-students/a1-jeomin12
"""

import csv

# Declare some global constants
SONGS_FILE = "songs.csv"
LEARNED_CHAR = 'l'
UNLEARNED_CHAR = 'u'

def main():
    """ Main function for song manager program."""

    print("Song List 1.0 - by Jeomin Gimmi")
    songs = load_songs()

    while True:
        print("Menu:")
        print("D - Display songs")
        print("A - Add new song")
        print("C - Complete a song")
        print("Q - Quit")
        choice = input(">>> ").strip().lower()

        # Perform required action based on user choice
        if choice == 'd':
            display_songs(songs)
        elif choice == 'a':
            add_song(songs)
        elif choice == 'c':
            complete_song(songs)
        elif choice == 'q':
            save_songs(songs)
            print("Make some music!")
            break
        else:
            print("Invalid menu choice")

def load_songs():
    """ Load songs from a CSV file."""

    # This list will store all the songs loaded from the file
    songs = []

    # Handle error when file is not found
    try:
        with open(SONGS_FILE, newline='', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                title, artist, year, learned = row
                songs.append(
                    [title, artist, int(year), learned == LEARNED_CHAR])

        print(f"{len(songs)} songs loaded.")
    except FileNotFoundError:
        print("No songs found. Starting with an empty list.")
    return songs


def save_songs(songs):
    """ Save songs to a CSV file."""

    with open(SONGS_FILE, newline='', mode='w') as file:
        writer = csv.writer(file)
        for song in songs:
            # Set the learn status to 'u' or 'l' based on whether song is learned or not.
            learned_char = LEARNED_CHAR if song[3] else UNLEARNED_CHAR

            writer.writerow([song[0], song[1], song[2], learned_char])

    print(f"{len(songs)} songs saved to {SONGS_FILE}")


def display_songs(songs):
    """ Display a list of songs."""

    if not songs:
        print("Song list is empty!")
    else:
        # Sort the songs based on year and title
        songs.sort(key=lambda song: (song[2], song[0]))

        max_title_length = max(len(song[0]) for song in songs)
        max_artist_length = max(len(song[1]) for song in songs)
        max_num_width = len(str(len(songs)))

        for i, song in enumerate(songs, start=1):
            # Set status to space or * based on whether song is learned or not
            status = ' ' if song[3] else '*'

            title_padding = max_title_length - len(song[0])
            artist_padding = max_artist_length - len(song[1])

            print(
                f"{i:>{max_num_width}}. {status} {song[0]}{' ' * title_padding}"
                f" - {song[1]}{' ' * artist_padding} ({song[2]})")

        # Determine and print the number of songs learned and unlearned
        learned_count = sum(1 for song in songs if song[3])
        unlearned_count = len(songs) - learned_count
        print(
            f"{learned_count} songs learned, {unlearned_count} songs still to "
            f"learn.")


def get_input(prompt):
    """ Get user input with error checking."""

    user_input = input(prompt)

    while user_input == "":
        print("Input can not be blank.")
        user_input = input(prompt)
    return user_input


def add_song(songs):
    """ Add a new song to the list."""

    print("Enter details for a new song.")
    title = get_input("Title: ")
    artist = get_input("Artist: ")
    year = input("Year: ")

    while True:

        # Catch all invalid inputs
        try:
            if int(year) <= 0:
                print("Number must be > 0.")
            else:
                break
        except ValueError:
            print("Invalid input; enter a valid number.")
        year = input("Year: ")

    # Append the new song into the song list
    songs.append([title, artist, int(year), False])
    print(f"{title} by {artist} ({year}) added to song list.")


def complete_song(songs):
    """ Function to mark a song as learned."""

    # Check if there are any more songs to learn
    # If no more songs to learn, then print error and exit
    unlearned_songs = [song for song in songs if not song[3]]
    if not unlearned_songs:
        print("No more songs to learn!")
        return

    print("Enter the number of a song to mark as learned.")

    while True:
        try:
            song_number = int(input(">>> "))

            if song_number <= 0:
                print("Number must be > 0.")
            elif 1 <= song_number <= len(songs):
                break
            else:
                print("Invalid song number")
        except ValueError:
            print("Invalid song number")

    # Fetch the song from the song list
    song = songs[song_number - 1]

    # Check if song is learned or not learned
    if song[3]:
        print(f"You have already learned {song[0]}")
    else:
        song[3] = True
        print(f"{song[0]} by {song[1]} learned")

if __name__ == '__main__':
    main()
