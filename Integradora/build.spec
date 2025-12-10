# build.spec
block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('base_datos', 'base_datos'),
        ('controller', 'controller'),
        ('model', 'model'),
        ('view', 'view'),
        ('configuracion.py', '.'),
    ],
    hiddenimports=[
        'customtkinter',
        'mysql.connector',
        'PIL',  # Si usas imágenes en customtkinter
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='NutriSystem',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Cambia a True si quieres ver la consola
    icon=None,  # Agrega ruta a un icono .ico si quieres
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None
)