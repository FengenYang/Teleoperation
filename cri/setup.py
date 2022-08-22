# -*- coding: utf-8 -*-
"""Setup file for Common Robot Interface.
"""

from setuptools import setup

with open("README.md", "r",errors="ignore") as f:
    long_description = f.read()

setup(
    name="cri",
    version="0.1.0",
    description="Common Robot Interface",
    license="GPLv3",
    long_description=long_description,
    author="John Lloyd",
    author_email="jlloyd237@gmail.com",
    url="https://github.com/jlloyd237/cri/",
    packages=["cri", "cri.abb", "cri.ur", "cri.ur.rtde", "cri.dobot", "cri.dobot.mg400", "cri.dobot.mg400_dll", "cri.dobot.magician"],
	package_data={'cri.ur': ['rtde_config.xml'],
            "cri.dobot.mg400_dll": ['Dobot.dll',"libgcc_s_seh-1.dll","libstdc++-6.dll","libwinpthread-1.dll","Qt5Core.dll","Qt5Network.dll","Qt5SerialPort.dll"],
            "cri.dobot.magician": ['DobotDll.dll',"msvcp120.dll","msvcr120.dll","Qt5Core.dll","Qt5Network.dll","Qt5SerialPort.dll"]},
    install_requires=["numpy", "transforms3d"]
)
