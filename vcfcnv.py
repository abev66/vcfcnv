#!/usr/bin/env python
#

import sys

def getfile ( argv ):
    
    if len( argv ) < 2:
        print ( "No filename given" )
        return None
    else:
        filename = sys.argv[1]
    
    try:
        fp = open( filename , "r" )
    except IOError:
        print( "Unable to open file: %s" % filename )
        return None
    
    content = fp.readlines()
    fp.close()
    
    return content
    

def parser( content ):
    
    patterns = { 
          'FN:'      : 'FN;CHARSET=UTF-8:',
          'N:'       : 'N;CHARSET=UTF-8:',
          'ADR;'     : 'ADR;CHARSET=UTF-8;',
          'ADR:'     : 'ADR;CHARSET=UTF-8:',
          'ORG:'     : 'ORG;CHARSET=UTF-8:',
          'ORG;'     : 'ORG;CHARSET=UTF-8;',
          'TITLE:'   : 'TITLE;CHARSET=UTF-8:',
          'TITLE;'   : 'TITLE;CHARSET=UTF-8;',
          'NICKNAME:': 'NICKNAME;CHARSET=UTF-8:',
          'NICKNAME;': 'NICKNAME;CHARSET=UTF-8;',
        }
    
    newcontent = []
    
    for line in content:
        if ( line.find("BEGIN:VCARD") != -1 ) or (line.find("END:VCARD") != -1):
            newcontent.append(line)
            continue
        
        o = line
        for f, t in patterns.items():
            o = o.replace( f, t )
        newcontent.append(o)
    
    return newcontent

def splitter ( content ):
    
    cards = []
    card = []
    
    for line in content: 
        if line.find("BEGIN:VCARD") != -1:
            card = []
            card.append(line)
            
        elif line.find("END:VCARD") != -1:
            card.append(line)
            cards.append(card)
            
        elif len(line) < 1:
            continue
        
        else:
            card.append(line)
    
    return cards

def getname( card ):
    
    for line in card:
        s1 = line.find("FN;")
        s2 = line.find("FN:")
        
        if ( s1 != -1 ):
            beg = line.find(":", s1)
            return line[beg+1:-2]
        
        elif ( s2 != -1 ) :
            return line[s2+3:-2]

if __name__ == '__main__':
    
    content = getfile(sys.argv)
    
    if content == None :
        print("Done")
        sys.exit(0)
    
    content = parser(content)
        
    cards = splitter ( content )
    
    for card in cards:
        try:
            out = open ( ( "%s.vcf" % getname(card) ), "w" )
            out.writelines( card )
            out.close()
            
        except IOError:
            print ( "Unable to output vCard: %s.vcf" % getname(card) )
            continue
    