from .backends.viper import Viper

def get_viper():
    return Viper

languages = {"viper": Viper}

def get_compiler(language):
    return languages[language] 