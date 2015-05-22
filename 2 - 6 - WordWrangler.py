"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided
import math

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    newlist = []
    
    for number in range(len(list1)):
        if number == 0:
            newlist.append(list1[number])
            marker = list1[number]
        elif list1[number] != marker:
            newlist.append(list1[number])
            marker = list1[number]

            
    print newlist
    return newlist

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    
    if len(list1) > len(list2):
        longerlist = list1
        shorterlist = list2
    else:
        longerlist = list2
        shorterlist = list1
        
    wordlist = []
    
    for element in longerlist:
        for secondelement in shorterlist:
            if element == secondelement:
                wordlist.append(element)
                break
                  
    return wordlist

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """

    newlist = []
    marker1 = 0
    marker2 = 0
    timer = len(list2) + len(list1)
    
    for number in range(timer):
        print number
        if marker1 == len(list1) and marker2 == len(list2):
            return newlist
        elif marker1 == len(list1):
            newlist.append(list2[marker2])
            marker2 += 1
        elif marker2 == len(list2):
            newlist.append(list1[marker1])
            marker1 += 1
        elif list1[marker1] == list2[marker2]:
            newlist.append(list1[marker1])
            newlist.append(list2[marker2])
            marker1 += 1
            marker2 += 1
        elif list1[marker1] > list2[marker2]:
            newlist.append(list2[marker2])
            marker2 += 1
        elif list1[marker1] < list2[marker2]:
            newlist.append(list1[marker1])
            marker1 += 1
            
            
    
    return newlist
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    if len(list1) < 2:
        return list1
    middle = len(list1) / 2
    left = merge_sort(list1[:middle])
    right = merge_sort(list1[middle:])
    return merge(left, right)

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if len(word) < 1:
        return [word]
    else:
        first = word[0]
        rest = word[1:]
        rest_string = gen_all_strings(rest)
    
    
    temp_list = []
    for string in rest_string:
            for letter in range(len(string) + 1):               
                new_word = string[:letter] + first + string[letter:]
                temp_list.append(new_word)
    return rest_string + temp_list

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)
    data = netfile.read()
    return data

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
#run()

    
#listeryo = ('hello', 'hi', 'hi', 'yo')
#listerhi = ('hello', 'hi', 'hullo', 'yello', 'yellow')
#merge(listeryo, listerhi)

#list3 = ('yo', 'hello', 'hi', 'yello', 'hullo')
#print merge_sort(list3)
#print gen_all_strings("abb")