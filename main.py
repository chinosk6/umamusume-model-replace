import umaModelReplace

uma = umaModelReplace.UmaReplace()


def replace_char_body_texture(char_id: str):
    is_not_exist, msg = uma.save_char_body_texture(char_id, False)
    if not is_not_exist:
        print(f"解包资源已存在: {msg}")
        do_replace = input("输入 \"Y\" 覆盖已解包资源, 输入其它内容跳过导出: ")
        if do_replace in ["Y", "y"]:
            _, msg = uma.save_char_body_texture(char_id, True)

    print(f"已尝试导出资源, 请查看目录: {msg}")
    do_fin = input("请进行文件修改/替换, 修改完成后请输入 \"Y\" 打包并替换游戏文件。\n"
                   "若您不想立刻修改, 可以输入其它任意内容退出, 您可以在下次替换时选择\"跳过导出\"\n"
                   "请输入: ")
    if do_fin.strip() in ["Y", "y"]:
        uma.replace_char_body_texture(char_id)
        print("贴图已修改")


if __name__ == "__main__":
    while True:
        do_type = input("[1] 更换头部模型\n"
                        "[2] 更换身体模型\n"
                        "[3] 更换尾巴模型(不建议)\n"
                        "[4] 更换头部与身体模型\n"
                        "[5] 修改角色身体贴图\n"
                        "[6] 更换抽卡开门人物\n"
                        "[7] 更换技能动画\n"
                        "[8] 更换G1胜利动作(实验性)\n"
                        "[9] live服装解锁\n"
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

        if do_type == "5":
            print("请输入7位数ID, 例: 1046_01")
            replace_char_body_texture(input("角色7位ID: "))

        if do_type == "6":
            print("请输入普通开门动画的人物服装6位数ID, 例: 100101、100130")
            uma.edit_gac_chr_start(input("服装6位数ID: "), '001')
            print("请输入理事长开门动画的人物服装的6位数ID, 例: 100101、100130")
            uma.edit_gac_chr_start(input("服装6位数ID: "), '002')
            print("替换完成")

        if do_type == "7":
            print("请输入人物技能6位数ID, 例: 100101、100102")
            uma.edit_cutin_skill(input("替换ID: "), input("目标ID: "))

        if do_type == "8":
            checkDo = input("注意: 目前部分胜利动作替换后会出现破音、黑屏等问题。\n"
                            "若您仍要更改, 请输入y继续: ")
            if checkDo not in ["y", "Y"]:
                continue
            print("请输入胜利动作6位数ID, 例: 100101、100102")
            uma.replace_race_result(input("替换ID: "), input("目标ID: "))
            print("替换完成")

        if do_type == "9":
            uma.unlock_live_dress()
            print("解锁完成")

        if do_type == "98":
            uma.file_restore()
            print("已还原修改")

        if do_type == "99":
            break

        input("Press enter to continue...\n")
