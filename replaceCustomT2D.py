import umaModelReplace
import shutil

uma = umaModelReplace.UmaReplace()


def getAndReplaceTexture2D(bundle_hash, src_names):
    is_not_exist, msg = uma.get_texture_in_bundle(bundle_hash, src_names)
    if not is_not_exist:
        print(f"解包资源已存在: {msg}")
        do_replace = input("输入 \"Y\" 覆盖已解包资源, 输入其它内容跳过导出: ")
        if do_replace in ["Y", "y"]:
            _, msg = uma.get_texture_in_bundle(bundle_hash, src_names, True)

    print(f"已尝试导出资源, 请查看目录: {msg}")
    do_fin = input("请进行文件修改/替换, 修改完成后请输入 \"Y\" 打包并替换游戏文件。\n"
                   "若您不想立刻修改, 可以输入其它任意内容退出, 您可以在下次替换时选择\"跳过导出\"\n"
                   "请输入: ")
    if do_fin.strip() in ["Y", "y"]:
        uma.file_backup(bundle_hash)
        edited_path = uma.replace_texture2d(bundle_hash)
        shutil.copyfile(edited_path, uma.get_bundle_path(bundle_hash))
        print("贴图已修改")


# getAndReplaceTexture2D("EUI2AY3HRHIRXFCU5ZUTQRQKS4IJGBF5", ["tex_env_cutin1019_40_00_base01"])  # 数码固有"尊"
# getAndReplaceTexture2D("L6XWAMB2FBPJK32AEWJUMUDB47BJQROC", ["tex_chr_prop1259_00_diff"])  # 数码固有 玩偶
getAndReplaceTexture2D("KM6Z67WZ5C6XUQZBLXJ237TBVVVAGFCS", ["tex_chr_prop1003_06_diff"])  # 杂志封面
