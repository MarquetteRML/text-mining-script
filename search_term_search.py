# search_term_search.py

# Ad Maiorem Dei Gloriam

import re
import sys

# Open the article that keywords will be checked against
with open(sys.argv[1]) as f:
    SearchText = list(f)

# Open the search terms list (search_terms.txt) and search for the terms using re.search function in the article. Display the number of search terms that appear in the article. This is intended to make it easier for the researchers to glance at the report and see what terms were found without having to look at the whole result list. This could probably be incorporated into the search feature below it.

with open('search_terms.txt') as f:
    print ("Search words appearing in this article: \n")
    for line_no, line in enumerate(f):
        word_count = 0
        NeedleSearchTerm1 = line.strip()
        my_regex = r"\b(?=\w)" + re.escape(NeedleSearchTerm1) + r"\b(?!\w)"
        for haystack in SearchText:
            if re.search(my_regex, haystack, re.IGNORECASE) is not None:
            	if word_count == 0:
            		print ( NeedleSearchTerm1 + "\n")
		word_count += 1


# Open the search terms list (search_terms.txt) and search for the terms using re.search function in the article. Display the search term from the list found in the article and show a snippet from the line the term/phrase was found in as well as the line number of the file so the researchers can more easily find the line in the article for further analysis. The re.search feature appears to work well finding words and phrases, but I discovered that it does not appear to find phrases that include parentheses, is this something that can be added to the regex? 
		
with open('search_terms.txt') as f:
    for line in f:
        word_count = 0
        NeedleSearchTerm2 = line.strip()
        my_regex = r"\b(?=\w)" + re.escape(NeedleSearchTerm2) + r"\b(?!\w)"
        for line_no, haystack in enumerate(SearchText):
        	matchedit = re.search(my_regex, haystack, re.IGNORECASE)
            	if matchedit is not None:
            		if word_count == 0:
            			print ("\n\n==========================================\nSearch Word:\n" + NeedleSearchTerm2 + "\n")
            		else:
                		print ("\n*=*=*\n")                
                	for match in re.finditer(my_regex, haystack, re.IGNORECASE):

                    # Find the start index of the keyword
                    		start = match.span()[0]

                    # Find the end index of the keyword
                    		end = match.span()[1]

                    # Truncate line to get only 'n' characters before and after the keyword
                    		tmp = haystack[start-150:end+150] + '\n'            
                    		print (line_no, ':', tmp)
                	

			word_count += 1