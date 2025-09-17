# typing_test.py
import time
import random
import textwrap

EXAMPLES = [
    "The quick brown fox jumps over the lazy dog.",
    "Practice makes perfect — keep typing and improving every day!",
    "Typing speed is measured in words per minute, abbreviated as WPM.",
    "Simplicity is the soul of efficiency.",
    "Never stop learning; small consistent steps lead to big progress."
]

def get_prompt():
    return random.choice(EXAMPLES)

def measure_typing(prompt):
    print("\nType the following sentence EXACTLY as shown and press Enter when done:\n")
    print(textwrap.fill(prompt, width=70))
    print("\nPress Enter when you are ready to start...")
    input()  # Let user get ready
    print("Start typing now:")
    start = time.perf_counter()
    typed = input()
    end = time.perf_counter()
    elapsed = end - start
    return typed, elapsed

def compute_wpm(typed, elapsed_seconds):
    # WPM commonly uses 5 characters per word; we'll use a words-based metric too.
    if elapsed_seconds <= 0:
        return 0.0
    # option A: word count based
    word_count = len(typed.split())
    wpm_words = (word_count / elapsed_seconds) * 60.0
    # option B: characters/5 standard
    chars = len(typed)
    wpm_chars = ((chars / 5.0) / elapsed_seconds) * 60.0
    return wpm_words, wpm_chars

def compute_accuracy(prompt, typed):
    # Character-level accuracy
    total = max(len(prompt), 1)
    correct_chars = sum(1 for p, t in zip(prompt, typed) if p == t)
    # any extra typed beyond prompt are incorrect
    accuracy = (correct_chars / total) * 100.0
    # word-level accuracy (simple)
    prompt_words = prompt.split()
    typed_words = typed.split()
    correct_words = sum(1 for p, t in zip(prompt_words, typed_words) if p == t)
    word_accuracy = (correct_words / max(len(prompt_words), 1)) * 100.0
    # collect first few differences for feedback
    diffs = []
    for i, p in enumerate(prompt):
        t = typed[i] if i < len(typed) else None
        if t != p:
            diffs.append((i, p, t))
            if len(diffs) >= 6:
                break
    return accuracy, word_accuracy, diffs

def pretty_report(prompt, typed, elapsed):
    wpm_words, wpm_chars = compute_wpm(typed, elapsed)
    accuracy, word_acc, diffs = compute_accuracy(prompt, typed)

    print("\n--- Results ---")
    print(f"Time taken      : {elapsed:.2f} seconds")
    print(f"Words typed     : {len(typed.split())}")
    print(f"Characters typed: {len(typed)}")
    print(f"WPM (by words)  : {wpm_words:.2f}")
    print(f"WPM (chars/5)   : {wpm_chars:.2f}")
    print(f"Char accuracy   : {accuracy:.2f}%")
    print(f"Word accuracy   : {word_acc:.2f}%")

    if not diffs:
        print("Nice! No character-level differences detected in the first compared range.")
    else:
        print("\nSample differences (position, expected, you typed):")
        for pos, expected, got in diffs:
            got_display = got if got is not None else "<nothing>"
            print(f"  pos {pos:3d} : expected '{expected}'  typed '{got_display}'")

def main():
    print("Typing Speed & Accuracy Tracker")
    print("--------------------------------")
    while True:
        prompt = get_prompt()
        typed, elapsed = measure_typing(prompt)
        pretty_report(prompt, typed, elapsed)

        again = input("\nTry again? (y/n): ").strip().lower()
        if again not in ("y", "yes"):
            print("Good job — keep practicing!")
            break

if __name__ == "__main__":
    main()

