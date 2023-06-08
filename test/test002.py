class MyClass:
    def __init__(self):
        self.shared_var = None

    def func1(self):
        self.shared_var = 10

    def func2(self):
        print(f"shared_var is {self.shared_var}")


# # 创建一个实例化对象 obj
# obj = MyClass()

# 调用 func1()
MyClass().func1()

# 调用 func2()
MyClass().func2()  # 输出: shared_var is 10