import codecs

""" Parse data from track 1 in ISO format. """
def ISO_track1(result):
    # confirm track 1 start sentinel
    if len(result) == 0 or result[0] != '25':
        return []

    mpt = codecs.decode(''.join(result), 'hex') + '\\0'

    fcode = codecs.decode(''.join(result[1:2]), 'hex')

    # iterators to keep track of current data index
    start = current = 2

    for h in result[start:]:
        if h == '5e': # field separator value
            break
        current += 1

    pan = codecs.decode(''.join(result[start:current]), 'hex')

    if pan[:2] == '59': # requires country code
        cc = codecs.decode(''.join(result[current+1:current+4]), 'hex')
        current += 4
    else:
        cc = 'N/A'
        current += 1

    start = current
    for h in result[start:]:
        if h == '5e': # field separator value
            break
        current += 1

    ch = codecs.decode(''.join(result[start:current]), 'hex').replace('/', ', ')

    current += 1

    if result[current:current+1][0] == '5e': # no expiration date
        ed = 'N/A'
        current += 1
    else:
        ed = codecs.decode(''.join(result[current+2:current+4]), 'hex') + '/' + codecs.decode(''.join(result[current:current+2]), 'hex')
        current += 4

    if result[current:current+3][0] == '5e': # no service code
        sc = 'N/A'
        current += 1
    else:
        sc = codecs.decode(''.join(result[current:current+3]), 'hex')
        current += 3

    if result[current:current+1][0] == '30': # no PVV
        pv = 'N/A'
    else:
        pv = codecs.decode(''.join(result[current+1:current+5]), 'hex')
    current += 5

    # if end of data is reached, there is no dd (probably a gift card)
    if current != len(result):
        dd = codecs.decode(''.join(result[current:len(result)-1]), 'hex')
    else:
        dd = 'N/A'

    card_data = []
    card_data.append('Track 1:')
    card_data.append('  Format Code:\t\t' + fcode)
    card_data.append('  Country Code:\t\t' + cc)
    card_data.append('  Primary Account #:\t' + pan)
    card_data.append('  Card Holder:\t\t' + ch)
    card_data.append('  Expiration Date:\t' + ed)
    card_data.append('  Service Code:\t\t' + sc)#TODO add service code description
    card_data.append('  PVV:\t\t\t' + pv)
    card_data.append('  Discretionary:\t' + dd)
    card_data.append('  - MagSpoof plaintext:\t' + mpt)

    return card_data

""" Parse data from track 2 in ISO format. """
def ISO_track2(result, card_data):
    start = current = 1

    # confirm track 2 start sentinel
    if len(result) == 0 or result[0] != '3b':
        if len(result) == 0 or result[1] != '3b':
            return card_data
        else:
            start = current = 2

    for h in result[start:]:
        if h == '3d': # field separator
            break
        current += 1

    mpt = codecs.decode(''.join(result[start-1:]), 'hex') + '\\0'

    pan = codecs.decode(''.join(result[start:current]), 'hex')

    if pan[:2] == '59': # requires country code
        cc == codecs.decode(''.join(result[current+1:current+4]), 'hex')
        current += 4
    else:
        cc = 'N/A'
        current += 1

    if result[current:current+1][0] == '3d': # no expiration date
        ed = 'N/A'
        current += 1
    else:
        ed = codecs.decode(''.join(result[current+2:current+4]), 'hex') + '/' + codecs.decode(''.join(result[current:current+2]), 'hex')
        current += 4

    if result[current:current+3][0] == '3d': # no service code
        sc = 'N/A'
        current += 1
    else:
        sc = codecs.decode(''.join(result[current:current+3]), 'hex')
        current += 3

    if result[current:current+1][0] == '30': #no PVV
        pv = 'N/A'
    else:
        pv = codecs.decode(''.join(result[current+1:current+5]), 'hex')
    current += 5

    dd = codecs.decode(''.join(result[current:len(result)-1]), 'hex')

    if 'Track 2:' not in card_data:
        card_data.append('Track 2:')
        card_data.append('  Country Code:\t\t' + cc)
        card_data.append('  Primary Account #:\t' + pan)
        card_data.append('  Expiration Date:\t' + ed)
        card_data.append('  Service Code:\t\t' + sc)
        card_data.append('  PVV:\t\t\t' + pv)
        card_data.append('  Discretionary:\t' + dd)
        card_data.append('  - MagSpoof plaintext:\t' + mpt)

    return card_data

