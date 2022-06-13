import inspect

from abc import abstractmethod


class C05:
    """設定値クラス"""

    def __init__(self, msg: str):
        self.__msg = msg

    @staticmethod
    def f01(val: str):
        """f01です"""
        raise "dummy"  # 使いたくない

    name = ""
    """名前"""

    value = ""
    """値"""


class C04:
    """共通定義クラス"""

    @staticmethod
    @abstractmethod
    def f01(val: str):
        raise "dummy"

    A03 = C05("a03xx")


class C03a(type):
    """設定値メタクラス"""

    def __new__(mcs, name: str, bases, attributes):
        print("## " + str(__class__) + " " + inspect.currentframe().f_code.co_name)

        # print(bases)
        # print(bases[0])
        bbb = bases[0]
        # print(bbb.__dict__)
        # print(bbb.A03)
        # print(type(bbb))
        # print(type(bases[0]))
        # print(type(bases[0]).__name__)

        pp = {}

        # 基底クラスから引き継いだ定義
        for key in bbb.__dict__:
            org_class = getattr(bbb, key).__class__.__name__
            if org_class == "C05":
                # print(getattr(bbb, key).__dir__())
                # for key2 in getattr(bbb, key).__dir__():
                #     print(f"key2({key2})=" + str(getattr(getattr(bbb, key), key2)))
                # print(getattr(getattr(bbb, key), "name2"))
                # attributes[key] = type("D01", (), {"name": f"key={key}", "f01": attributes["f01"]})
                attributes[key] = type("C05", (), {})
                pp[key] = getattr(bbb, key)

        # print(attributes["A03"].__dict__)
        # setattr(C04a.__class__, "f01", attributes["f01"])
        # setattr(attributes["A03"], "f01", attributes["f01"])

        # クラスでの定義
        for key in attributes:
            org_class = attributes[key].__class__.__name__
            # print(f"key={key},class={org_class}")
            if org_class == "C05":
                # print(attributes[key].__dir__())
                pp[key] = attributes[key]
                # setattr(attributes[key], "name", "key=A04")
                # setattr(attributes[key], "f01", attributes["f01"])

        # 定義の属性を設定
        for key in pp:
            # print(pp[key].__dir__())
            # for key2 in pp[key].__dir__():
            #     print(f"key2({key2})=" + str(getattr(pp[key], key2)))
            # print(getattr(pp[key], "name2"))
            # print(getattr(pp[key], "_C05__msg"))

            setattr(attributes[key], "f01", attributes["f01"])
            setattr(attributes[key], "value", getattr(pp[key], "_C05__msg"))
            setattr(attributes[key], "name", key)

        print(f"### name={name},bases={bases},attributes={attributes}")
        return super().__new__(mcs, name, bases, attributes)
