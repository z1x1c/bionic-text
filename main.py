def main():
    # convert pdf for bionic reading
    txt = "This is a sample text."
    print(f"Old: {txt}")
    print(f"New: {convert_text(txt)}")

def convert_text(txt):
    words = txt.strip().split()
    new_words = []
    for i in range(len(words)):
        word = words[i]
        if not(len(word) == 1):
            index = len(word) // 2
            new_word = "**" + word[:index] + "**" + word[index:]
            new_words.append(new_word)
        else:
            new_words.append(word)
    bionic = (" ").join(new_words)
    return bionic

main()
