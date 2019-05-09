# Text Mining Script

[![Digital Scholarship Lab Logo](https://www.marquette.edu/library/digital-scholarship/images/DSLab2.png)](https://www.marquette.edu/library/digital-scholarship/)

## Project Description

The Python code in the repository and work flow described below was used to text mine over 7,500 full-text journal articles published in American Counseling Association journals from 2000-2016 for 500+ keywords, allowing a research team to conduct a content analysis for an upcoming publication.  

The code searched each file against the keyword list and generated a report listing each keyword found along with the 150 characters before and after each found keyword.

No one on the team is a classically trained computer scientist or computer engineer and the member of the team who wrote the code for the project initially thought Python was a type of snake, not a coding language.

The code in this repository was generated through trial and error testing and lots of reading of discussion posts on Stack Overflow and review of free online Python courses. 

We invite and encourage others to help improve and expand on this code.

## Technology Used

* Mac OS (this can be done on a PC, but requires installing Python)
* Python (comes out of the box with Mac OS)
* Terminal (Mac OS) or Windows Terminal (Windows)
* Advanced Text Editor (such as [BBEdit](https://www.barebones.com/products/bbedit/))

## Gather Articles

Using the [CrossRef API](https://github.com/CrossRef/rest-api-doc) and downloads from the library's database aggregators, PDF versions of the journal articles from the date range were aquired. 

## Search Articles for Search Terms

### STEP 1: Convert PDF to XML

Place the PDFs you want to convert to XML, using [pdfx and online PDF to XML conversion tool](http://pdfx.cs.man.ac.uk/), into a folder. Next, run the code below in Terminal. The code will produce a series of XML files with the same name as the original PDF file name.

**Please note that service abuse of pdfx, in number of submissions or frequency of requests, will result in automatic blacklisting.** 

```sh
find . -name "*.pdf" | while read file;
do
curl --data-binary @"$file" -H "Content-Type: application/pdf" -L "http://pdfx.cs.man.ac.uk" > "${file}x.xml";
done
```

### STEP 2: Convert XML File Content to Lower Case

To ensure more accurate matching of the keywords, the code below was run in Terminal to lower case all of the text in the files converted in Step 1. Note that the word LOWER is preappeneded to the file name to make it easier to identify the file. 

```sh
for file in *.xml; do dd if="$file" of=LOWER-"$file" conv=lcase; done
```

### STEP 3: Remove Reference Section from Files

Use an advanced text editor such as BBEdit to do a multi-file find and replace in the XML files. 

The research team did not want to analyze references, the code below will remove the References section from the articles. 

```sh
<ref-list class="DoCO:BiblioGraphicReferenceList">[\s\S]*?</ref-list>
```
Some of the keywords include the word "class", the code below removes the word "class" in the XML code, **NOT** the article text. This dramatically reduced the false postive returns for the word "class" when searching the articles against the search term list. 

```sh
class=
```

### STEP 4: Remove the LOWER from the Filename

```sh
for filename in *; do 
    [ -f "$filename" ] || continue
    mv "$filename" "${filename//LOWER-/}"
done
```

### STEP 5: Get List of Filenames From the Directory

The code below, run in Terminal, will generate a .txt file with a listing of all the filenames in the directory you run the code in.

```sh
ls > filenames.txt
```

### STEP 6: Search Articles Against Keywords

The code below will loop through the article files and search them against the  keywords list. The code will generate a file called REPORT-FILENAME.xml in the same directory.

**IMPORTANT: Make sure the Python file [search_term_search.py](https://github.com/MarquetteRML/text-mining-script/blob/master/search_term_search.py) AND the text file with the search terms are in the same directory before running this code.**

```sh
while read -r ARTICLE || [[ -n "$ARTICLE" ]]; do python search_term_search.py $ARTICLE > REPORT-$ARTICLE; done < filenames.txt
```

### STEP 7: Convert XML Report Files to Text Files

The process in STEP 6 generates a report file for each article that is in .txt format. The code below, run from terminal, converts the .xml file to a .txt file which was the format requested by the research team. 

```sh
for file in *.xml; do mv "$file" "${file%.xml}.txt"; done
```
