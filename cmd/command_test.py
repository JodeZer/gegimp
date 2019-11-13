import unittest
import cmd


class TestCommand(unittest.TestCase):
    def test_init(self):
        pass

    def test_color_balance(self):
        # inf = '/Users/zhujiafeng/SIAT/gimp_test/origin.jpg'
        # of = '/Users/zhujiafeng/SIAT/gimp_test/gegimp_fu_test_now.jpg'
        # cb = cmd.Cmd_gimp_color_balance(inf, of, preserve_lum=True, yellow_blue=100)
        # cb.exec()
        return

    # def test_gegl(self):
    #     inf = '/Users/zhujiafeng/SIAT/gimp_test/origin.jpg'
    #     of = '/Users/zhujiafeng/SIAT/gimp_test/gegimp_fu_test_py.jpg'
    #     cb = cmd.Cmd_gegl_color_temperature(original_temperature=10000.0, intended_temperature=4000.0)
    #     cb.setIOFile(inf, of)
    #     cb.exec()
    #     return

    def test_gegl_agg(self):
        inf = '/Users/zhujiafeng/SIAT/gimp_test/origin.jpg'
        of = '/Users/zhujiafeng/SIAT/gimp_test/gegimp_fu_agg_test.jpg'
        cs = cmd.CmdSet(inf, of)
        cs.append(cmd.Cmd_gegl_color_temperature(original_temperature=10000.0, intended_temperature=4000.0))
        cs.append(cmd.Cmd_gegl_saturation(scale=3.0))
        cs.exec()
