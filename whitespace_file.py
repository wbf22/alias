import sys

def create_spaces_file(filename):
    line = ' ' * 1000  # 1000 spaces
    with open(filename, 'w') as f:
        for i in range(1, 1001):
            f.write(line + '\n')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <output_filename>")
        sys.exit(1)
    filename = sys.argv[1]
    create_spaces_file(filename)
    print(f"File '{filename}' created with 1000 lines of 1000 spaces each.")
