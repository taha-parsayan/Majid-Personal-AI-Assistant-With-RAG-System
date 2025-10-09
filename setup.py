from setuptools import setup
import glob, os, shutil

APP = ['main.py']

lib_path = '/opt/miniconda3/envs/majid/lib/'
dest_path = 'dist/Majid.app/Contents/Frameworks/'
os.makedirs(dest_path, exist_ok=True)

for lib in ['libssl.3.dylib', 'libcrypto.3.dylib']:
    src = os.path.join(lib_path, lib)
    dst = os.path.join(dest_path, lib)
    if os.path.exists(src) and not os.path.exists(dst):
        shutil.copy(src, dst)

src = '/opt/miniconda3/envs/majid/lib/libsqlite3.dylib'
dst = '/opt/miniconda3/envs/majid/lib/libsqlite3.0.dylib'
if os.path.exists(src) and not os.path.exists(dst):
    shutil.copy(src, dst)

DATA_FILES = [
    'rump.py',
    'chatbox_WEB.py',
    'enter_api_WEB.py',
    'langchain_functions.py',
    ('icons', glob.glob('icons/*')),
    '/opt/miniconda3/envs/majid/lib/libsqlite3.dylib',
    ('charset_normalizer', glob.glob('/opt/miniconda3/envs/majid/lib/python3.12/site-packages/charset_normalizer/md__mypyc*.so')),
    ('parsedatetime/pdt_locales', glob.glob('/opt/miniconda3/envs/majid/lib/python3.12/site-packages/parsedatetime/pdt_locales/*')),
]

OPTIONS = {
    "excludes": [
        "setuptools",
        "zmq",
        "jupyter",
        "pypdfium2",
        "pypdfium2_raw"
    ],
    'includes': [
        'tiktoken_ext.openai_public',
        'tiktoken_ext',
        'langchain_community.document_loaders.pdf_plumber',
        'langchain_community.document_loaders.pdf',
        'pdfplumber',
        'pdfminer',
        'pdfminer.six',
        'charset_normalizer',
    ],
    'argv_emulation': True,
    'plist': {
        'CFBundleName': 'Majid',
        'CFBundleDisplayName': 'Majid',
        'CFBundleIconFile': 'icons/App_icon.icns'
    },
    'packages': [
'flask',
        'parsedatetime',
        'parsedatetime.pdt_locales',
        'charset_normalizer',
        'pdfplumber',
        'pdfminer'
    ],
    'frameworks': [
        '/opt/miniconda3/envs/majid/lib/libffi.8.dylib',
        '/opt/miniconda3/envs/majid/lib/libssl.3.dylib',
        '/opt/miniconda3/envs/majid/lib/libcrypto.3.dylib',
        '/opt/miniconda3/envs/majid/lib/libsqlite3.0.dylib'
    ],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
