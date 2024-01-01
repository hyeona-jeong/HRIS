# -*- mode: python ; coding: utf-8 -*-
ui = [('login.ui', '.'),
       ('find.ui', '.'),
       ('index.ui', '.'),
       ('emp_list.ui', '.'),
       ('emp_info.ui', '.'),
       ('emp_regist.ui', '.'),
       ('edu_list.ui', '.'),
       ('change_pw.ui', '.'),
       ('add_edu.ui', '.'),
       ('add_img.ui', '.'),
       ('emp_edit.ui', '.'),
       ('sign_up.ui', '.'),
       ('search_post.ui', '.'),
       ('user_auth.ui', '.'),
       ('write.ui', '.'),
       ('read.ui', '.'),
       ('forum_list.ui', '.'),
       ('rc1.png', '.'),
       ('peo.png', '.'),
       ('logout.png', '.'),
       ('hr.png', '.'),
       ('edu.png', '.'),
       ('chgpw.png', '.'),
       ('diagram.png', '.'),
       ('find.png', '.'),
       ('nori_230.jpg', '.'),
       ('nori.png', '.'),
       ('nori.gif', '.'),
       ('unknown.png', '.'),
       ('busi1.png', '.'),
       ('windowicon.jpg', '.'),
       ('center.png', '.'),
       ('image.png', '.'),
       ('justify.png', '.'),
       ('left.png', '.'),
       ('right.png', '.'),
       ('unknown.png', '.')
]

a = Analysis(
    ['login.py'],
    pathex=[],
    binaries=[],
    datas=ui,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='login',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
