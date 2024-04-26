from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Paquete de Python RNMN'
LONG_DESCRIPTION = ('Paquete de Python para crear y usar '+
                    'una red neuronal multimodal que predice números enteros')
setup(
    name="RNMN",
    version=VERSION,
    author="Sergio Hidalgo",
    author_email="<sergio.hidalgo@estudiante.uam.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(where="./requirements.txt"),

    keywords=['python', 'RNMN'],
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Intended Audience :: Pablo Varona",
        "Programming Language :: Python :: 3",
        "Operating System :: Linux :: Ubuntu",
    ]

)
