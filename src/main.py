import sys
import usb.core
import usb.util
import paho.mqtt.publish as publish
import json
from os import environ

mqtt_host  = environ.get('MQTT_HOST', 'localhost')
mqtt_topic = environ.get('MQTT_TOPIC', 'sync/reader')
vendor_id  = environ.get('READER_USB_VENDOR_ID', '0x6352')
product_id = environ.get('READER_USB_PRODUCT_ID', '0x213a')

chrMap = {
    4:  'a',
    5:  'b',
    6:  'c',
    7:  'd',
    8:  'e',
    9:  'f',
    10: 'g',
    11: 'h',
    12: 'i',
    13: 'j',
    14: 'k',
    15: 'l',
    16: 'm',
    17: 'n',
    18: 'o',
    19: 'p',
    20: 'q',
    21: 'r',
    22: 's',
    23: 't',
    24: 'u',
    25: 'v',
    26: 'w',
    27: 'x',
    28: 'y',
    29: 'z',
    30: '1',
    31: '2',
    32: '3',
    33: '4',
    34: '5',
    35: '6',
    36: '7',
    37: '8',
    38: '9',
    39: '0',
    40: 'KEY_ENTER',
    41: 'KEY_ESCAPE',
    42: 'KEY_BACKSPACE',
    43: 'KEY_TAB',
    44: ' ',
    45: '-',
    46: '=',
    47: '[',
    48: ']',
    49: '\\',
    51: ';',
    52: '\'',
    53: '`',
    54: ',',
    55: '.',
    56: '/',
    57: 'KEY_CAPSLOCK'
}

shiftchrMap = {
    4:  'A',
    5:  'B',
    6:  'C',
    7:  'D',
    8:  'E',
    9:  'F',
    10: 'G',
    11: 'H',
    12: 'I',
    13: 'J',
    14: 'K',
    15: 'L',
    16: 'M',
    17: 'N',
    18: 'O',
    19: 'P',
    20: 'Q',
    21: 'R',
    22: 'S',
    23: 'T',
    24: 'U',
    25: 'V',
    26: 'W',
    27: 'X',
    28: 'Y',
    29: 'Z',
    30: '!',
    31: '@',
    32: '#',
    33: '$',
    34: '%',
    35: '^',
    36: '&',
    37: '*',
    38: '(',
    39: ')',
    40: 'KEY_ENTER',
    41: 'KEY_ESCAPE',
    42: 'KEY_BACKSPACE',
    43: 'KEY_TAB',
    44: ' ',
    45: '_',
    46: '+',
    47: '{',
    48: '}',
    49: '|',
    51: ':',
    52: '"',
    53: '~',
    54: '<',
    55: '>',
    56: '?',
    57: 'KEY_CAPSLOCK'
}

vendor_id = int(vendor_id, 16)
product_id = int(product_id, 16)

print('vendor_id %s, product_id %s' % (vendor_id, product_id))

#dev = usb.core.find(idVendor=0x6352, idProduct=0x213a)
dev = usb.core.find(idVendor=vendor_id, idProduct=product_id)
ep = dev[0].interfaces()[0].endpoints()[0]
i = dev[0].interfaces()[0].bInterfaceNumber

dev.reset()

if dev.is_kernel_driver_active(i):
    dev.detach_kernel_driver(i)

dev.set_configuration()

eaddr = ep.bEndpointAddress
emax = ep.wMaxPacketSize

data = []
datalist = []
swiped = False
print("Please swipe your card...")

while True:
    try:
        
        #data += dev.read(eaddr, emax, timeout=1000)
        results = dev.read(eaddr, emax, timeout=1000)
        data += results
        datalist.append(results)
        if not swiped:
            print("Reading...")
        swiped = True

    except usb.core.USBError as e:
        
        if e.args[1] == ('Operation timed out') and swiped:

            if len(data) < emax:
                
                print("Bad swipe, try again. %d bytes" % len(data))

                data = []
                datalist = []
                swiped = False
                continue
            else:
                #break   # we got it!

                try:
                    #print('data len -> ', len(data))
                    # create a list of 8 bit bytes and remove.. empty bytes
                    ndata = []
                    for d in datalist:
                        if d.tolist() != [0, 0, 0, 0, 0, 0, 0, 0]:
                            ndata.append(d.tolist())

                    # parse over our bytes and create string to final return
                    sdata = ''
                    for n in ndata:
                        # handle non shifted letters
                        if n[2] in chrMap and n[0] == 0:
                            sdata += chrMap[n[2]]
                        # handle shifted letters
                        elif n[2] in shiftchrMap and n[0] == 2:
                            sdata += shiftchrMap[n[2]]

                    #print('sdata -> ', sdata)
                    card = sdata[14:22]
                    print('card number -> ', card)
                    data = []
                    datalist = []
                    swiped = False

                    payload = {'cardNumber':card}
                    publish.single(mqtt_topic, json.dumps(payload), hostname=mqtt_host)
                    print('[reader] message sent.. card number: %s' % payload)

                except Exception as e:
                    print ("[x] error in message emitter.. {}".format(e))
                    continue

