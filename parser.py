import codecs
import struct

""" Parse data from track 1 in ISO format. """
def ISO_track1(result):
    # confirm track 1 start sentinel
    if result[0] != '25':
        return

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

    print(str(card_data))

""" Parse data from track 2 in ISO format. """
def ISO_track2(result):
    # confirm track 2 start sentinel
    if result[0] != '3b':
        return

    start = current = 1

    for h in result[start:]:
        if h == '3d': # field separator
            break
        current += 1

    pan = codecs.decode(''.join(result[start:current]), 'hex')

    if pan[:2] == '59': # requires country code
        cc == codecs.decode(''.join(result[current+1:current+4]), 'hex')
        current += 4
    else:
        cc = 'N/A'
        current += 1

    if result[current:current+1][0] == '3d': # no expirationd date
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

    card_data = []
    card_data.append('Track 2:')
    card_data.append('  Country Code:\t\t' + cc)
    card_data.append('  Primary Account #:\t' + pan)
    card_data.append('  Expiration Date:\t' + ed)
    card_data.append('  Service Code:\t\t' + sc)
    card_data.append('  PVV:\t\t\t' + pv)
    card_data.append('  Discretionary:\t' + dd)

    print(str(card_data))

""" Parse ISO card data. """
def parse_ISO(data):
    result = [hex(x).replace('0x', '') for x in data]
    print(result)

    for i in range(len(result)):
        if result[i] == '3f' and result[i+1] == '1c' and result[i+2] == '1b':
            t3_end = i
            break
        if result[i] == '1b' and result[i+1] == '3':
            t2_end = i
            i += 2
            t3_start = i
            continue
        if result[i] == '1b' and result[i+1] == '2':
            t1_end = i
            i += 2
            t2_start = i
            continue
        if result[i] == '1b' and result[i+1] == '1':
            i += 2
            t1_start = i
            continue

    ISO_track1(result[t1_start:t1_end])
    ISO_track2(result[t2_start:t2_end])
    '''
    ### TRACK 1 (IATA) ###
    # Start sentinal always begins on index 5, card data on 6
    fcode = codecs.decode(''.join(result[6:7]), 'hex')

    #iterator to keep track of current index of result
    start = current = 7

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

    if result[current:current+1][0] == '1b': # track 2 starts for gift cards
        dd = 'N/A'
    else:
        start = current
        for h in result[start:]:
            if h == '3f':
                break
            current += 1

        dd = codecs.decode(''.join(result[start:current]), 'hex')

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

    ### Track 2 (ABA) ###
    start = current
    for h in result[start:]:
        if h == '3b':
            current += 1
            break
        current += 1

    start = current
    for h in result[start:]:
        if h == '3d': # field separator
            break
        current += 1

    pan = codecs.decode(''.join(result[start:current]), 'hex')

    if pan[:2] == '59': # requires country code
        cc == codecs.decode(''.join(result[current+1:current+4]), 'hex')
        current += 4
    else:
        cc = 'N/A'
        current += 1

    if result[current:current+1][0] == '3d': # no expirationd date
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

    start = current
    for h in result[start:]:
        if h == '3f':
            break
        current += 1

    dd = codecs.decode(''.join(result[start:current]), 'hex')

    card_data.append('Track 2:')
    card_data.append('  Country Code:\t\t' + cc)
    card_data.append('  Primary Account #:\t' + pan)
    card_data.append('  Expiration Date:\t' + ed)
    card_data.append('  Service Code:\t\t' + sc)
    card_data.append('  PVV:\t\t\t' + pv)
    card_data.append('  Discretionary:\t' + dd)

    for v in card_data:
        print(v)

    #print(str(result[current:]))
    if current < len(result):
        print('Track 3:\n  This track has proprietary encoding from the issuer.')'''
