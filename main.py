import umaModelReplace
import os
import shutil
import UnityPy
from tkinter import filedialog

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


def replace_char_head_texture(char_id: str):
    for n, i in enumerate(uma.save_char_head_texture(char_id, False)):
        is_not_exist, msg = i

        if not is_not_exist:
            print(f"解包资源已存在: {msg}")
            do_replace = input("输入 \"Y\" 覆盖已解包资源, 输入其它内容跳过导出: ")
            if do_replace in ["Y", "y"]:
                _, msg = uma.save_char_head_texture(char_id, True, n)[0]

        print(f"已尝试导出资源, 请查看目录: {msg}")

    do_fin = input("请进行文件修改/替换, 修改完成后请输入 \"Y\" 打包并替换游戏文件。\n"
                   "若您不想立刻修改, 可以输入其它任意内容退出, 您可以在下次替换时选择\"跳过导出\"\n"
                   "请输入: ")
    if do_fin.strip() in ["Y", "y"]:
        uma.replace_char_head_texture(char_id)


def replace_support_card_texture(card_id: str, overwrite: bool):
    if overwrite == True:
        for n, i in enumerate(uma.save_support_card_texture(card_id, False)):
            is_not_exist, msg = i

            if not is_not_exist:
                print(f"文件夹已存在: {msg}")
                do_replace = input("输入 \"Y\" 覆盖已解包资源, 输入其它内容跳过导出: ")
                if do_replace in ["Y", "y"]:
                    _, msg = uma.save_support_card_texture(card_id, True, n)[0]

                print(f"已尝试导出资源, 请查看目录: {msg}")

        do_fin = input("请进行文件修改/替换, 修改完成后请输入 \"Y\" 打包并替换游戏文件。\n"
                       "若您不想立刻修改, 可以输入其它任意内容退出, 您可以在下次替换时选择\"跳过导出\"\n"
                       "请输入: ")
        if do_fin.strip() in ["Y", "y"]:
            uma.replace_support_card_texture(card_id)

    else:
        uma.replace_support_card_texture(card_id)


def replace_support_thumb_texture(card_id: str, overwrite: bool):
    if overwrite == True:
        for n, i in enumerate(uma.save_support_thumb_texture(card_id, False)):
            is_not_exist, msg = i

            if not is_not_exist:
                print(f"文件夹已存在: {msg}")
                do_replace = input("输入 \"Y\" 覆盖已解包资源, 输入其它内容跳过导出: ")
                if do_replace in ["Y", "y"]:
                    _, msg = uma.save_support_thumb_texture(card_id, True, n)[0]

                print(f"已尝试导出资源, 请查看目录: {msg}")

        do_fin = input("请进行文件修改/替换, 修改完成后请输入 \"Y\" 打包并替换游戏文件。\n"
                       "若您不想立刻修改, 可以输入其它任意内容退出, 您可以在下次替换时选择\"跳过导出\"\n"
                       "请输入: ")
        if do_fin.strip() in ["Y", "y"]:
            uma.replace_support_thumb_texture(card_id)

    else:
        uma.replace_support_thumb_texture(card_id)


def get_bundle_name(fullPath):
    begin = fullPath.rfind("/") + 1
    end = fullPath.rfind(".")
    if end != -1:
        result = fullPath[begin:end]
    else:
        result = fullPath[begin:]
    return result


