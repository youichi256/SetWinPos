from test01 import C05, C03a, C04


class C04a(C04, metaclass=C03a):
    """個別定義クラス"""

    @staticmethod
    def f01(val: str):
        return f"f04a({val}) #########"  # 全部これを使いたい

    A04 = C05("a04xx")
