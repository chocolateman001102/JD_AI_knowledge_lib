#!/usr/bin/env python3
import sys
import os
import glob

def merge_paragraphs(lines):
    """
    Join lines that do not end with a period to the next line.
    Preserve lines ending with a period as sentence boundaries, and keep blank lines.
    """
    out = []
    buffer = ""
    for ln in lines:
        stripped = ln.strip()
        # Blank line: flush any buffer, then output a blank line
        if stripped == "":
            if buffer:
                out.append(buffer + "\n")
                buffer = ""
            out.append("\n")
        else:
            # If the line ends with a full-stop, it's a sentence boundary
            if stripped.endswith('.'):
                if buffer:
                    buffer += ' ' + stripped
                    out.append(buffer + '\n')
                    buffer = ''
                else:
                    out.append(stripped + '\n')
            else:
                # No full-stop: accumulate into buffer
                buffer = (buffer + ' ' + stripped) if buffer else stripped
    # Flush any remaining text
    if buffer:
        out.append(buffer + "\n")
    return out

def main():
    # ensure at least one path argument
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <file_or_directory>  # wrap paths containing spaces in quotes, or they will be auto-joined")
        sys.exit(1)

    # combine all args into one path (helps handle unquoted spaces)
    path = " ".join(sys.argv[1:])
    # Determine if path is a directory or single file
    if os.path.isdir(path):
        files = glob.glob(os.path.join(path, "*.txt"))
    elif os.path.isfile(path) and path.lower().endswith('.txt'):
        files = [path]
    else:
        print(f"Error: '{path}' is not a .txt file or directory.")
        sys.exit(1)

    for filepath in files:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()
            merged = merge_paragraphs(lines)
            with open(filepath, "w", encoding="utf-8") as f:
                f.writelines(merged)
            print(f"Processed {os.path.basename(filepath)}")
        except Exception as e:
            print(f"Failed to process {filepath}: {e}")

if __name__ == "__main__":
    main() 