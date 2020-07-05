# -*- mode: python -*-

block_cipher = None


a = Analysis(['L:\\SCRIPT\\Colour\\OCIO_converter\\script\\github\\OCIO_Converter\\src\\main\\python\\main.py'],
             pathex=['L:\\SCRIPT\\Colour\\OCIO_converter\\script\\github\\OCIO_Converter\\target\\PyInstaller'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=['l:\\script\\colour\\ocio_converter\\script\\venv_converter\\lib\\site-packages\\fbs\\freeze\\hooks'],
             runtime_hooks=['L:\\SCRIPT\\Colour\\OCIO_converter\\script\\github\\OCIO_Converter\\target\\PyInstaller\\fbs_pyinstaller_hook.py'],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Colorspace_converter',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=False , icon='L:\\SCRIPT\\Colour\\OCIO_converter\\script\\github\\OCIO_Converter\\src\\main\\icons\\Icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='Colorspace_converter')
