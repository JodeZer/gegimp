
import cmd

# RUNNABLE_SHELL = '/bin/zsh'
# GIMP_EXECUTE = '/Applications/GIMP-2.10.app/Contents/MacOS/GIMP'
# GEGL_EXECUTE = '/usr/local/bin/gegl'
cmd.SetEnvConf('/bin/zsh', '/Applications/GIMP-2.10.app/Contents/MacOS/GIMP', '/usr/local/bin/gegl')

inf = '/Users/zhujiafeng/SIAT/gimp_test/origin.jpg'
of = '/Users/zhujiafeng/SIAT/gimp_test/gegimp_fu_test_now.jpg'

cmds = cmd.CmdSet(inf, of)
cmds.append(cmd.Cmd_gimp_color_balance(preserve_lum=True, yellow_blue=100))
cmds.append(cmd.Cmd_gegl_saturation(scale=1.0))
cmds.append(cmd.Cmd_gegl_color_temperature(original_temperature=5000.0, intended_temperature=5000.0))
cmds.exec()
