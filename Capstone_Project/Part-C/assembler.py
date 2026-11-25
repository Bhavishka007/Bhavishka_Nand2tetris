import os

# ============================================================
# HACK ASSEMBLER
# Student Roll Number: 2501730356
# K = 56
# K mod 3 = 2
# Personalized Feature: Assembly Statistics Report
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

INPUT_DIR = os.path.join(BASE_DIR, "input")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

FILES = ["Add.asm", "Max.asm", "Rect.asm", "Pong.asm", "Box.asm"]



def create_symbol_table():

    symbols = {
        "SP": 0,
        "LCL": 1,
        "ARG": 2,
        "THIS": 3,
        "THAT": 4,
        "SCREEN": 16384,
        "KBD": 24576
    }

    # Add R0 to R15
    for i in range(16):
        symbols["R" + str(i)] = i

    return symbols



COMP = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "M": "1110000",

    "!D": "0001101",
    "!A": "0110001",
    "!M": "1110001",

    "-D": "0001111",
    "-A": "0110011",
    "-M": "1110011",

    "D+1": "0011111",
    "A+1": "0110111",
    "M+1": "1110111",

    "D-1": "0001110",
    "A-1": "0110010",
    "M-1": "1110010",

    "D+A": "0000010",
    "D+M": "1000010",

    "D-A": "0010011",
    "D-M": "1010011",

    "A-D": "0000111",
    "M-D": "1000111",

    "D&A": "0000000",
    "D&M": "1000000",

    "D|A": "0010101",
    "D|M": "1010101"
}


DEST = {
    "": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}


JUMP = {
    "": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}



def clean_lines(source_lines):

    cleaned = []

    for line_number, line in enumerate(source_lines, start=1):

        # Remove comments
        line = line.split("//")[0]

        # Remove whitespace
        line = line.strip()
        line = line.replace(" ", "")
        line = line.replace("\t", "")

        # Ignore empty lines
        if line:
            cleaned.append((line, line_number))

    return cleaned



def first_pass(cleaned, symbols):

    instruction_address = 0
    label_count = 0

    for line, original_line_number in cleaned:

        # Label declaration
        if line.startswith("(") and line.endswith(")"):

            label = line[1:-1]

            if not label:
                raise ValueError(
                    f"Line {original_line_number}: Empty label."
                )

            if label in symbols:
                raise ValueError(
                    f"Line {original_line_number}: "
                    f"Duplicate or predefined symbol '{label}'."
                )

            symbols[label] = instruction_address
            label_count += 1

        else:

            # A or C instruction
            instruction_address += 1

    return label_count, instruction_address



def convert_a_instruction(line, symbols, next_variable_address):

    value = line[1:]

    # Numeric address
    if value.isdigit():

        address = int(value)

    else:

        # Symbol
        if value not in symbols:

            symbols[value] = next_variable_address
            next_variable_address += 1

        address = symbols[value]

    if address < 0 or address > 32767:

        raise ValueError(
            f"Invalid A-instruction address: @{value}"
        )

    binary = format(address, "016b")

    return binary, next_variable_address



def convert_c_instruction(line):

    dest = ""
    comp = ""
    jump = ""

    # Split destination and computation
    if "=" in line:

        parts = line.split("=")

        if len(parts) != 2:
            raise ValueError(f"Invalid C-instruction: {line}")

        dest = parts[0]
        remaining = parts[1]

    else:

        remaining = line

    # Split computation and jump
    if ";" in remaining:

        parts = remaining.split(";")

        if len(parts) != 2:
            raise ValueError(f"Invalid C-instruction: {line}")

        comp = parts[0]
        jump = parts[1]

    else:

        comp = remaining

    # Validate
    if comp not in COMP:

        raise ValueError(f"Invalid computation: {comp}")

    if dest not in DEST:

        raise ValueError(f"Invalid destination: {dest}")

    if jump not in JUMP:

        raise ValueError(f"Invalid jump: {jump}")

    # Generate binary instruction
    return "111" + COMP[comp] + DEST[dest] + JUMP[jump]

