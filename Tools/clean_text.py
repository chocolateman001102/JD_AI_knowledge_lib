#!/usr/bin/env python3
"""
clean_text.py

A script to clean text by merging broken lines and replacing a specified bullet pattern
with an optional marker (default none). Provides a GUI for pasting input and viewing output.

Usage:
  python clean_text.py           # launch GUI input window, strips bullets
  python clean_text.py -b "*"    # launch GUI input, prefix bullets with "*"
  python clean_text.py -p "-"    # use '-' instead of default bullet pattern ''
"""
import argparse
import sys
import re

# Try importing tkinter for GUI output
try:
    import tkinter as tk
    from tkinter import scrolledtext
except ImportError:
    print("Error: tkinter is required for GUI. Please install it.")
    sys.exit(1)

def clean_text(text, bullet_marker='', pattern=''):
    """
    Merge broken lines, replace bullet pattern at start of lines with the given marker,
    and preserve paragraph breaks.
    """
    lines = text.splitlines()
    cleaned_lines = []
    buffer = ''
    bullet_re = re.compile(rf'^{re.escape(pattern)}')

    for line in lines:
        stripped = line.strip()
        # Paragraph break
        if not stripped:
            if buffer:
                cleaned_lines.append(buffer.strip())
                buffer = ''
            cleaned_lines.append('')
        # Line starts with bullet pattern
        elif bullet_re.match(stripped):
            if buffer:
                cleaned_lines.append(buffer.strip())
                buffer = ''
            content = bullet_re.sub('', stripped, count=1).strip()
            buffer = f"{bullet_marker} {content}" if bullet_marker else content
        else:
            # Continuation of previous line
            buffer += (' ' + stripped) if buffer else stripped

    if buffer:
        cleaned_lines.append(buffer.strip())

    return "\n".join(cleaned_lines)

def main():
    parser = argparse.ArgumentParser(description='Clean text via GUI input/output.')
    parser.add_argument('-b', '--bullet', default='', help='Optional bullet marker to prefix lines.')
    parser.add_argument('-p', '--pattern', default='', help='Bullet pattern to remove.')
    args = parser.parse_args()

    # Input window
    root = tk.Tk()
    root.title("Paste Text to Clean")
    # Bring input window to the front
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(lambda: root.attributes('-topmost', False))

    input_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
    input_widget.pack(fill=tk.BOTH, expand=True)

    def on_clean():
        raw = input_widget.get('1.0', tk.END).strip()
        cleaned = clean_text(raw, bullet_marker=args.bullet, pattern=args.pattern)
        # Output window
        out_win = tk.Toplevel(root)
        out_win.title("Cleaned Text Output")
        out_win.lift()
        out_win.attributes('-topmost', True)
        out_win.after_idle(lambda: out_win.attributes('-topmost', False))

        lines = cleaned.split('\n')
        rows = max(len(lines), 1)
        # Compute width: avoid generator vs int comparison, ensure at least 1 column
        cols = max([len(line) for line in lines] + [1])
        text_widget = scrolledtext.ScrolledText(out_win, wrap=tk.WORD, width=cols, height=rows)
        text_widget.pack()
        text_widget.insert(tk.END, cleaned)
        text_widget.configure(state='disabled')

        out_win.update_idletasks()
        width_px = text_widget.winfo_reqwidth()
        height_px = text_widget.winfo_reqheight()
        out_win.geometry(f"{width_px}x{height_px}")
        out_win.resizable(False, False)

    btn = tk.Button(root, text="Clean", command=on_clean)
    btn.pack(pady=5)
    root.mainloop()

if __name__ == '__main__':
    main() 