from parsers import ToS
from random import randrange
from socket import *


class Ipv4:
    def __init__(self,  version: int = 4,
                        header_length: int = None,
                        type_of_service: list = 0,
                        total_length: int = None,
                        identification: int = randrange(65536),
                        null_bit: type(None) = 0,
                        dont_fragment: int = 0,
                        more_fragment: int = 0,
                        fragment_offset: int = 0,
                        ttl: int = 128,
                        protocol: str = 6,
                        header_checksum: int = None,
                        source_ip: str = gethostbyname_ex(gethostname()),
                        destination_ip: str = None,
                        option: type(None) = None,
                        data: bytes=b""):

        if type(type_of_service) is not int:
            type_of_service = ToS.make(type_of_service)

        self.protocols = {"TCP": 6,
                        "UDP": 17,
                        "IGMP": 2,
                        "ICMP": 1,
                        "IGRP": 9,
                        "GRE": 47,
                        "ESP": 50,
                        "AH": 51,
                        "SKIP": 57,
                        "EIGRP": 88,
                        "OSPF": 89,
                        "L2TP": 115}

        if version != 4:
            print("wtf... anyway your version is different than 4, but this is an ipv4 header...well, idc")

        if type(protocol) is str:
            assert protocol in self.protocols, f"Protocol:\"{protocol}\" is not supported by it's name, you should put it's code instead"
            protocol = self.protocols[protocol]

        if header_length is None:
            header_length = 5 + len(option)

        if total_length is None:
            total_length = header_length + len(data)

        if destination_ip is None:
            print("Mam, you forgot the destination_ip")

        self.null_bit = null_bit
        self.dont_fragment = dont_fragment
        self.more_fragment = more_fragment
        self.fragment_offset = fragment_offset
        self.identification = identification
        self.header_length = header_length
        self.protocol = protocol
        self.version = version
        self.ttl = ttl
        self.protocol = protocol
        self.total_length = total_length
        self.source_ip = source_ip
        self.destination_ip = destination_ip

        self.type_of_service = type_of_service

        if header_checksum is None:
            header_checksum = self.check_sum()

        self.header_checksum = header_checksum

    @staticmethod
    def invert_bits(number, size=16):

        if type(number) is int:
            number = bin(number)[2:]

        number = "0" * (size - len(number)) + number

        # copy stolen from here
        # https://codegolf.stackexchange.com/questions/30361/the-shortest-code-to-invert-bit-wise-a-binary-string
        # Thanks from Bassem and TheRare
        return int((''.join([str(1-int(x)) for x in number])), 2)

    @staticmethod
    def raw_ip(ip):
        return bytes(map(int, ip.split(".")))

    @staticmethod
    def ip_sum(ip):
        if type(ip) is str:
            ip = Ipv4.raw_ip(ip)

        first_part = ip[:2]
        first_number = (first_part[0] << 8) + first_part[1]

        second_part = ip[2:]
        second_number = (second_part[0] << 8) + second_part[1]

        return first_number + second_number

    def check_sum(self):
        _sum = (self.version << 12) + (self.header_length << 8) + self.type_of_service
        _sum += self.total_length
        _sum += self.identification
        _sum += (self.null_bit << 15) + (self.dont_fragment << 14) + (self.more_fragment << 13) + self.fragment_offset
        _sum += (self.ttl << 8) + self.protocol
        _sum += Ipv4.ip_sum(self.source_ip)
        _sum += Ipv4.ip_sum(self.destination_ip)

        return Ipv4.invert_bits(_sum)


if __name__ == '__main__':
    print(Ipv4(version = 4,
                header_length = 5,
                type_of_service = 0,
                total_length = 28,
                identification = 1,
                ttl = 4,
                protocol = 17,
                source_ip = "10.12.14.5",
                destination_ip = "12.6.7.9",
                option = None,
                data = b"").header_checksum)
