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


def get_gac_chr_start_path(type):
    return f"cutt/cutin/skill/gac_chr_start_{type}/gac_chr_start_{type}"


def get_cutin_skill_path(_id):
    return f"cutt/cutin/skill/crd{_id}_001/crd{_id}_001"


def get_race_result_path(_id):
    return get_chr_race_result_path(_id) + get_crd_race_result_path(_id)


def get_chr_race_result_path(_id):
    return [
        f"cutt/cutin/raceresult/res_chr{_id[:4]}_001/res_chr{_id[:4]}_001",
        f"3d/motion/raceresult/body/chara/chr{_id[:4]}_00/anm_res_chr{_id[:4]}_001",
        f"3d/motion/raceresult/camera/chara/chr{_id[:4]}_00/anm_res_chr{_id[:4]}_001_cam",
        f"3d/motion/raceresult/facial/chara/chr{_id[:4]}_00/anm_res_chr{_id[:4]}_001_ear",
        f"3d/motion/raceresult/facial/chara/chr{_id[:4]}_00/anm_res_chr{_id[:4]}_001_ear_driven",
        f"3d/motion/raceresult/facial/chara/chr{_id[:4]}_00/anm_res_chr{_id[:4]}_001_face",
        f"3d/motion/raceresult/facial/chara/chr{_id[:4]}_00/anm_res_chr{_id[:4]}_001_face_driven"
    ]


def get_crd_race_result_path(_id):
    return [
        f"cutt/cutin/raceresult/res_crd{_id}_001/res_crd{_id}_001",
        f"3d/motion/raceresult/body/chara/chr{_id[:4]}_00/anm_res_crd{_id}_001",
        f"3d/motion/raceresult/camera/chara/chr{_id[:4]}_00/anm_res_crd{_id}_001_cam",
        f"3d/motion/raceresult/facial/chara/chr{_id[:4]}_00/anm_res_crd{_id}_001_ear",
        f"3d/motion/raceresult/facial/chara/chr{_id[:4]}_00/anm_res_crd{_id}_001_ear_driven",
        f"3d/motion/raceresult/facial/chara/chr{_id[:4]}_00/anm_res_crd{_id}_001_face",
        f"3d/motion/raceresult/facial/chara/chr{_id[:4]}_00/anm_res_crd{_id}_001_face_driven",
        f"sound/v/snd_voi_race_{_id}.acb",
        f"sound/v/snd_voi_race_{_id}.awb"
    ]


def get_head_mtl_path(_id):
    return [
        f"sourceresources/3d/chara/head/chr{_id}/materials/mtl_chr{_id}_face",
        f"sourceresources/3d/chara/head/chr{_id}/materials/mtl_chr{_id}_hair"
    ]
