import UnityPy
import sqlite3
import os
import shutil
import typing as t
from PIL import Image
from . import assets_path

spath = os.path.split(__file__)[0]
BACKUP_PATH = f"{spath}/backup"
EDITED_PATH = f"{spath}/edited"

class UmaFileNotFoundError(FileNotFoundError):
    pass


class UmaReplace:
    def __init__(self):
        self.init_folders()
        profile_path = os.environ.get("UserProfile")
        self.base_path = f"{profile_path}/AppData/LocalLow/Cygames/umamusume"
        self.conn = sqlite3.connect(f"{self.base_path}/meta")

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

    @staticmethod
    def replace_file_path(fname: str, id1: str, id2: str, save_name: t.Optional[str] = None) -> str:
        env = UnityPy.load(fname)

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
        with open(save_name, "wb") as f:
            f.write(env.file.save())
        return save_name


    def replace_texture2d(self, bundle_name: str):
        edited_path = f"./editTexture/{bundle_name}"
        if not os.path.isdir(edited_path):
            raise UmaFileNotFoundError(f"path: {edited_path} not found. Please extract first.")

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

        save_name = f"{EDITED_PATH}/{os.path.split(bundle_name)[-1]}"
        with open(save_name, "wb") as f:
            f.write(env.file.save())
        return save_name


    def get_texture_in_bundle(self, bundle_name: str, src_names: t.List[str], force_replace=False):
        base_path = f"./editTexture/{bundle_name}"
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
                    if data.name in src_names:
                        img_data = data.read()
                        image: Image = img_data.image
                        image.save(f"{base_path}/{data.name}.png")
                        print(f"save {data.name} into {f'{base_path}/{data.name}.png'}")
        return True, base_path

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
            raise UmaFileNotFoundError(f"{path} not found!")

        cursor.close()
        return query[0]

    def save_char_body_texture(self, char_id: str, force_replace=False):
        mtl_bdy_path = assets_path.get_body_mtl_path(char_id)
        bundle_hash = self.get_bundle_hash(mtl_bdy_path, None)
        return self.get_texture_in_bundle(bundle_hash, assets_path.get_body_mtl_names(char_id), force_replace)

    def replace_char_body_texture(self, char_id: str):
        mtl_bdy_path = assets_path.get_body_mtl_path(char_id)
        bundle_hash = self.get_bundle_hash(mtl_bdy_path, None)
        self.file_backup(bundle_hash)
        edited_path = self.replace_texture2d(bundle_hash)
        # print("save", edited_path)
        shutil.copyfile(edited_path, self.get_bundle_path(bundle_hash))

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


# a = UmaReplace()
# a.file_backup("6NX7AYDRVFFGWKVGA4TDKUX2N63TRWRT")
# a.replace_file_path("5IU2HDJHXDO3ISZSXXOQWXF7VEOG5OCX", "1046", "")
# a.replace_body("1046_02", "1098_00")

# a.replace_head("1046_02", "1098_00")
# a.replace_tail("1046", "1037")
# a.file_restore()
