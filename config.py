from configparser import ConfigParser


def config_params(filename: str = "databasse.ini", section: str = "postgressql"):

    parser = ConfigParser()
    parser.read(filename)
    db = {}

    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
        return db
    else:
        raise Exception("Selection {0} is not found in the {1} file.".format(section, filename))
