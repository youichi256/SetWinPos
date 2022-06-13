from test01 import C05, C03a, C04


class C04b(C04, metaclass=C03a):
    """個別定義クラス"""

    @staticmethod
    def f01(val: str):
        return f"f04b({val}) #########"  # 全部これを使いたい

    A05 = C05("a05xx")
