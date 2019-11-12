
import cmd

inf = '/Users/zhujiafeng/SIAT/gimp_test/origin.jpg'
of = '/Users/zhujiafeng/SIAT/gimp_test/gegimp_fu_test_now.jpg'
cb = cmd.Cmd_gimp_color_balance(inf, of, preserve_lum=True, yellow_blue=100)
cb.gen()
cb.exec()
