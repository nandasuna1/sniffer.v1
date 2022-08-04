import socket
import struct
import textwrap

def main():
    conn = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))

    while True:
        raw_data, addr= conn.recvfrom(65536)
        dest_mac, src_mac, eth_proto, data = ethernet_frame(raw_data)
        print('\n Ethernet Frame:')
        print('Destination: {}, Source: {}, Protocol: {}'.format(dest_mac, src_mac, eth_proto))

# Desestruturando pacote ethernet, recebido em binário
# tratando dados para que a forma como eles são armazenados seja a mesma
# data[:14] -> cabeçalho || data[14:]-> payload
# retorna o endereço de destino, o endereco de envio, o protocolo e o payload respectivamente
def ethernet_frame(data):
    mac_destino, mac_fonte, protocolo = struct.unpack('! 6s 6s H', data[:14])
    return get_mac_address(mac_destino), get_mac_address(mac_fonte), socket.htons(protocolo), data[14:]

# Retorna o endereço MAC formatado para leitura
# transforma os bytes em 2 digitos decimais formatados (ex AA:BB:CC:DD:EE:FF)
def get_mac_address(byte_addr):
    bytes_str = map('{:02x}'.format, byte_addr)
    mac_addr = ':'.join(bytes_str).upper()
    return mac_addr


main()