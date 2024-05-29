# This program can randomly generate IPv4-addresses for practicing some knowledge.

from random import randint

#function for calculating netmask in binary format
def ip_netmask(bits):
    net_mask = [[0 for i in range(8)] for i in range(4)]
    counter = 0
    for i in range(0, 4):
        for j in range(0, 8):
            if counter == netmask:
                break
            net_mask[i][j] += 1
            counter += 1
    return net_mask

#function for calculating IPv4 in string form
def string_IPv4(octets):
    ipv4 = ''
    for i in range(4):
        if i == 3:
            ipv4 += str(octets[i])
            continue
        ipv4 += str(octets[i]) + '.'
    return ipv4

#figuring netmask in decimal form
def netmask_dec(arr_octets):
    netmask = []
    for i in range(4):
        tmp_str = ''
        for j in range(8):
            tmp_str += str(arr_octets[i][j])
        netmask.append(int(tmp_str, 2))
    return netmask

#######################################################################
#main part of program
user_netmask = ''
while user_netmask != 'stop':
    #genereting ipv4-address
    gen_ipv4 = [randint(0, 255) for i in range(0, 4)]

    #generating netmask
    netmask = randint(10, 30)
    ipv4 = string_IPv4(gen_ipv4)
    print('IPv4: %s/%d' % (ipv4, netmask))

    #convert IPv4 to binary mode: for each octet of address -> array of binary format - 0 and 1
    ip_bin = [[int(bin(gen_ipv4[i])[j])for j in range(2, len(bin(gen_ipv4[i])))] for i in range(0, 4)]
    print(ip_bin)

    #ip to full format(4 * 8 bits = 32 bits)
    full_bin_ip = []
    for i in range(0, 4):
        tmp_size = len(ip_bin[i])
        full_bin_ip.append([0 for elem in range(8 - tmp_size)])
        full_bin_ip[i] += ip_bin[i]
    print(full_bin_ip)

    #output netmask in binary format
    networkm = ip_netmask(netmask)

    print(networkm)

    #calculating operation AND for IPv4 and subnetmask for this IPv4
    network_addr = []
    netaddr_str = ['' for i in range(0, 4)]
    for i in range(4):
        tmp_octet = []
        for j in range(8):
            tmp_octet.append(full_bin_ip[i][j] * networkm[i][j])
            netaddr_str[i] += str(full_bin_ip[i][j] * networkm[i][j])
        network_addr.append(tmp_octet)
    print('Network address: ', network_addr)
    print('Network address in strings: ', netaddr_str)

    #convert binary network address to dicimal format
    dec_temp = [int(netaddr_str[i], 2) for i in range(0, 4)]
    dec_netaddr = string_IPv4(dec_temp)
    print('\nNetwork addres for %s: %s\n' % (ipv4, dec_netaddr))

    #Now figuring wild-card for this network
    dec_netmask = netmask_dec(ip_netmask(netmask))
    wild_card = []
    tmp_arr = [255 for i in range(4)]
    for i in range(4):
        wild_card.append(tmp_arr[i] - dec_netmask[i])
    print('\nWild-card for network %s: %s\n' % (dec_netaddr, string_IPv4(wild_card)))

    #input user variant
    user_netmask = input('Enter your network address: ')
    print(dec_netaddr)
    if user_netmask == dec_netaddr:
        print('You calculating right network address! GOOD!')
    #17.05.2020 - adding code ~~~~~~~~~~~~~~
    elif user_netmask == 'stop':
        print('Okey. Bye)')
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~
    else:
        print('Unfortunetly, you wrong. Try again.')
