
def get_body_mtl_names(_id):
    return [
        f"tex_bdy{_id}_shad_c",
        f"tex_bdy{_id}_base",
        f"tex_bdy{_id}_ctrl",
        f"tex_bdy{_id}_diff"
    ]


def get_body_mtl_path(_id):
    return f"sourceresources/3d/chara/body/bdy{_id}/materials/mtl_bdy{_id}"


def get_body_path(_id):
    return [
        f"3d/chara/body/bdy{_id}/pfb_bdy{_id}",
        get_body_mtl_path(_id)
    ]


def get_head_path(_id):
    return [
        f"3d/chara/head/chr{_id}/pfb_chr{_id}",
        f"sourceresources/3d/chara/head/chr{_id}/materials/mtl_chr{_id}_cheek",
        f"sourceresources/3d/chara/head/chr{_id}/materials/mtl_chr{_id}_eye",
        f"sourceresources/3d/chara/head/chr{_id}/materials/mtl_chr{_id}_face",
        f"sourceresources/3d/chara/head/chr{_id}/materials/mtl_chr{_id}_hair",
        f"sourceresources/3d/chara/head/chr{_id}/materials/mtl_chr{_id}_mayu",
        f"sourceresources/3d/chara/head/chr{_id}/materials/mtl_chr{_id}_tear",
        f"sourceresources/3d/chara/head/chr{_id}/facial/ast_chr{_id}_ear_target"
    ]


def get_tail1_path(_id):
    return [
        f"3d/chara/tail/tail0001_00/textures/tex_tail0001_00_{_id[:4]}_diff",
        f"3d/chara/tail/tail0001_00/textures/tex_tail0001_00_{_id[:4]}_diff_wet",
        f"3d/chara/tail/tail0001_00/textures/tex_tail0001_00_{_id[:4]}_shad_c",
        f"3d/chara/tail/tail0001_00/textures/tex_tail0001_00_{_id[:4]}_shad_c_wet",
    ]

def get_tail2_path(_id):
    return [
        f"3d/chara/tail/tail0002_00/textures/tex_tail0002_00_{_id[:4]}_diff",
        f"3d/chara/tail/tail0002_00/textures/tex_tail0002_00_{_id[:4]}_diff_wet",
        f"3d/chara/tail/tail0002_00/textures/tex_tail0002_00_{_id[:4]}_shad_c",
        f"3d/chara/tail/tail0002_00/textures/tex_tail0002_00_{_id[:4]}_shad_c_wet"
    ]
