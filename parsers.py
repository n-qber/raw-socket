class ToS:
    tos_mid = {"minimum_delay": 8, "maximum_throughput": 4, "maximum_reliability": 2, "normal_service": 0, "maximum_security": 15}
    tos_names = ["precedence", "delay", "throughput", "reliability", "cost", "mbz"]

    @staticmethod
    def make(args):
        tos = 0
        if type(args) is list:
            for pos, value in enumerate(args[::-1]):
                if type(value) is not int:
                    value = 0
                tos += value << pos
            return tos

        if type(args) is dict:

            for pos, argument in enumerate(ToS.tos_names[::-1]):
                if argument not in args:
                    args[argument] = 0

                if type(args[argument]) is str:
                    pass

                tos += args[argument] << pos

            return tos
