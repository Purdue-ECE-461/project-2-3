import os
import logging
"""
rampup

Args:
    file: Filepath of temp folder

Returns:
    nothing yet

Raises:
    KeyError: Raises an exception.
"""
def rampup(filepath):

    commentTotal = 0
    lineTotal = 0
    commentScore = 0
    readmeScore = 0

    try:
        # We want to iterate over modules independently, not modules in node_modules
        filepath = filepath + ''
    except Exception as e:
        logging.warning("RampUp: Could not open ""src"" in repository: {}".format(e))
        return
    for subdir, dirs, files in os.walk(filepath):
        dirs[:] = [d for d in dirs if not d.startswith('node_modules')] # remove node modules
        for filename in files:
            if filename.endswith(('.js')):
                file = subdir + '/' + filename
                commentTuple = calcComments(file)
                commentTotal += commentTuple[2]
                lineTotal += commentTuple[3]
                # print("Read file {} in {}, with {} line comments and {} block comments".format(filename, subdir, commentTuple[0], len(commentTuple[1])))
    logging.info("Repo parsed, found {} total comments.".format(commentTotal))
    if (lineTotal == 0):
        commentRatio = 0
    else:
        commentRatio = commentTotal / lineTotal
    logging.info("{}""%"" of all lines were comments".format(round(commentRatio * 100, 2)))
    # If over 20% of lines have comments, then give them full marks on comment score, otherwise give them the comment score from the ratio scaled from 0 to 0.2.
    if commentRatio >= 0.2:
        commentScore = 1
    else:
        commentScore = commentRatio / 0.2

    readmeScore = calcReadme(filepath)

    return round(0.7 * readmeScore + 0.3 * commentScore, 4)

"""
calcComments

Args:
    file: Filepath of a source code file

Returns:
    Tuple with line comments, block comments (list with block comment sizes), and total comments

Raises:
    KeyError: Raises an exception.
"""
def calcComments(file):

    lineComments = 0
    blockComments = [] # [blockComment1 lines, blockComment2 lines, etc.]
    totalComments = 0
    totalLines = 0
    isBlockComment = False
    comment = 0

    fp = open(file, "r")
    try:
        lines = fp.readlines()
        for line in lines:
            if isBlockComment is True:
                if line.lstrip().startswith('*/'):
                    blockComments.append(comment)
                    comment = 0
                    isBlockComment = False
                else:
                    comment += 1
                    if '*/' in line:
                        blockComments.append(comment)
                        comment = 0
                        isBlockComment = False
            elif '//' in line:
                lineComments += 1
            elif '/*' in line:
                if '*/' in line:
                    blockComments.append(1)
                else:
                    isBlockComment = True
            totalLines += 1
        totalComments = lineComments
        for comment in blockComments:
            totalComments += comment
    finally:
        fp.close()
    return (lineComments, blockComments, totalComments, totalLines)

"""
calcReadme - 60% for length, 40% for formatting / features

Args:
    file: Filepath of a source code file

Returns:
    Tuple with line comments, block comments (list with block comment sizes), and total comments

Raises:
    KeyError: Raises an exception.
"""
def calcReadme(filepath):

    lengthscore = 0
    formatscore = 0
    readme = None
    logging.info("Looking for README")
    if(os.path.exists(filepath + "/readme.md")):
        readme = filepath + "/readme.md"
    elif(os.path.exists(filepath + "/README.md")):
        readme = filepath + "/README.md"
    else:
        logging.warning("No readme.md or README.md file found, scoring 0")
        return 0
    logging.info("README found")
    fp = open(readme)
    lines = fp.readlines()
    length = len(lines)

    # If number of lines is greater than 80, then give them a 100
    if length >= 80:
        lengthscore = 1
    else:
        lengthscore = length / 80
    logging.info("Readme length is %d lines", length)
    # We want readmes to take advantage of the markdown formatting features. We want all to have three headings 
    # and one image minimum, and use at least six other markdown formatting features (list, code segment, bold)
    headingcnt = 0
    imagecnt = 0
    othercnt = 0

    for line in lines:
        line = line.lstrip()
        if (len(line) > 0):
            firstchar = line[0]
            # Header
            if (firstchar == '#'):
                headingcnt += 1
            # Image
            elif (".jpg" in line or ".png" in line):
                imagecnt += 1
            # list
            elif (firstchar == '-' or firstchar == '+'):
                othercnt += 1
            # numbered list
            if (firstchar.isdigit()):
                for char in line:
                    if char.isdigit():
                        pass
                    elif char == '.':
                        othercnt += 1
                        break
                    else:
                        break
            # italic / bold
            elif (firstchar == '*'):
                othercnt += 1
            # blockquote
            elif (firstchar == '>'):
                othercnt += 1
            # code block
            elif (line.startswith('```')):
                othercnt += 1
    fp.close()
    logging.info("Found %d headers, %d images, and %d other markdown features in the readme.", headingcnt, imagecnt, othercnt)
    # calculations
    if othercnt > 6:
        othercnt = 6
    if imagecnt > 1:
        imagecnt = 1
    if headingcnt > 3:
        headingcnt = 3
    formatscore = (headingcnt + imagecnt + othercnt) / 10
    return round(formatscore * 0.4 + lengthscore * 0.6, 4)