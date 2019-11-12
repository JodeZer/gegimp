import tempfile
import command
class CmdSet():
    def __init__(self, infile, outfile):
        self.cmds = []
        self.infile = infile
        self.outfile = outfile

    def append(self, cmd):
        self.cmds.append(cmd)

    def __compact(self):
        newcmd = []
        aggcmd = []
        for cmd in self.cmds:
            if cmd.cmd_type == command.Cmd_Type.GEGL:
                aggcmd.append(cmd)
            if cmd.cmd_type == command.Cmd_Type.GIMP:
                if len(aggcmd) != 0:
                    if len(aggcmd) == 1:
                        newcmd.append(aggcmd[0])
                    else:
                        newcmd.append(command.Cmd_gegl_aggregation(aggcmd))
                    aggcmd = []
                newcmd.append(cmd)
        if len(aggcmd) != 0:
            newcmd.append(command.Cmd_gegl_aggregation(aggcmd))
        self.cmds = newcmd

    def exec(self):
        if len(self.cmds) == 0:
            return 0
        self.__compact()
        if len(self.cmds) == 1:
            cmd = self.cmds[0]
            cmd.setIOFile(self.infile, self.outfile)
            return cmd.exec()

        tmpf = tempfile.NamedTemporaryFile(delete=True)
        self.cmds[0].setIOFile(self.infile, tmpf.name)
        assert self.cmds[0].exec() == 0

        for cmd in self.cmds[1:-1]:
            assert cmd.setIOFile(tmpf.name, tmpf.name) == 0

        self.cmds[-1].setIOFile(tmpf.name, self.outfile)
        assert self.cmds[-1].exec() == 0

        tmpf.close()




