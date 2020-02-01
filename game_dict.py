"""
game_dict: Game dictionary.
Differs from a spelling dictionary in that looking up a string
has three possible outcomes:  The string matches a word exactly,
or it does not match exactly but is a prefix of a word, or there is
no word starting with that string.

Authors:  #FIXME
Consulted in design: #FIXME
"""

dict = [ ]  

# Codes for result of search
WORD = 1
PREFIX = 2
NO_MATCH = 0

def read( file, min_length=3 ):
    """Read the dictionary from a sorted list of words.
    Args:
        filename: path to dictionary file, as a string
        min_length: integer, minimum length of words to
            include in dictionary. Useful for games in
            which short words don't count.  For example,
            in Boggle the limit is usually 3, but in
            some variations of Boggle only words of 4 or
            more letters count.
    Returns:  nothing
    """
    global dict
    dict = [ ]
    for word in file :
        word = word.strip()
        if len(word) >= min_length and word.isalpha():
            dict.append(word)
    dict = sorted(dict)
            
def search( str ):
    """Search for a prefix string in the dictionary.
    Args:
        str:  A string to look for in the dictionary
    Returns:
        code WORD if str exactly matches a word in the dictionary,
            PREFIX if str does not match a word exactly but is a prefix
                of a word in the dictionary, or
        NO_MATCH if str is not a prefix of any word in the dictionary
    """
    # Binary search.  Note that an unsuccessful binary search should
    # end with "left" on a word with a matching prefix,
    # if there is any.
    left = 0
    right = len(dict) - 1
    while left <= right :
        mid = (left + right) // 2
        # print("DBG - probing ", mid, dict[mid])
        if dict[mid] > str :
            right = mid - 1
        elif dict[mid] < str :
            left = mid + 1
        else :
            return WORD

    # No match ... but could it be a prefix?
    if left < len(dict) and  dict[left].startswith(str):
        return PREFIX
    return NO_MATCH
    
    
######################################################
#  Test driver
#    for testing game_dict.py by itself,
#    separate from boggler.py
#   Note we will need shortdict.txt for testing
#
#######################################################


if __name__ == "__main__":
    # This code executes only if we execute game_dict.py by itself,
    # not if we import it into boggler.py
    from test_harness import testEQ
    read(open("shortdict.txt"))
    # shortdict contains "alpha", "beta","delta", "gamma", "omega"
    testEQ("First word in dictionar (alpha)", search("alpha"), WORD)
    testEQ("Last word in dictionary (omega)", search("omega"), WORD)
    testEQ("Within dictionary (beta)", search("beta"), WORD)
    testEQ("Within dictionary (delta)", search("delta"), WORD)
    testEQ("Within dictionary (gamma)", search("gamma"), WORD)
    testEQ("Prefix of first word (al)", search("al"), PREFIX)
    testEQ("Prefix of last word (om)", search("om"), PREFIX)
    testEQ("Prefix of interior word (bet)", search("bet"),PREFIX)
    testEQ("Prefix of interior word (gam)", search("gam"),PREFIX)
    testEQ("Prefix of interior word (del)", search("del"),PREFIX)
    testEQ("Before any word (aardvark)", search("aardvark"), NO_MATCH)
    testEQ("After all words (zephyr)", search("zephyr"), NO_MATCH)
    testEQ("Interior non-word (axe)", search("axe"), NO_MATCH)
    testEQ("Interior non-word (carrot)", search("carrot"), NO_MATCH)
    testEQ("Interior non-word (hagiography)",
        search("hagiography"), NO_MATCH)
    # Try again with only words of length at least 5
    # Now beta should be absent
    read(open("shortdict.txt"), min_length=5)
    print("New dictionary: ", dict)
    testEQ("First word in dictionary (alpha)", search("alpha"), WORD)
    testEQ("Last word in dictionary (omega)", search("omega"), WORD)
    testEQ("Short word omitted (beta)", search("beta"), NO_MATCH)
    read(open("dict.txt"))  # Long dictioanry
    testEQ("Can I find farm in long dictonary?", search("farm"), WORD)
    testEQ("Can I find bead in long dictionary?", search("bead"), WORD)
    
    
