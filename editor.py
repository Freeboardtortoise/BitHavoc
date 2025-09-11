import curses
import sys

RIGHT_KEYS = set("qwertasdfgzxcvb12345`~!@#$%^&*()-_=+\\|")
LEFT_KEYS = set("yuiophjklnm67890[]{};:'\",.<>/?")

OPCODES = {
    "00000001": "set [1] to value of address [2]",
    "00000010": "read from user 1 bit into [1]",
    "00000011": "write [1]",
    "00000100": "set [1] to value of [2]",
    "00010100": "add [2] + [3] and place it in [1]",
    "00011100": "multiply [2] * [3] and place it in [1]",
    "00011000": "subtract [2] - [3] and place it in [1]",
    "00011010": "divide [2] / [3] and place it in [1]",
    "00100001": "if [0] == [1] goto [2]",
    "00100010": "if [0] >= [1] goto [2]",
    "00100011": "if [0] <= [1] goto [2]",
    "00100110": "if [0] > [1] goto [2]",
    "00100111": "if [0] < [1] goto [2]",
    "00100101": "if [0] != [1] goto [2]",
    "00001111": "run from memory [1] with args memory[2:]",
    "00001010": "load from persistent byte persistent[1] to memory[2]",
    "00010101": "write to persistent memory memory[1] -> persistent[memory[2]]",
    "01000000": "goto line [1] and run from there",
}


def prompt_filename(stdscr, prompt):
    curses.echo()
    stdscr.addstr(curses.LINES - 2, 0, prompt)
    stdscr.clrtoeol()
    filename = stdscr.getstr(curses.LINES - 2, len(prompt)).decode('utf-8')
    curses.noecho()
    return filename.strip()


def find_opcode_start(line, cursor_x):
    bit_positions = [i for i, c in enumerate(line) if c in '01']
    if not bit_positions:
        return None

    for i, pos in enumerate(bit_positions):
        if pos >= cursor_x:
            bit_index = i
            break
    else:
        bit_index = len(bit_positions) - 1

    start_bit = (bit_index // 8) * 8
    if start_bit + 1 > len(bit_positions):
        return None
    return bit_positions[start_bit]


def get_bits_from(line, start, count=8):
    bits = []
    i = start
    while i < len(line) and len(bits) < count:
        if line[i] in '01':
            bits.append(line[i])
        i += 1
    return ''.join(bits)


def is_backspace(key):
    return key in ('\b', '\x7f', '\x08') or key == curses.KEY_BACKSPACE


def main(stdscr, filename=None):
    curses.curs_set(1)
    stdscr.clear()
    text = ['']
    y, x = 0, 0

    def save_file(fname):
        with open(fname, 'w') as f:
            f.write('\n'.join(text))

    def load_file(fname):
        nonlocal text
        try:
            with open(fname, 'r') as f:
                lines = f.read().splitlines()
                text = lines if lines else ['']
        except:
            text = ['']

    if filename:
        load_file(filename)

    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        right_width = 40
        text_width = width - right_width - 1

        status = f"File: {filename or 'Untitled'} - [s] Save  [l] Load  [q] Quit"
        stdscr.addstr(height - 1, 0, status[:width - 1], curses.A_REVERSE)

        # Draw text with opcode highlighting
        for idx, line in enumerate(text[:height - 2]):
            start_idx = end_idx = None
            if idx == y:
                start_idx = find_opcode_start(line, x)
                if start_idx is not None:
                    end_idx = start_idx + 8 + line[start_idx:start_idx+8].count(' ')

            for i, c in enumerate(line[:text_width]):
                attr = curses.A_NORMAL
                if start_idx is not None and start_idx <= i < start_idx + 16:
                    if c in '01':
                        attr = curses.A_REVERSE
                stdscr.addch(idx, i, c, attr)

        # Opcode panel
        stdscr.addstr(0, text_width + 1, "Current Opcode:", curses.A_UNDERLINE)
        current_line = text[y] if y < len(text) else ""
        opcode_start = find_opcode_start(current_line, x)
        if opcode_start is not None:
            bits = get_bits_from(current_line, opcode_start, 8)
            if bits:
                if len(bits) == 8 and bits in OPCODES:
                    stdscr.addstr(1, text_width + 1, f"{bits}: {OPCODES[bits]}", curses.A_BOLD)
                else:
                    stdscr.addstr(1, text_width + 1, f"{bits}: (partial)", curses.A_DIM)

                stdscr.addstr(3, text_width + 1, "Next possible opcodes:", curses.A_UNDERLINE)
                matches = [f"{k}: {v}" for k, v in OPCODES.items() if k.startswith(bits) and k != bits]
                if matches:
                    for i, match in enumerate(matches[:height - 6]):
                        stdscr.addstr(4 + i, text_width + 1, match[:right_width])
                else:
                    stdscr.addstr(4, text_width + 1, "No matching opcodes.", curses.A_DIM)
            else:
                stdscr.addstr(1, text_width + 1, "No bits at cursor", curses.A_DIM)
        else:
            stdscr.addstr(1, text_width + 1, "Move to opcode bits.", curses.A_DIM)

        stdscr.move(y, x)
        stdscr.refresh()

        key = stdscr.get_wch()

        # ==== Key Handling ====
        if isinstance(key, str):
            if key.lower() == 'q':
                break
            elif key.lower() == 's':
                if not filename:
                    filename = prompt_filename(stdscr, "Save as: ")
                if filename:
                    save_file(filename)
            elif key.lower() == 'l':
                filename = prompt_filename(stdscr, "Load file: ")
                if filename:
                    load_file(filename)
                    y, x = 0, 0
            elif is_backspace(key):
                if x > 0:
                    text[y] = text[y][:x - 1] + text[y][x:]
                    x -= 1
                elif y > 0:
                    prev_len = len(text[y - 1])
                    text[y - 1] += text[y]
                    del text[y]
                    y -= 1
                    x = prev_len
            elif key == '\n':
                line = text[y]
                text[y] = line[:x]
                text.insert(y + 1, line[x:])
                y += 1
                x = 0
            elif key == ' ':
                text[y] = text[y][:x] + ' ' + text[y][x:]
                x += 1
            elif key.lower() in LEFT_KEYS:
                text[y] = text[y][:x] + '0' + text[y][x:]
                x += 1
            elif key.lower() in RIGHT_KEYS:
                text[y] = text[y][:x] + '1' + text[y][x:]
                x += 1
            elif key in ['0', '1']:
                text[y] = text[y][:x] + key + text[y][x:]
                x += 1

        elif key == curses.KEY_BACKSPACE:
            if x > 0:
                text[y] = text[y][:x - 1] + text[y][x:]
                x -= 1
            elif y > 0:
                prev_len = len(text[y - 1])
                text[y - 1] += text[y]
                del text[y]
                y -= 1
                x = prev_len
        elif key == curses.KEY_LEFT:
            if x > 0:
                x -= 1
            elif y > 0:
                y -= 1
                x = len(text[y])
        elif key == curses.KEY_RIGHT:
            if x < len(text[y]):
                x += 1
            elif y + 1 < len(text):
                y += 1
                x = 0
        elif key == curses.KEY_UP:
            if y > 0:
                y -= 1
                x = min(x, len(text[y]))
        elif key == curses.KEY_DOWN:
            if y + 1 < len(text):
                y += 1
                x = min(x, len(text[y]))


if __name__ == '__main__':
    filename = sys.argv[1] if len(sys.argv) > 1 else None
    curses.wrapper(main, filename)
