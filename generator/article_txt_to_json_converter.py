import sys
import json

def next_nonempty_line(lines, current_line_number):
    """
    list lines : the list of lines of the article
    int current_line_number : the current line number (starting from 0)
    """
    current_line_number += 1
    while current_line_number < len(lines) and ( lines[current_line_number] == '\n' or lines[current_line_number].startswith('//') ):
        current_line_number += 1
    return current_line_number

def extractImageInfos(line):
    i = line.find(' ') # find the first space, where the source begins
    j = line.find(' ', i+1) # find the second space, where the description begins
    if j != -1: # if there is a text description
        return { 'class'    : 'image',
                 'source'   : line[i+1:j],
                 'content'  : line[j+1:-1]}
    else: # if there is no text description, the content is empty
        return { 'class'    : 'image',
                 'source'   : line[i+1:-1],
                 'content'  : ''}

def main():
    if len(sys.argv) != 2: # if the user didn't provide a filename
        print("Error: Invalid number of arguments")
        print('Usage: python3 article_txt_to_json_converter.py <filename>')
        print("Example: python3 article_txt_to_json_converter.py article.txt")
        return

    json_list = []
    article_txt_file_name = sys.argv[1]
    with open(article_txt_file_name, 'r', encoding='utf8') as f:
        article_lines = f.readlines() # read the lines of the file
        number_of_lines = len(article_lines) # get the number of lines
        current_line_number = next_nonempty_line(article_lines, -1) # skip the first empty lines and initialize the current line number

        dict = { 'class'    : 'article-title',
                 'content'  : article_lines[current_line_number][:-1]}
        json_list.append(dict)

        current_line_number = next_nonempty_line(article_lines, 0) # go the date line
        dict = { 'class'    : 'date',
                 'content'  : article_lines[current_line_number][:-1]}
        json_list.append(dict)

        current_line_number = next_nonempty_line(article_lines, current_line_number) # go the first relevant line
        while not article_lines[current_line_number].startswith('#end'): # while the current line is not the end of the article
            if article_lines[current_line_number].startswith('#title '): # if the current line is a title
                dict = { 'class'    : 'title',
                         'content'  : article_lines[current_line_number][7:-1]}
            elif article_lines[current_line_number].startswith('#subtitle '): # if the current line is a subtitle
                dict = { 'class'    : 'subtitle',
                         'content'  : article_lines[current_line_number][10:-1]}
            elif article_lines[current_line_number].startswith('#image '): # if the current line is an image
                dict = extractImageInfos(article_lines[current_line_number])
            else: # if the current line is a paragraph
                dict = { 'class'    : 'text',
                         'content'  : article_lines[current_line_number][:-1]}
            
            json_list.append(dict)
            current_line_number = next_nonempty_line(article_lines, current_line_number)

        json_file_name = article_txt_file_name[:-4] + '.json'
        with open(json_file_name, 'w') as f:
            json.dump(json_list, f)
        
        print('Conversion completed successfully! File saved as ' + json_file_name)
    return


if __name__ == '__main__':
    main()