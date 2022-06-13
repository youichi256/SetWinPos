from test01 import C05
from test02a import C04a
from test02b import C04b


def main():
    put(C04a.A03)
    put(C04a.A04)
    put(C04b.A03)
    put(C04b.A05)


def put(val: C05):
    """put"""
    # print("----")
    # print(val)
    # print(val.__class__)
    # print(val.__dir__())
    # print(val.__dict__)
    # print("#name=" + val.name)
    # print("#val=" + val.value)
    print(f"#f01({val.name})=" + val.f01(val.value))


main()