""" Parse data from track 3 in ISO format. ms parameter is for MagSpoof use. """
def ISO_track3(result, card_data, ms):
    if ms:
        return ISO_track2(result, card_data)

    # confirm track 3 start sentinel
    if len(result) == 0 or result[0] != '3b':
        return card_data

    start = current = 1
    
    card_data.append('Track 3:')
    card_data.append('  This track contains the following proprietary encoded data:')
    card_data.append('  ' + str(result))
    card_data.append('  > ' + codecs.decode(''.join(result), 'hex'))

    return card_data

""" Parse ISO card data. ms is for use by MagSpoof. """
def parse_ISO(data, ms):
    result = [hex(x).replace('0x', '') for x in data]
    #print(str(result))
    for i in range(len(result)):
        if result[i] == '3f' and result[i+1] == '1c' and result[i+2] == '1b':
            t3_end = i
            break
        elif result[i] == '1b' and result[i+1] == '3':
            t2_end = i
            t3_start = i+2
        elif result[i] == '1b' and result[i+1] == '2':
            t1_end = i
            t2_start = i+2
        elif result[i] == '1b' and result[i+1] == '1':
            t1_start = i+2

    card_data = ISO_track1(result[t1_start:t1_end])
    card_data = ISO_track2(result[t2_start:t2_end], card_data)
    card_data = ISO_track3(result[t3_start:t3_end], card_data, ms)
    
    for i in card_data:
        print(i)

""" Parse binary from RAW track 2/3. """
def RAW_t23_binary():
    graph = {
            '00001': '0',
            '10000': '1',
            '01000': '2',
            '11001': '3',
            '00100': '4',
            '10101': '5',
            '01101': '6',
            '11100': '7',
            '00010': '8',
            '10011': '9',
            '01011': ':',
            '11010': ';',
            '00111': '<',
            '10110': '=',
            '01110': '>',
            '11111': '?'
            }
    return graph

""" Parse binary from RAW track 1. """
def RAW_t1_binary():
    graph = {
            '000000': ' ',
            '000010': '0',
            '000001': '@',
            '000011': 'P',

            '100000': '!',
            '100010': '1',
            '100001': 'A',
            '100011': 'Q',

            '010000': '\"',
            '010010': '2',
            '010001': 'B',
            '010011': 'R',

            '110000': '#',
            '110010': '3',
            '110001': 'C',
            '110011': 'S',
            
            '001000': '$',
            '001010': '4',
            '001001': 'D',
            '001011': 'T',

            '101000': '%',
            '101010': '5',
            '101001': 'E',
            '101011': 'U',

            '011000': '&',
            '011010': '6',
            '011001': 'F',
            '011011': 'V',

            '111000': '\'',
            '111010': '7',
            '111001': 'G',
            '111011': 'W',

            '000100': '(',
            '000110': '8',
            '000101': 'H',
            '000111': 'X',
            
            '100100': ')',
            '100110': '9',
            '100101': 'I',
            '100111': 'Y',
            
            '010100': '*',
            '010110': ':',
            '010101': 'J',
            '010111': 'Z',
            
            '110100': '+',
            '110110': ';',
            '110101': 'K',
            '110111': '[',

            '001100': '`',
            '001110': '<',
            '001101': 'L',
            '001111': '\\',
            
            '101100': ',',
            '101110': '=',
            '101101': 'M',
            '101111': ']',
            
            '011100': '.',
            '011110': '>',
            '011101': 'N',
            '011111': '^',

            '111100': '/',
            '111110': '?',
            '111101': 'O',
            '111111': '_'
            }
    return graph

