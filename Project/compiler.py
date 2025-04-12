from scanner import Scanner

def main():
    scanner = Scanner("input.txt")
    scanner.tokenize()
    scanner.write_outputs()

if __name__ == "__main__":
    main()
