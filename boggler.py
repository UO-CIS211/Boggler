"""
Boggle solver.
    Usage:  python3 boggler.py  "board" dict.txt
    where "board" is 16 characters of board, in left-to-right reading order
    and dict.txt can be any file containing a list of words in alphabetical order
    
    Author: Michal Young, michal@cs.uoregon.edu  2012.10.26
    
"""

from boggle_board import BoggleBoard   
import argparse  
import game_dict  # Dictionary of legal game words
import time

global results

def main():
    """
    Main program: 
    Find all words of length 3 or greater on a boggle 
    board. 
    Args:
        none (but expect two arguments on command line)
    Returns: 
        Nothing (but prints found words in alphabetical
        order, without duplicates, one word per line)
    """
    start_time=time.time()
    parser = argparse.ArgumentParser(description="Find boggle words")
    parser.add_argument('board', type=str,
                        help="A 16 character string to represent 4 rows of 4 letters. Q represents QU.")
    parser.add_argument('dict', type=argparse.FileType('r'),
                        help="A text file containing dictionary words, one word per line.")
    args = parser.parse_args()  # will get arguments from command line and validate them
    boardtext = args.board
    game_dict.read( args.dict )
    board = BoggleBoard(boardtext)
    global results
    results = [ ] ## find_words will fill this list
    for row in range(4):
        for col in range(4):
            find_words(board, row, col, "")
    results = dedup(results)
    total = 0
    for word in results:
        word_score = score(word)
        total += word_score
        print(word, word_score)
    print("Total score: ", total)
    print("Runtime: {}" .format(time.time() - start_time))

        
def find_words(board, row, col, prefix):
    """Find all words starting with prefix that
    can be completed from row,col of board.
    Args:
        row:  row of position to continue from (need not be on board)
        col:  col of position to continue from (need not be on board)
    prefix: looking for words that start with this prefix
    Returns: nothing
        (side effect is filling results list)
    """
    if not board.available(row, col):
        return
    prefix = prefix + board.get_char(row,col)
    match = game_dict.search(prefix)
    if match == game_dict.NO_MATCH:
        return
    if match == game_dict.WORD :
        results.append(prefix)
    board.mark_taken(row, col)
    find_words(board, row-1, col, prefix)
    find_words(board, row+1, col, prefix)
    find_words(board, row, col+1, prefix)
    find_words(board, row, col-1, prefix)
    find_words(board, row-1,col-1,prefix)
    find_words(board, row-1,col+1,prefix)
    find_words(board, row+1,col-1,prefix)
    find_words(board, row+1,col+1,prefix)
    board.unmark_taken(row, col)
    return
    
def dedup(list) :
    """
    Return a copy of list, less duplicate items.
    Args:
       list:  A list of elements that can be compared and sorted
    Returns:
       A copy of the list, omitting duplicates 
    """
    result = [ ]
    prev = None
    for el in sorted(list):
        if el != prev :
            result.append(el)
            prev = el
    return result
    
    
def score(word):
    """
    Compute the Boggle score for a word, based on the scoring table
    at http://en.wikipedia.org/wiki/Boggle. 
    Args: 
       word:  A string of at least three letters.
    Returns: 
       An integer between 1 and 11, inclusive.
    """
    if len(word) <= 4:
        return 1
    if len(word) == 5: 
        return 2
    if len(word) == 6:
        return 3
    if len(word) == 7:
        return 5
    # 8 or longer
    return 11


####
# Run if invoked from command line
####

if __name__ == "__main__":
    main()
    input("Press enter to end")

