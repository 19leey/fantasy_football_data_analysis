# -*- encoding: utf-8 -*-
import pandas as pd
import subprocess


def run_rscript():
    command = 'Rscript'
    script_path = 'render_plots.R'
    ret = subprocess.check_output([command, script_path])
    return ret.decode()
