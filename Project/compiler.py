from scanner import Scanner

def main():
    scanner = Scanner("input.txt") # create scanner object
    scanner.tokenize() # tokenize the input file
    scanner.write_outputs() # write tokens, errors and symbol table to files 
    
    # next add parser and other for phase 2 and 3 😊😊🤪🤪🤪😂😂

if __name__ == "__main__":
    main()