def second_pass(cleaned, symbols):

    machine_code = []

    a_count = 0
    c_count = 0
    variable_count = 0

    next_variable_address = 16

    for line, original_line_number in cleaned:

        # Ignore labels
        if line.startswith("(") and line.endswith(")"):

            continue

        try:

            # A-instruction
            if line.startswith("@"):

                binary, next_variable_address = (
                    convert_a_instruction(
                        line,
                        symbols,
                        next_variable_address
                    )
                )

                a_count += 1

                # Count allocated variables
                if not line[1:].isdigit():

                    if symbols[line[1:]] >= 16:

                        variable_count += 1

                machine_code.append(binary)

            # C-instruction
            else:

                binary = convert_c_instruction(line)

                c_count += 1

                machine_code.append(binary)

        except ValueError as error:

            raise ValueError(
                f"Error at source line {original_line_number}: {error}"
            )

    return machine_code, a_count, c_count, variable_count


# ============================================================
# 8. PERSONALIZED FEATURE - STATISTICS REPORT
# K = 56
# K mod 3 = 2
# ============================================================

def generate_statistics_report(
    filename,
    total_source_lines,
    instruction_count,
    a_count,
    c_count,
    label_count,
    variable_count,
    machine_code_count
):

    report_name = filename.replace(".asm", "_Statistics.txt")

    report_path = os.path.join(OUTPUT_DIR, report_name)

    with open(report_path, "w") as report:

        report.write("========================================\n")
        report.write("       HACK ASSEMBLER STATISTICS\n")
        report.write("========================================\n\n")

        report.write("Student Roll Number: 2501730356\n")
        report.write("Personalized K Value: 56\n")
        report.write("K mod 3: 2\n")
        report.write("Feature: Assembly Statistics Reporting\n\n")

        report.write(f"Source File: {filename}\n")
        report.write(
            f"Total Source Lines: {total_source_lines}\n"
        )
        report.write(
            f"Actual Instructions: {instruction_count}\n"
        )
        report.write(
            f"A-Instructions: {a_count}\n"
        )
        report.write(
            f"C-Instructions: {c_count}\n"
        )
        report.write(
            f"Labels: {label_count}\n"
        )
        report.write(
            f"Variables Allocated: {variable_count}\n"
        )
        report.write(
            f"Machine Code Instructions: {machine_code_count}\n"
        )

        report.write("\n========================================\n")
        report.write("         ASSEMBLY COMPLETED\n")
        report.write("========================================\n")

    print(f"Statistics report generated: {report_name}")

def assemble_file(filename):

    input_path = os.path.join(INPUT_DIR, filename)

    output_filename = filename.replace(".asm", ".hack")

    output_path = os.path.join(OUTPUT_DIR, output_filename)

    # Read source code
    with open(input_path, "r") as file:

        source_lines = file.readlines()

    total_source_lines = len(source_lines)

    # Clean source code
    cleaned = clean_lines(source_lines)

    # Create symbol table
    symbols = create_symbol_table()

    # First pass
    label_count, instruction_count = first_pass(
        cleaned,
        symbols
    )

    # Second pass
    machine_code, a_count, c_count, variable_count = (
        second_pass(cleaned, symbols)
    )

    # Write .hack file
    with open(output_path, "w") as file:

        for instruction in machine_code:

            file.write(instruction + "\n")

    # Generate personalized report
    generate_statistics_report(
        filename,
        total_source_lines,
        instruction_count,
        a_count,
        c_count,
        label_count,
        variable_count,
        len(machine_code)
    )

    print(f"\nSuccessfully assembled: {filename}")
    print(f"Output file: {output_filename}")
    print(f"Total instructions: {len(machine_code)}")

def main():

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("========================================")
    print("       PYTHON HACK ASSEMBLER")
    print("       Roll No: 2501730356")
    print("       K = 56")
    print("========================================")

    for filename in FILES:

        input_path = os.path.join(INPUT_DIR, filename)

        if not os.path.exists(input_path):

            print(f"\nFile not found: {filename}")
            continue

        try:

            assemble_file(filename)

        except Exception as error:

            print(f"\nFailed to assemble {filename}")
            print(error)

    print("\nAll files processed.")

if __name__ == "__main__":

    main()