""" Parse RAW data from track 1."""
def RAW_track1(data):
    if len(data) <= 1:
        return []
    for i in range(len(data)):
        if len(data[i]) == 1:
            data[i] = '0'+data[i]
    
    length = codecs.decode(data[0], 'hex') 
    
    rd = str(data[1:])

    bn = bin(int((''.join(data[1:])), 16))[2:].zfill(32)
    bn2 = ''
    count = 0
    for c in bn:
        count += 1
        bn2 += c
        if count == 7:
            bn2 += ' '
            count = 0

    g = RAW_t1_binary()
    bn2l = bn2.split(' ')
    dc = ''
    for e in bn2l:
        if len(e) < 6:
            continue
        if e[:6] in g:
            dc += g[e[:6]]
        else:
            dc += '|' #unique identifier for missing characters

    card_data = []
    card_data.append('Track 1:')
    card_data.append('  Length: ' + length)
    card_data.append('  Encoded Raw Data: ' + rd)
    card_data.append('  Encoded Binary: ' + bn2)
    card_data.append('  Decoded Data: ' + dc)

    return card_data

""" Parse RAW data from track 2. """
def RAW_track2(data, card_data):
    if len(data) <= 1:
        return card_data
    for i in range(len(data)):
        if len(data[i]) == 1:
            data[i] = '0'+data[i]
            
    length = codecs.decode(data[0], 'hex') 
    rd = str(data[1:])

    bn = bin(int((''.join(data[1:])), 16))[2:].zfill(32)
    bn2 = ''
    count = 0
    for c in bn:
        count += 1
        bn2 += c
        if count == 5:
            bn2 += ' '
            count = 0

    g = RAW_t23_binary()
    bn2l = bn2.split(' ')
    dc = ' '
    for e in bn2l:
        if len(e) < 5:
            continue
        if e in g:
            dc += g[e]
        else:
            dc += '|' #unique identifier for missing characters

    card_data.append('Track 2:')
    card_data.append('  Length: ' + length)
    card_data.append('  Encoded Raw: ' + rd)
    card_data.append('  Encoded Binary: ' + bn2)   
    card_data.append('  Decoded Data: ' + dc)

    return card_data   

""" Parse RAW data from track 3. """
def RAW_track3(data, card_data):
    if len(data) <= 1:
        return card_data
    for i in range(len(data)):
        if len(data[i]) == 1:
            data[i] = '0'+data[i]
            
    length = codecs.decode(data[0], 'hex') 
    rd = str(data[1:])

    bn = bin(int((''.join(data[1:])), 16))[2:].zfill(32)
    bn2 = ''
    count = 0
    for c in bn:
        count += 1
        bn2 += c
        if count == 5:
            bn2 += ' '
            count = 0

    g = RAW_t23_binary()
    bn2l = bn2.split(' ')
    dc = ' '
    for e in bn2l:
        if len(e) < 5:
            continue
        if e in g:
            dc += g[e]
        else:
            dc += '|' # unique identifier for missing characters

    card_data.append('Track 3:')
    card_data.append('  Length: ' + length)
    card_data.append('  Raw: ' + rd)
    card_data.append('  Binary: ' + bn)
    card_data.append('  Decoded: ' + dc)

    return card_data   

""" Parse RAW card data. """
def parse_RAW(data):
    result = [hex(x).replace('0x', '') for x in data]
    #print(str(result))
    for i in range(len(result)):
        if result[i] == '3f' and result[i+1] == '1c' and result[i+2] == '1b':
            t3_end = i
            break
        elif result[i] == '1b' and result[i+1] == '3':
            t2_end = i
            t3_start = i+2
        elif result[i] == '1b' and result[i+1] == '2':
            t1_end = i
            t2_start = i+2
        elif result[i] == '1b' and result[i+1] == '1':
            t1_start = i+2

    card_data = RAW_track1(result[t1_start:t1_end])
    card_data = RAW_track2(result[t2_start:t2_end], card_data)
    card_data = RAW_track3(result[t3_start:t3_end], card_data)

    for i in range(len(card_data)):
        if card_data.index(card_data[i]) >= i:
            print(card_data[i])
