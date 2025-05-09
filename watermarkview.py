import tkinter as tk
from tkinter import scrolledtext
import unicodedata

# All common watermark or suspicious Unicode whitespace/invisible chars
WATERMARK_CHARS = {
    '\u00A0': "No-Break Space",
    '\u034F': "Combining Grapheme Joiner",
    '\u061C': "Arabic Letter Mark",
    '\u115F': "Hangul Filler",
    '\u1160': "Hangul Jungseong Filler",
    '\u1680': "Ogham Space Mark",
    '\u180E': "Mongolian Vowel Separator",
    '\u2000': "En Quad",
    '\u2001': "Em Quad",
    '\u2002': "En Space",
    '\u2003': "Em Space",
    '\u2004': "Three-Per-Em Space",
    '\u2005': "Four-Per-Em Space",
    '\u2006': "Six-Per-Em Space",
    '\u2007': "Figure Space",
    '\u2008': "Punctuation Space",
    '\u2009': "Thin Space",
    '\u200A': "Hair Space",
    '\u200B': "Zero Width Space",
    '\u200C': "Zero Width Non-Joiner",
    '\u200D': "Zero Width Joiner",
    '\u200E': "Left-to-Right Mark",
    '\u200F': "Right-to-Left Mark",
    '\u202F': "Narrow No-Break Space",
    '\u205F': "Medium Mathematical Space",
    '\u2060': "Word Joiner",
    '\u2061': "Function Application",
    '\u2062': "Invisible Times",
    '\u2063': "Invisible Separator",
    '\u2064': "Invisible Plus",
    '\u206A': "Inhibit Symmetric Swapping",
    '\u206B': "Activate Symmetric Swapping",
    '\u206C': "Inhibit Arabic Form Shaping",
    '\u206D': "Activate Arabic Form Shaping",
    '\u206E': "National Digit Shapes",
    '\u206F': "Nominal Digit Shapes",
    '\u2800': "Braille Pattern Blank",
    '\u3000': "Ideographic Space",
    '\u3164': "Hangul Filler",
    '\uFEFF': "Zero Width No-Break Space (BOM)",
    '\uFFA0': "Halfwidth Hangul Filler"
}

def scan_unicode_chars():
    text = text_input.get("1.0", tk.END)
    output_display.delete("1.0", tk.END)
    found = False

    for idx, char in enumerate(text):
        if char in WATERMARK_CHARS:
            found = True
            codepoint = f"U+{ord(char):04X}"
            name = WATERMARK_CHARS.get(char, unicodedata.name(char, "Unknown"))
            output_display.insert(tk.END, f"Position {idx}: {codepoint} — {name}\n")

    if not found:
        output_display.insert(tk.END, "No watermark or invisible Unicode characters found.")

def remove_watermark_chars():
    text = text_input.get("1.0", tk.END)
    cleaned = ''.join(c for c in text if c not in WATERMARK_CHARS)
    text_input.delete("1.0", tk.END)
    text_input.insert(tk.END, cleaned)
    output_display.delete("1.0", tk.END)
    output_display.insert(tk.END, "Watermark characters removed.")

# GUI Setup
root = tk.Tk()
root.title("Unicode Watermark Scanner")
root.geometry("700x600")

tk.Label(root, text="Paste your text below:").pack()

text_input = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10)
text_input.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

button_frame = tk.Frame(root)
button_frame.pack(pady=5)

tk.Button(button_frame, text="Scan for Watermarks", command=scan_unicode_chars).pack(side=tk.LEFT, padx=10)
tk.Button(button_frame, text="Remove Watermarks", command=remove_watermark_chars).pack(side=tk.LEFT, padx=10)

tk.Label(root, text="Scan Output:").pack()

output_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=15, bg="#f4f4f4")
output_display.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

root.mainloop()
