import subprocess
from enum import Enum

'''
enum define
'''


class Cmd_Type(Enum):
    GIMP = 1
    GEGL = 2


'''
TODO package config
'''
RUNNABLE_SHELL = '/bin/zsh'
GIMP_EXECUTE = '/Applications/GIMP-2.10.app/Contents/MacOS/GIMP'
GEGL_EXECUTE = '/usr/local/bin/gegl'


def SetEnvConf(shell, gimp_bin, gegl_bin):
    global RUNNABLE_SHELL, GIMP_EXECUTE, GEGL_EXECUTE
    RUNNABLE_SHELL = shell
    GIMP_EXECUTE = gimp_bin
    GEGL_EXECUTE = gegl_bin


'''
TODO index
'''
CMD_GIMP_COLOR_BALANCE = 0x0001

CMD_GEGL_COLOR_TEMP = 0x1001
CMD_GEGL_SATURATION = 0x1002

'''
Abstract Command
GimpCommand: invoke through `gimp` command by `python-fu-eval` interpreter
GeglCommand: invoke through `gegl` command
'''


class Command():
    def __init__(self):
        self.infile = ""
        self.outfile = ""

    def setIOFile(self, infile, outfile):
        self.infile = infile
        self.outfile = outfile


class GimpCommand(Command):
    def __init__(self):
        super(GimpCommand, self).__init__()
        self.cmd_type = Cmd_Type.GIMP
        self.cmd_str = ""
        self.exec_template = GIMP_EXECUTE + ' --no-interface ' + ' --no-data ' + ' --no-fonts ' + '--batch-interpreter python-fu-eval -b "{}" -b "pdb.gimp_quit(1)"'

    def execute(self):
        assert self.infile != ""
        assert self.outfile != ""
        self.exec_str = self.exec_template.format(self.cmd_str)
        print("self.exec_str", self.exec_str)

        result = subprocess.call(self.exec_str, shell=True)
        print("result", result)
        return result
        # shSplits = shlex.split(self.exec_str)
        # print("shSplits", shSplits)
        # result = subprocess.run(shSplits, shell=True, executable=RUNNABLE_SHELL)
        # print("result.stdout" , result.stdout)


class GeglCommand(Command):
    def __init__(self):
        super(GeglCommand, self).__init__()
        # infile outfile command + parameters
        self.cmd_type = Cmd_Type.GEGL
        self.exec_template = GEGL_EXECUTE + " {} -o {} -- {}"

    def fill(self, opr_str):
        assert self.infile != ""
        assert self.outfile != ""
        self.exec_str = self.exec_template.format(self.infile, self.outfile, opr_str)

    def execute(self):
        print(self.exec_str)
        result = subprocess.call(self.exec_str, shell=True)
        print("result", result)
        return result


'''
gimp commands
'''

'''
transfer_mode     INT32 Transfer mode { TRANSFER-SHADOWS (0), TRANSFER-MIDTONES (1), TRANSFER-HIGHLIGHTS (2) }
preserve_lum      INT32 Preserve luminosity values at each pixel (TRUE or FALSE)
cyan_red          FLOAT Cyan-Red color balance (-100 <= cyan-red <= 100)
magenta_green     FLOAT Magenta-Green color balance (-100 <= magenta-green <= 100)
yellow_blue       FLOAT Yellow-Blue color balance (-100 <= yellow-blue <= 100)
'''


class Cmd_gimp_color_balance(GimpCommand):

    def __init__(self, preserve_lum=True, cyan_red=0, magenta_green=0, yellow_blue=0):
        super(Cmd_gimp_color_balance, self).__init__()
        self.template = "filePath = '{}';outputFile = '{}'; imgIns = pdb.gimp_file_load(filePath, filePath, run_mode=1);imgInsDrawable = pdb.gimp_image_get_active_drawable(imgIns);pdb.gimp_drawable_color_balance(imgInsDrawable, 1, {}, {},{},{});pdb.gimp_file_save(imgIns, imgInsDrawable, outputFile, outputFile);pdb.gimp_image_delete(imgIns)"
        self.setParam(preserve_lum, cyan_red, magenta_green, yellow_blue)

    def setParam(self, preserve_lum, cyan_red=0, magenta_green=0, yellow_blue=0):
        self.preserve_lum = preserve_lum
        self.cyan_red = cyan_red
        self.magenta_green = magenta_green
        self.yellow_blue = yellow_blue

    def gen(self):
        cmd_str = self.template.format(self.infile, self.outfile, self.preserve_lum, self.cyan_red, self.magenta_green,
                                       self.yellow_blue)
        print(cmd_str)
        self.cmd_str = cmd_str

    def exec(self):
        self.gen()
        return super().execute()


'''
gegl commands
'''


class Cmd_gegl_color_temperature(GeglCommand):
    def __init__(self, original_temperature=0, intended_temperature=0):
        super(Cmd_gegl_color_temperature, self).__init__()
        self.operation = 'color-temperature'
        self.original_temperature = original_temperature
        self.intended_temperature = intended_temperature

    def _gen_param(self):
        self.cmd_para = ' original-temperature={} intended-temperature={} '.format(self.original_temperature,
                                                                                   self.intended_temperature)

    def exec(self):
        self._gen_param()
        self.fill(self.operation + self.cmd_para)
        return self.execute()


class Cmd_gegl_saturation(GeglCommand):
    def __init__(self, scale=0):
        super(Cmd_gegl_saturation, self).__init__()
        self.scale = scale
        self.operation = 'saturation'

    def _gen_param(self):
        self.cmd_para = ' scale={} '.format(self.scale)

    def exec(self):
        self._gen_param()
        self.fill(self.operation + self.cmd_para)
        return self.execute()


class Cmd_gegl_aggregation(GeglCommand):
    def __init__(self, geglCommands):
        super(Cmd_gegl_aggregation, self).__init__()
        self.cmds = geglCommands

    def __gen_param(self):
        self.cmd_para = ""
        for cmd in self.cmds:
            assert cmd.cmd_type == Cmd_Type.GEGL
            cmd._gen_param()
            self.cmd_para += (cmd.operation + cmd.cmd_para)

    def exec(self):
        self.__gen_param()
        self.fill(self.cmd_para)
        return self.execute()
