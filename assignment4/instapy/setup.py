from distutils.core import setup


setup(
    name="Python for instagram",
    version="1.0",
    packages=["instapy"],
    scripts=["instapy/grayscale_image.py",
             "instapy/sepia_image.py",
             "bin/instapy",
             ]
    )