if __name__ == "__main__":
    while True:
        do_type = input("[11] 更换头部模型\n"
                        "[12] 更换身体模型\n"
                        "[13] 更换尾巴模型(不建议)\n"
                        "[14] 更换头部与身体模型\n"
                        "[15] 更换抽卡开门人物\n"
                        "[21] 修改角色身体贴图\n"
                        "[22] 修改角色头部贴图\n"
                        "[23] 修改支援卡贴图\n"
                        "[24] 修改支援卡缩略图贴图\n"
                        "[25] 批量修改支援卡\n"
                        "[3]  更换技能动画\n"
                        "[4]  更换G1胜利动作(实验性)\n"
                        "[51] Live服装解锁\n"
                        "[52] 清除Live所有模糊效果\n"
                        "[8]  安装MOD\n"
                        "[9]  复原所有修改\n"
                        "[91] 清理 backup,edited 文件夹\n"
                        "[0] 退出\n"
                        "请选择您的操作: ")

        if do_type == "11":
            print("请输入7位数ID, 例: 1046_01")
            uma.replace_head(input("替换ID: "), input("目标ID: "))
            print("替换完成")

        if do_type == "12":
            print("请输入7位数ID, 例: 1046_01")
            uma.replace_body(input("替换ID: "), input("目标ID: "))
            print("替换完成")

        if do_type == "13":
            checkDo = input("注意: 目前无法跨模型更换尾巴, 更换目标不能和原马娘同时出场。\n"
                            "若您仍要更改, 请输入y继续: ")
            if checkDo not in ["y", "Y"]:
                continue
            print("请输入4位数ID, 例: 1046")
            uma.replace_tail(input("替换ID: "), input("目标ID: "))
            print("替换完成")

        if do_type == "14":
            print("请输入7位数ID, 例: 1046_01")
            inId1 = input("替换ID: ")
            inId2 = input("目标ID: ")
            uma.replace_head(inId1, inId2)
            uma.replace_body(inId1, inId2)
            print("替换完成")

        if do_type == "15":
            print("请输入普通开门动画的人物服装6位数ID, 例: 100101、100130")
            uma.edit_gac_chr_start(input("服装6位数ID: "), '001')
            print("请输入理事长开门动画的人物服装的6位数ID, 例: 100101、100130")
            uma.edit_gac_chr_start(input("服装6位数ID: "), '002')
            print("替换完成")

        if do_type == "21":
            print("请输入7位数ID, 例: 1046_01")
            replace_char_body_texture(input("角色7位ID: "))

        if do_type == "22":
            print("请输入7位数ID, 例: 1046_01")
            replace_char_head_texture(input("角色7位ID: "))

        if do_type == "23":
            print("支援卡ID, 例: 20002")
            replace_support_card_texture(input("支援卡ID: "), True)

        if do_type == "24":
            print("支援卡ID, 例: 20002")
            replace_support_thumb_texture(input("支援卡ID: "), True)

        if do_type == "25":
            file = f"{umaModelReplace.EDITED_TEXTURE_PATH}/support_card"
            for dirpath, dirnames, filenames in os.walk(file):
                for dirname in dirnames:
                    print(dirname)
                    replace_support_card_texture(dirname, False)
                    replace_support_thumb_texture(dirname, False)

        if do_type == "3":
            print("请输入人物技能6位数ID, 例: 100101、100102")
            uma.edit_cutin_skill(input("替换ID: "), input("目标ID: "))

        if do_type == "4":
            checkDo = input("注意: 目前部分胜利动作替换后会出现破音、黑屏等问题。\n"
                            "若您仍要更改, 请输入y继续: ")
            if checkDo not in ["y", "Y"]:
                continue
            print("请输入胜利动作6位数ID, 例: 100101、100102")
            uma.replace_race_result(input("替换ID: "), input("目标ID: "))
            print("替换完成")

        if do_type == "51":
            uma.unlock_live_dress()
            print("解锁完成")

        if do_type == "52":
            edit_live_id = input("Live id (通常为4位, 留空则全部修改): ").strip()
            uma.clear_live_blur(edit_live_id)
            # print("此功能搭配TLG插件的Live自由镜头功能，使用效果更佳\n"
            #       "This function is paired with the TLG plug-in's Live free camera for better use\n"
            #       "Repo: https://github.com/MinamiChiwa/Trainers-Legend-G")

        if do_type == "8":
            for dirpath, dirnames, filenames in os.walk(umaModelReplace.EDITED_PATH):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    if os.path.isfile(uma.get_bundle_path(filename)):
                        base = UnityPy.load(file_path)
                        name: str
                        for key, value in base.container.items():
                            name = get_bundle_name(key)
                            print(name)
                            shutil.copyfile(file_path, f"{umaModelReplace.MOD_PATH}/{filename}")
            print("开始安装")
            for dirpath, dirnames, filenames in os.walk(umaModelReplace.MOD_PATH):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    if os.path.isfile(uma.get_bundle_path(filename)):
                        shutil.copyfile(file_path, uma.get_bundle_path(filename))

        if do_type == "9":
            uma.file_restore()

        if do_type == "91":
            uma.file_delete()

        if do_type == "0":
            break

        input("Press enter to continue...\n")
