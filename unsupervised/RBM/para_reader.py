
import readline


class Paragraphs:

    def __init__(self, fileobj, separator='\n'):

        # Ensure that we get a line-reading sequence in the best way possible:
        #import xreadlines
        try:
            # Check if the file-like object has an xreadlines method
            self.seq = fileobj.readlines()
        except AttributeError:
            # No, so fall back to the xreadlines module's implementation
            self.seq = xreadlines.readlines(fileobj)

        self.line_num = 0    # current index into self.seq (line number)
        self.para_num = 0    # current index into self (paragraph number)

        # Ensure that separator string includes a line-end character at the end
        if separator[-1:] != '\n': separator += '\n'
        self.separator = separator


    def __getitem__(self, index):
        if index != self.para_num:
            raise TypeError, "Only sequential access supported"
        
        self.para_num += 1
        # Start where we left off and skip 0+ separator lines
        while 1:
        # Propagate IndexError, if any, since we're finished if it occurs
            line = self.seq[self.line_num]
            #print "line : ",line
            self.line_num += 1
            if line != self.separator: break
        # Accumulate 1+ nonempty lines into result
        result = [line]
        while 1:
        # Intercept IndexError, since we have one last paragraph to return
            try:
                # Let's check if there's at least one more line in self.seq
                line = self.seq[self.line_num]
                #print "line 2 : ",line
            except IndexError:
                # self.seq is finished, so we exit the loop
                break
            # Increment index into self.seq for next time
            self.line_num += 1
            result.append(line)
            if line == self.separator: break
            
        return ''.join(result)

# Here's an example function, showing how to use class Paragraphs:
def show_paragraphs(filename, numpars=20):
    paralist = []
    pp = Paragraphs(open(filename))
    for p in pp:
        #print "Par#%d : %s" % (pp.para_num, repr(p))
        paralist.append(p)
        if pp.para_num>numpars: break

    return paralist
#print(show_paragraphs('article2'))

