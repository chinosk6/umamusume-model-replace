import umaModelReplace

if __name__ == "__main__":
    uma = umaModelReplace.UmaReplace()

    while True:
        do_type = input("[1] 更换头部模型\n"
                        "[2] 更换身体模型\n"
                        "[3] 更换尾巴模型(不建议)\n"
                        "[4] 更换头部与身体模型\n"
                        "[98] 复原所有修改\n"
                        "[99] 退出\n"
                        "请选择您的操作: ")

        if do_type == "1":
            print("请输入7位数ID, 例: 1046_01")
            uma.replace_head(input("替换ID: "), input("目标ID: "))
            print("替换完成")

        if do_type == "2":
            print("请输入7位数ID, 例: 1046_01")
            uma.replace_body(input("替换ID: "), input("目标ID: "))
            print("替换完成")

        if do_type == "3":
            checkDo = input("注意: 目前无法跨模型更换尾巴, 更换目标不能和原马娘同时出场。\n"
                            "若您仍要更改, 请输入y继续: ")
            if checkDo not in ["y", "Y"]:
                continue
            print("请输入4位数ID, 例: 1046")
            uma.replace_tail(input("替换ID: "), input("目标ID: "))
            print("替换完成")

        if do_type == "4":
            print("请输入7位数ID, 例: 1046_01")
            inId1 = input("替换ID: ")
            inId2 = input("目标ID: ")
            uma.replace_head(inId1, inId2)
            uma.replace_body(inId1, inId2)
            print("替换完成")

        if do_type == "98":
            uma.file_restore()
            print("已还原修改")

        if do_type == "99":
            break

        print("\n")
