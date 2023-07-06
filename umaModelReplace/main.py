import UnityPy
import sqlite3
import os
import shutil
import typing as t
from PIL import Image
from . import assets_path
from tkinter import filedialog

spath = os.path.split(__file__)[0]
BACKUP_PATH = f"{spath}/backup"
EDITED_PATH = f"{spath}/edited"


class UmaFileNotFoundError(FileNotFoundError):
    pass


class UmaReplace:
    def __init__(self):
        self.init_folders()
        profile_path = os.environ.get("UserProfile")
        #        self.base_path = f"{profile_path}/AppData/LocalLow/Cygames/umamusume"
        self.base_path = filedialog.askdirectory(title='选择同时包含dat文件夹,meta文件的文件夹',
                                                 initialdir=f"{profile_path}/AppData/LocalLow/Cygames/umamusume")  # 选择同时包含dat文件夹,meta文件的文件夹
        self.conn = sqlite3.connect(f"{self.base_path}/meta")
        self.master_conn = sqlite3.connect(f"{self.base_path}/master/master.mdb")

    @staticmethod
    def init_folders():
        if not os.path.isdir(BACKUP_PATH):
            os.makedirs(BACKUP_PATH)
        if not os.path.isdir(EDITED_PATH):
            os.makedirs(EDITED_PATH)

    def get_bundle_path(self, bundle_hash: str):
        return f"{self.base_path}/dat/{bundle_hash[:2]}/{bundle_hash}"

    def file_backup(self, bundle_hash: str):
        if not os.path.isfile(f"{BACKUP_PATH}/{bundle_hash}"):
            shutil.copyfile(f"{self.get_bundle_path(bundle_hash)}", f"{BACKUP_PATH}/{bundle_hash}")

    def file_restore(self, hashs: t.Optional[t.List[str]] = None):
        """
        恢复备份
        :param hashs: bundle hash 列表, 若为 None, 则恢复备份文件夹内所有文件
        """
        if not hashs:
            hashs = os.listdir(BACKUP_PATH)
        if not isinstance(hashs, list):
            raise TypeError(f"hashs must be a list, not {type(hashs)}")

        for i in hashs:
            fpath = f"{BACKUP_PATH}/{i}"
            if os.path.isfile(fpath):
                shutil.copyfile(fpath, self.get_bundle_path(i))
                print(f"restore {i}")
        print("已还原修改")

    def file_delete(self):
        do_delete = input("即将清理 backup,edited 文件夹,输入 \"Y\" 确认: ")
        if do_delete in ["Y", "y"]:
            do_restore = input("输入 \"Y\" 在清理前复原所有修改: ")
            if do_restore in ["Y", "y"]:
                self.file_restore()
            shutil.rmtree(BACKUP_PATH)
            shutil.rmtree(EDITED_PATH)
            self.init_folders()
            print("已清理")
        else:
            print("取消清理")

    @staticmethod
    def replace_file_path(fname: str, id1: str, id2: str, save_name: t.Optional[str] = None) -> str:
        env = UnityPy.load(fname)

        data = None

        for obj in env.objects:
            if obj.type.name not in ["Avatar"]:
                data = obj.read()
                if hasattr(data, "name"):
                    if id1 in data.name:
                        # print(obj.type.name, data.name)
                        if obj.type.name == "MonoBehaviour":
                            raw = bytes(data.raw_data)
                            raw = raw.replace(id1.encode("utf8"), id2.encode("utf8"))
                            data.set_raw_data(raw)
                            data.save(raw_data=raw)
                        else:
                            raw = bytes(data.get_raw_data())
                            raw = raw.replace(id1.encode("utf8"), id2.encode("utf8"))
                            data.set_raw_data(raw)
                            data.save()

                        # if obj.type.name == "Texture2D":
                        #     mono_tree = obj.read_typetree()
                        #     if "m_Name" in mono_tree:
                        #         mono_tree["m_Name"] = mono_tree["m_Name"].replace(id1, id2)
                        #         obj.save_typetree(mono_tree)

                # mono_tree = obj.read_typetree()
                # if "m_Name" in mono_tree:
                #     mono_tree["m_Name"] = mono_tree["m_Name"].replace(id1, id2)
                #     obj.save_typetree(mono_tree)

        if save_name is None:
            save_name = f"{EDITED_PATH}/{os.path.split(fname)[-1]}"
        if data is None:
            with open(fname, "rb") as f:
                data = f.read()
                data = data.replace(id1.encode("utf8"), id2.encode("utf8"))
            with open(save_name, "wb") as f:
                f.write(data)
        else:
            with open(save_name, "wb") as f:
                f.write(env.file.save())
        return save_name

    def replace_texture2d(self, bundle_name: str, edited_path: t.Optional[str] = None):
        edited_path = f"./editTexture/{bundle_name}" if edited_path is not None else edited_path
        save_name = f"{EDITED_PATH}/{os.path.split(bundle_name)[-1]}"
        if not os.path.isdir(edited_path):
            raise UmaFileNotFoundError(f"path: {edited_path} not found. Please extract first.")
        if os.path.exists(self.get_bundle_path(bundle_name)):
            file_names = os.listdir(edited_path)
            env = UnityPy.load(self.get_bundle_path(bundle_name))
            for obj in env.objects:
                if obj.type.name == "Texture2D":
                    data = obj.read()
                    if hasattr(data, "name"):
                        if f"{data.name}.png" in file_names:
                            img_data = data.read()
                            img_data.image = Image.open(f"{edited_path}/{data.name}.png")
                            data.save()

            with open(save_name, "wb") as f:
                f.write(env.file.save())

        return save_name

    def get_texture_in_bundle(self, bundle_name: str, src_names: t.Optional[t.List[str]], force_replace=False,
                              base_path: t.Optional[str] = None):
        base_path = f"./editTexture/{bundle_name}" if base_path is None else base_path
        if not os.path.isdir(base_path):
            os.makedirs(base_path)

        if not force_replace:
            if len(os.listdir(base_path)) > 0:
                return False, base_path

        env = UnityPy.load(self.get_bundle_path(bundle_name))
        for obj in env.objects:
            if obj.type.name == "Texture2D":
                data = obj.read()
                if hasattr(data, "name"):
                    if src_names is None or (data.name in src_names):
                        img_data = data.read()
                        image: Image = img_data.image
                        image.save(f"{base_path}/{data.name}.png")
                        print(f"save {data.name} into {f'{base_path}/{data.name}.png'}")
        return True, base_path

    def get_support_card_texture_in_bundle(self, card_id: str, bundle_name: str, src_names: t.Optional[t.List[str]],
                                           force_replace=False):
        return self.get_texture_in_bundle(bundle_name, src_names, force_replace,
                                          f"./editTexture/support_card/{card_id}")

    def get_bundle_hash(self, path: str, query_orig_id: t.Optional[str]) -> str:
        cursor = self.conn.cursor()
        query = cursor.execute("SELECT h FROM a WHERE n=?", [path]).fetchone()
        if query is None:
            if (query_orig_id is not None) and ("_" in query_orig_id):
                query_id, query_sub_id = query_orig_id.split("_")

                if query is None:
                    new_path = path.replace(query_orig_id, f"{query_id}_%")
                    query = cursor.execute("SELECT h, n FROM a WHERE n LIKE ?", [new_path]).fetchone()
                    if query is not None:
                        print(f"{path} not found, but found {query[1]}")

        if query is None:
            print(UmaFileNotFoundError(f"{path} not found!"))
            query = []
            return query
        cursor.close()
        return query[0]

    def save_char_body_texture(self, char_id: str, force_replace=False):
        mtl_bdy_path = assets_path.get_body_mtl_path(char_id)
        bundle_hash = self.get_bundle_hash(mtl_bdy_path, None)
        return self.get_texture_in_bundle(bundle_hash, assets_path.get_body_mtl_names(char_id), force_replace)

    def save_char_head_texture(self, char_id: str, force_replace=False, on_index=-1):
        ret = []
        for n, i in enumerate(assets_path.get_head_mtl_path(char_id)):
            if on_index != -1:
                if n != on_index:
                    continue
            bundle_hash = self.get_bundle_hash(i, None)
            ret.append(self.get_texture_in_bundle(bundle_hash, None, force_replace))
        return ret

    def replace_char_body_texture(self, char_id: str):
        mtl_bdy_path = assets_path.get_body_mtl_path(char_id)
        bundle_hash = self.get_bundle_hash(mtl_bdy_path, None)
        self.file_backup(bundle_hash)
        edited_path = self.replace_texture2d(bundle_hash)
        # print("save", edited_path)
        shutil.copyfile(edited_path, self.get_bundle_path(bundle_hash))

    def replace_char_head_texture(self, char_id: str):
        for mtl_bdy_path in assets_path.get_head_mtl_path(char_id):
            bundle_hash = self.get_bundle_hash(mtl_bdy_path, None)
            self.file_backup(bundle_hash)
            edited_path = self.replace_texture2d(bundle_hash)
            # print("save", edited_path)
            shutil.copyfile(edited_path, self.get_bundle_path(bundle_hash))

    def save_support_card_texture(self, card_id: str, force_replace=False, on_index=-1):
        ret = []
        for n, i in enumerate(assets_path.get_support_card_path(card_id)):
            if on_index != -1:
                if n != on_index:
                    continue
            bundle_hash = self.get_bundle_hash(i, None)
            ret.append(self.get_support_card_texture_in_bundle(card_id, bundle_hash, None, force_replace))
        return ret

    def replace_support_card_texture(self, card_id: str):
        for support_card_path in assets_path.get_support_card_path(card_id):
            bundle_hash = self.get_bundle_hash(support_card_path, None)
            if bundle_hash:
                self.file_backup(bundle_hash)
                edited_path = self.replace_texture2d(bundle_hash, f"./editTexture/support_card/{card_id}")
                # print("save", edited_path)
                shutil.copyfile(edited_path, self.get_bundle_path(bundle_hash))
                print("贴图已修改")

    def save_support_thumb_texture(self, card_id: str, force_replace=False, on_index=-1):
        ret = []
        for n, i in enumerate(assets_path.get_support_thumb_path(card_id)):
            if on_index != -1:
                if n != on_index:
                    continue
            bundle_hash = self.get_bundle_hash(i, None)
            ret.append(self.get_support_card_texture_in_bundle(card_id, bundle_hash, None, force_replace))
        return ret

    def replace_support_thumb_texture(self, card_id: str):
        for support_thumb_path in assets_path.get_support_thumb_path(card_id):
            bundle_hash = self.get_bundle_hash(support_thumb_path, None)
            if bundle_hash:
                self.file_backup(bundle_hash)
                edited_path = self.replace_texture2d(bundle_hash, f"./editTexture/support_card/{card_id}")
                # print("save", edited_path)
                shutil.copyfile(edited_path, self.get_bundle_path(bundle_hash))
                print("贴图已修改")

    def replace_file_ids(self, orig_path: str, new_path: str, id_orig: str, id_new: str):
        orig_hash = self.get_bundle_hash(orig_path, id_orig)
        new_hash = self.get_bundle_hash(new_path, id_new)
        self.file_backup(orig_hash)
        edt_bundle_file_path = self.replace_file_path(self.get_bundle_path(new_hash), id_new, id_orig,
                                                      f"{EDITED_PATH}/{orig_hash}")
        shutil.copyfile(edt_bundle_file_path, self.get_bundle_path(orig_hash))

    def replace_body(self, id_orig: str, id_new: str):
        """
        替换身体
        :param id_orig: 原id, 例: 1046_01
        :param id_new: 新id
        """
        orig_paths = assets_path.get_body_path(id_orig)
        new_paths = assets_path.get_body_path(id_new)
        for i in range(len(orig_paths)):
            try:
                self.replace_file_ids(orig_paths[i], new_paths[i], id_orig, id_new)
            except UmaFileNotFoundError as e:
                print(e)

    def replace_head(self, id_orig: str, id_new: str):
        """
        替换头部
        :param id_orig: 原id, 例: 1046_01
        :param id_new: 新id
        """
        orig_paths = assets_path.get_head_path(id_orig)
        new_paths = assets_path.get_head_path(id_new)
        for i in range(len(orig_paths)):
            try:
                self.replace_file_ids(orig_paths[i], new_paths[i], id_orig, id_new)
            except UmaFileNotFoundError as e:
                print(e)

    def replace_tail(self, id_orig: str, id_new: str):  # 目前无法跨模型更换尾巴, 更换目标不能和原马娘同时出场。
        """
        替换尾巴
        :param id_orig: 原id, 例: 1046
        :param id_new: 新id
        """

        def check_vaild_path(paths: list):
            try:
                self.get_bundle_hash(paths[0], None)
            except UmaFileNotFoundError:
                return False
            return True

        orig_paths1 = assets_path.get_tail1_path(id_orig)
        orig_paths2 = assets_path.get_tail2_path(id_orig)

        new_paths1 = assets_path.get_tail1_path(id_new)
        new_paths2 = assets_path.get_tail2_path(id_new)

        orig_paths = None
        new_paths = None
        use_id1 = -1
        use_id2 = -1
        if check_vaild_path(orig_paths1):
            orig_paths = orig_paths1
            use_id1 = 1
        if check_vaild_path(orig_paths2):
            orig_paths = orig_paths2
            use_id1 = 2
        if check_vaild_path(new_paths1):
            new_paths = new_paths1
            use_id2 = 1
        if check_vaild_path(new_paths2):
            use_id2 = 2
            new_paths = new_paths2

        if (orig_paths is None) or (new_paths is None):
            print("tail not found")
            return

        if use_id1 != use_id2:
            print(f"{id_orig} 模型编号: {use_id1}, {id_new} 模型编号: {use_id2}, 目前无法跨模型修改尾巴。")
            return
        print("注意, 更换尾巴后, 更换目标不能和原马娘同时出场。")
        for i in range(len(orig_paths)):
            try:
                self.replace_file_ids(orig_paths[i], new_paths[i], id_orig, id_new)
            except UmaFileNotFoundError as e:
                print(e)

    def edit_gac_chr_start(self, dress_id: str, res_type: str):
        """
        替换开门人物
        :param dress_id: 目标开门id, 例: 100101
        :param res_type: 001骏川手纲，002秋川弥生
        """

        def edit_chr(orig_hash: str, dress_id: str):
            env = UnityPy.load(self.get_bundle_path(orig_hash))
            for obj in env.objects:
                if obj.type.name == "MonoBehaviour":
                    if obj.serialized_type.nodes:
                        tree = obj.read_typetree()
                        if "runtime_gac_chr_start_00" in tree["m_Name"]:
                            tree["_characterList"][0]["_characterKeys"]["_selectCharaId"] = int(dress_id[:-2])
                            tree["_characterList"][0]["_characterKeys"]["_selectClothId"] = int(dress_id)
                            obj.save_typetree(tree)
            with open(f"{EDITED_PATH}/{orig_hash}", "wb") as f:
                f.write(env.file.save())

        path = assets_path.get_gac_chr_start_path(res_type)
        orig_hash = self.get_bundle_hash(path, None)
        self.file_backup(orig_hash)
        edit_chr(orig_hash, dress_id)
        shutil.copyfile(f"{EDITED_PATH}/{orig_hash}", self.get_bundle_path(orig_hash))

    def edit_cutin_skill(self, id_orig: str, id_target: str):
        """
        替换技能
        :param id_orig: 原id, 例: 100101
        :param id_target: 新id
        """
        target_path = assets_path.get_cutin_skill_path(id_target)
        target_hash = self.get_bundle_hash(target_path, None)
        target = UnityPy.load(self.get_bundle_path(target_hash))

        target_tree = None
        target_clothe_id = None
        target_cy_spring_name_list = None

        for obj in target.objects:
            if obj.type.name == "MonoBehaviour":
                if obj.serialized_type.nodes:
                    tree = obj.read_typetree()
                    if "runtime_crd1" in tree["m_Name"]:
                        target_tree = tree
                        for character in tree["_characterList"]:
                            target_clothe_id = str(character["_characterKeys"]["_selectClothId"])

        if target_tree is None:
            print("目标无法解析")
            return

        for character in target_tree["_characterList"]:
            for targetList in character["_characterKeys"]["thisList"]:
                if len(targetList["_enableCySpringList"]) > 0:
                    target_cy_spring_name_list = targetList["_targetCySpringNameList"]

        orig_path = assets_path.get_cutin_skill_path(id_orig)
        orig_hash = self.get_bundle_hash(orig_path, None)
        self.file_backup(orig_hash)
        env = UnityPy.load(self.get_bundle_path(orig_hash))

        for obj in env.objects:
            if obj.type.name == "MonoBehaviour":
                if obj.serialized_type.nodes:
                    tree = obj.read_typetree()
                    if "runtime_crd1" in tree["m_Name"]:
                        for character in tree["_characterList"]:
                            character["_characterKeys"]["_selectCharaId"] = int(target_clothe_id[:-2])
                            character["_characterKeys"]["_selectClothId"] = int(target_clothe_id)
                            character["_characterKeys"]["_selectHeadId"] = 0
                            for outputList in character["_characterKeys"]["thisList"]:
                                if len(outputList["_enableCySpringList"]) > 0:
                                    outputList["_enableCySpringList"] = [1] * len(target_cy_spring_name_list)
                                    outputList["_targetCySpringNameList"] = target_cy_spring_name_list
                        obj.save_typetree(tree)

        with open(f"{EDITED_PATH}/{orig_hash}", "wb") as f:
            f.write(env.file.save())
        shutil.copyfile(f"{EDITED_PATH}/{orig_hash}", self.get_bundle_path(orig_hash))
        print("替换完成")

    def replace_race_result(self, id_orig: str, id_new: str):
        """
        替换G1胜利动作
        :param id_orig: 原id, 例: 100101
        :param id_new: 新id
        """
        orig_paths = assets_path.get_crd_race_result_path(id_orig)
        new_paths = assets_path.get_crd_race_result_path(id_new)
        for i in range(len(orig_paths)):
            try:
                self.replace_file_ids(orig_paths[i], new_paths[i], id_orig, id_new)
            except UmaFileNotFoundError as e:
                print(e)

    def unlock_live_dress(self):

        def dict_factory(cursor, row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d

        def get_all_dress_in_table():
            self.master_conn.row_factory = dict_factory
            cursor = self.master_conn.cursor()
            cursor.execute("SELECT * FROM dress_data")
            # fetchall as result
            query = cursor.fetchall()
            # close connection
            cursor.close()
            return query

        def get_unique_in_table():
            self.conn.row_factory = dict_factory
            cursor = self.conn.cursor()
            cursor.execute("SELECT n FROM a WHERE n like '%pfb_chr1____90'")
            # fetchall as result
            names = cursor.fetchall()
            # close connection
            cursor.close()
            lst = []
            for name in names:
                lst.append(name["n"][-7:-3])
            return lst

        def create_data(dress, unique):
            dress['id'] = dress['id'] + 89
            dress['body_type_sub'] = 90
            if str(dress['id'])[:-2] in set(unique):
                dress['head_sub_id'] = 90
            else:
                dress['head_sub_id'] = 0
            self.master_conn.row_factory = dict_factory
            cursor = self.master_conn.cursor()
            cursor.execute("INSERT INTO dress_data VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                           [dress['id'], dress['condition_type'], dress['have_mini'], dress['general_purpose'],
                            dress['costume_type'], dress['chara_id'], dress['use_gender'], dress['body_shape'],
                            dress['body_type'], dress['body_type_sub'], dress['body_setting'], dress['use_race'],
                            dress['use_live'], dress['use_live_theater'], dress['use_home'], dress['use_dress_change'],
                            dress['is_wet'], dress['is_dirt'], dress['head_sub_id'], dress['use_season'],
                            dress['dress_color_main'], dress['dress_color_sub'], dress['color_num'],
                            dress['disp_order'],
                            dress['tail_model_id'], dress['tail_model_sub_id'], dress['start_time'], dress['end_time']])
            self.master_conn.commit()
            cursor.close()

        def unlock_data():
            self.master_conn.row_factory = dict_factory
            cursor = self.master_conn.cursor()
            cursor.execute("UPDATE dress_data SET use_live = 1, use_live_theater = 1")
            self.master_conn.commit()
            cursor.close()

        dresses = get_all_dress_in_table()
        unique = get_unique_in_table()
        for dress in dresses:
            if 100000 < dress['id'] < 200000 and str(dress['id']).endswith('01'):
                create_data(dress, unique)
        unlock_data()

    def clear_live_blur(self, edit_id: str):
        cursor = self.conn.cursor()
        query = cursor.execute("SELECT h, n FROM a WHERE n LIKE 'cutt/cutt_son%/son%_camera'").fetchall()
        bundle_names = [i[0] for i in query]
        path_names = [i[1] for i in query]
        cursor.close()
        target_path = f"cutt/cutt_son{edit_id}/son{edit_id}_camera" if edit_id != "" else None
        tLen = len(bundle_names)

        for n, bn in enumerate(bundle_names):
            path_name = path_names[n]
            if target_path is not None:
                if path_name != target_path:
                    continue
            print(f"Editing: {path_name} ({n + 1}/{tLen})")
            try:
                bundle_path = self.get_bundle_path(bn)
                if not os.path.isfile(bundle_path):
                    print(f"File not found: {bundle_path}")
                    continue
                env = UnityPy.load(bundle_path)
                for obj in env.objects:
                    if obj.type.name == "MonoBehaviour":
                        if not obj.serialized_type.nodes:
                            continue
                        tree = obj.read_typetree()

                        tree['postEffectDOFKeys']['thisList'] = [tree['postEffectDOFKeys']['thisList'][0]]
                        dof_set_data = {
                            "frame": 0,
                            "attribute": 327680,
                            "interpolateType": 0,
                            "curve": {
                                "m_Curve": [],
                                "m_PreInfinity": 2,
                                "m_PostInfinity": 2,
                                "m_RotationOrder": 4
                            },
                            "easingType": 0,
                            "forcalSize": 30.0,
                            "blurSpread": 20.0,
                            "charactor": 1,
                            "dofBlurType": 3,
                            "dofQuality": 1,
                            "dofForegroundSize": 0.0,
                            "dofFgBlurSpread": 1.0,
                            "dofFocalPoint": 1.0,
                            "dofSmoothness": 1.0,
                            "BallBlurPowerFactor": 0.0,
                            "BallBlurBrightnessThreshhold": 0.0,
                            "BallBlurBrightnessIntensity": 1.0,
                            "BallBlurSpread": 0.0
                        }
                        for k in dof_set_data:
                            tree['postEffectDOFKeys']['thisList'][0][k] = dof_set_data[k]

                        tree['postEffectBloomDiffusionKeys']['thisList'] = []
                        tree['radialBlurKeys']['thisList'] = []

                        obj.save_typetree(tree)

                self.file_backup(bn)
                with open(bundle_path, 'wb') as f:
                    f.write(env.file.save())

            except Exception as e:
                print(f"Exception occurred when editing file: {bn}\n{e}")

        print("done.")

# a = UmaReplace()
# a.file_backup("6NX7AYDRVFFGWKVGA4TDKUX2N63TRWRT")
# a.replace_file_path("5IU2HDJHXDO3ISZSXXOQWXF7VEOG5OCX", "1046", "")
# a.replace_body("1046_02", "1098_00")

# a.replace_head("1046_02", "1098_00")
# a.replace_tail("1046", "1037")
# a.file_restore()
