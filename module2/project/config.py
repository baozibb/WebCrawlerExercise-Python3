import configparser


class Config():
    '''读取配置文件'''
    def __init__(self, file_name, section):
        cf = configparser.ConfigParser()
        cf.read(file_name)
        self._section = cf.items(section)

    @property
    def section(self):
        return self._section
