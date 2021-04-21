#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Rx 5 Antenna Array: The Seer
# Author: Tate Harsch-Hudspeth & Evan Peelen, Tested by Victor Madrid
# Description: This flowgraph runs the Rx 5 antenna array for The Seer
# GNU Radio version: 3.8.2.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
import sip
from gnuradio import analog
from gnuradio import blocks
from gnuradio import fft
from gnuradio.fft import window
from gnuradio import gr
from gnuradio.filter import firdes
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation

from gnuradio import qtgui

class the_seer_rx_flow(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Rx 5 Antenna Array: The Seer")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Rx 5 Antenna Array: The Seer")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "the_seer_rx_flow")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1024000
        self.fft_bins = fft_bins = 1024
        self.skip_bins = skip_bins = int(fft_bins/2+fft_bins/samp_rate)+1
        self.k = k = -60.103
        self.head = head = 32000
        self.freq = freq = 750000000

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_number_sink_0_1_1_0_1 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_NONE,
            1
        )
        self.qtgui_number_sink_0_1_1_0_1.set_update_time(0.10)
        self.qtgui_number_sink_0_1_1_0_1.set_title("Phase 4")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0_1_1_0_1.set_min(i, -1000)
            self.qtgui_number_sink_0_1_1_0_1.set_max(i, 1000)
            self.qtgui_number_sink_0_1_1_0_1.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0_1_1_0_1.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0_1_1_0_1.set_label(i, labels[i])
            self.qtgui_number_sink_0_1_1_0_1.set_unit(i, units[i])
            self.qtgui_number_sink_0_1_1_0_1.set_factor(i, factor[i])

        self.qtgui_number_sink_0_1_1_0_1.enable_autoscale(False)
        self._qtgui_number_sink_0_1_1_0_1_win = sip.wrapinstance(self.qtgui_number_sink_0_1_1_0_1.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_1_1_0_1_win, 4, 1, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_number_sink_0_1_1_0_0_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_NONE,
            1
        )
        self.qtgui_number_sink_0_1_1_0_0_0.set_update_time(0.10)
        self.qtgui_number_sink_0_1_1_0_0_0.set_title("Pr_4")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0_1_1_0_0_0.set_min(i, 0)
            self.qtgui_number_sink_0_1_1_0_0_0.set_max(i, 10)
            self.qtgui_number_sink_0_1_1_0_0_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0_1_1_0_0_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0_1_1_0_0_0.set_label(i, labels[i])
            self.qtgui_number_sink_0_1_1_0_0_0.set_unit(i, units[i])
            self.qtgui_number_sink_0_1_1_0_0_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0_1_1_0_0_0.enable_autoscale(False)
        self._qtgui_number_sink_0_1_1_0_0_0_win = sip.wrapinstance(self.qtgui_number_sink_0_1_1_0_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_1_1_0_0_0_win, 4, 2, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_number_sink_0_1_1_0_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_NONE,
            1
        )
        self.qtgui_number_sink_0_1_1_0_0.set_update_time(0.10)
        self.qtgui_number_sink_0_1_1_0_0.set_title("Pr_3")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0_1_1_0_0.set_min(i, 0)
            self.qtgui_number_sink_0_1_1_0_0.set_max(i, 10)
            self.qtgui_number_sink_0_1_1_0_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0_1_1_0_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0_1_1_0_0.set_label(i, labels[i])
            self.qtgui_number_sink_0_1_1_0_0.set_unit(i, units[i])
            self.qtgui_number_sink_0_1_1_0_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0_1_1_0_0.enable_autoscale(False)
        self._qtgui_number_sink_0_1_1_0_0_win = sip.wrapinstance(self.qtgui_number_sink_0_1_1_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_1_1_0_0_win, 3, 2, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_number_sink_0_1_1_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_NONE,
            1
        )
        self.qtgui_number_sink_0_1_1_0.set_update_time(0.10)
        self.qtgui_number_sink_0_1_1_0.set_title("Phase 3")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0_1_1_0.set_min(i, -1000)
            self.qtgui_number_sink_0_1_1_0.set_max(i, 1000)
            self.qtgui_number_sink_0_1_1_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0_1_1_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0_1_1_0.set_label(i, labels[i])
            self.qtgui_number_sink_0_1_1_0.set_unit(i, units[i])
            self.qtgui_number_sink_0_1_1_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0_1_1_0.enable_autoscale(False)
        self._qtgui_number_sink_0_1_1_0_win = sip.wrapinstance(self.qtgui_number_sink_0_1_1_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_1_1_0_win, 3, 1, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_number_sink_0_1_1 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_NONE,
            1
        )
        self.qtgui_number_sink_0_1_1.set_update_time(0.10)
        self.qtgui_number_sink_0_1_1.set_title("Pr_2")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0_1_1.set_min(i, 0)
            self.qtgui_number_sink_0_1_1.set_max(i, 10)
            self.qtgui_number_sink_0_1_1.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0_1_1.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0_1_1.set_label(i, labels[i])
            self.qtgui_number_sink_0_1_1.set_unit(i, units[i])
            self.qtgui_number_sink_0_1_1.set_factor(i, factor[i])

        self.qtgui_number_sink_0_1_1.enable_autoscale(False)
        self._qtgui_number_sink_0_1_1_win = sip.wrapinstance(self.qtgui_number_sink_0_1_1.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_1_1_win, 2, 2, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_number_sink_0_1_0_1_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_NONE,
            1
        )
        self.qtgui_number_sink_0_1_0_1_0.set_update_time(0.10)
        self.qtgui_number_sink_0_1_0_1_0.set_title("Phase_2")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0_1_0_1_0.set_min(i, -1000)
            self.qtgui_number_sink_0_1_0_1_0.set_max(i, 1000)
            self.qtgui_number_sink_0_1_0_1_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0_1_0_1_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0_1_0_1_0.set_label(i, labels[i])
            self.qtgui_number_sink_0_1_0_1_0.set_unit(i, units[i])
            self.qtgui_number_sink_0_1_0_1_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0_1_0_1_0.enable_autoscale(False)
        self._qtgui_number_sink_0_1_0_1_0_win = sip.wrapinstance(self.qtgui_number_sink_0_1_0_1_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_1_0_1_0_win, 2, 1, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_number_sink_0_1_0_1 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_NONE,
            1
        )
        self.qtgui_number_sink_0_1_0_1.set_update_time(0.10)
        self.qtgui_number_sink_0_1_0_1.set_title("Phase_1")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0_1_0_1.set_min(i, -1000)
            self.qtgui_number_sink_0_1_0_1.set_max(i, 1000)
            self.qtgui_number_sink_0_1_0_1.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0_1_0_1.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0_1_0_1.set_label(i, labels[i])
            self.qtgui_number_sink_0_1_0_1.set_unit(i, units[i])
            self.qtgui_number_sink_0_1_0_1.set_factor(i, factor[i])

        self.qtgui_number_sink_0_1_0_1.enable_autoscale(False)
        self._qtgui_number_sink_0_1_0_1_win = sip.wrapinstance(self.qtgui_number_sink_0_1_0_1.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_1_0_1_win, 1, 1, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_number_sink_0_1_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_NONE,
            1
        )
        self.qtgui_number_sink_0_1_0.set_update_time(0.10)
        self.qtgui_number_sink_0_1_0.set_title("Refference")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0_1_0.set_min(i, -1000)
            self.qtgui_number_sink_0_1_0.set_max(i, 1000)
            self.qtgui_number_sink_0_1_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0_1_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0_1_0.set_label(i, labels[i])
            self.qtgui_number_sink_0_1_0.set_unit(i, units[i])
            self.qtgui_number_sink_0_1_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0_1_0.enable_autoscale(False)
        self._qtgui_number_sink_0_1_0_win = sip.wrapinstance(self.qtgui_number_sink_0_1_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_1_0_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_number_sink_0_1 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_NONE,
            1
        )
        self.qtgui_number_sink_0_1.set_update_time(0.10)
        self.qtgui_number_sink_0_1.set_title("Pr_1")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0_1.set_min(i, 0)
            self.qtgui_number_sink_0_1.set_max(i, 10)
            self.qtgui_number_sink_0_1.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0_1.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0_1.set_label(i, labels[i])
            self.qtgui_number_sink_0_1.set_unit(i, units[i])
            self.qtgui_number_sink_0_1.set_factor(i, factor[i])

        self.qtgui_number_sink_0_1.enable_autoscale(False)
        self._qtgui_number_sink_0_1_win = sip.wrapinstance(self.qtgui_number_sink_0_1.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_1_win, 1, 2, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.fft_vxx_0_1_0_0_0_0 = fft.fft_vcc(fft_bins, True, window.blackmanharris(1024), True, 1)
        self.fft_vxx_0_1_0_0_0 = fft.fft_vcc(fft_bins, True, window.blackmanharris(1024), True, 1)
        self.fft_vxx_0_1_0_0 = fft.fft_vcc(fft_bins, True, window.blackmanharris(1024), True, 1)
        self.fft_vxx_0_1_0 = fft.fft_vcc(fft_bins, True, window.blackmanharris(1024), True, 1)
        self.fft_vxx_0 = fft.fft_vcc(fft_bins, True, window.blackmanharris(1024), True, 1)
        self.blocks_vector_to_stream_0_1_1_0_0_1_0_0 = blocks.vector_to_stream(gr.sizeof_float*1, fft_bins)
        self.blocks_vector_to_stream_0_1_1_0_0_1_0 = blocks.vector_to_stream(gr.sizeof_float*1, fft_bins)
        self.blocks_vector_to_stream_0_1_1_0_0_1 = blocks.vector_to_stream(gr.sizeof_float*1, fft_bins)
        self.blocks_vector_to_stream_0_1_1_0_0_0_0_0_0 = blocks.vector_to_stream(gr.sizeof_float*1, fft_bins)
        self.blocks_vector_to_stream_0_1_1_0_0_0_0_0 = blocks.vector_to_stream(gr.sizeof_float*1, fft_bins)
        self.blocks_vector_to_stream_0_1_1_0_0_0_0 = blocks.vector_to_stream(gr.sizeof_float*1, fft_bins)
        self.blocks_vector_to_stream_0_1_1_0_0_0 = blocks.vector_to_stream(gr.sizeof_float*1, fft_bins)
        self.blocks_vector_to_stream_0_1_1_0_0 = blocks.vector_to_stream(gr.sizeof_float*1, fft_bins)
        self.blocks_vector_to_stream_0_1_0_0 = blocks.vector_to_stream(gr.sizeof_float*1, fft_bins)
        self.blocks_throttle_0_0_0_0_0_0_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_throttle_0_0_0_0_0_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_throttle_0_0_0_0_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_throttle_0_0_0_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_stream_to_vector_1_0_0_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, 1024)
        self.blocks_stream_to_vector_1_0_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, 1024)
        self.blocks_stream_to_vector_1_0_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, 1024)
        self.blocks_stream_to_vector_1_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, 1024)
        self.blocks_stream_to_vector_0 = blocks.stream_to_vector(gr.sizeof_gr_complex*1, 1024)
        self.blocks_skiphead_0_2 = blocks.skiphead(gr.sizeof_float*1, skip_bins)
        self.blocks_skiphead_0_1_0_0_0_1_0_0 = blocks.skiphead(gr.sizeof_float*1, skip_bins)
        self.blocks_skiphead_0_1_0_0_0_1_0 = blocks.skiphead(gr.sizeof_float*1, skip_bins)
        self.blocks_skiphead_0_1_0_0_0_1 = blocks.skiphead(gr.sizeof_float*1, skip_bins)
        self.blocks_skiphead_0_1_0_0_0_0_0_0_0 = blocks.skiphead(gr.sizeof_float*1, skip_bins)
        self.blocks_skiphead_0_1_0_0_0_0_0_0 = blocks.skiphead(gr.sizeof_float*1, skip_bins)
        self.blocks_skiphead_0_1_0_0_0_0_0 = blocks.skiphead(gr.sizeof_float*1, skip_bins)
        self.blocks_skiphead_0_1_0_0_0_0 = blocks.skiphead(gr.sizeof_float*1, skip_bins)
        self.blocks_skiphead_0_1_0_0_0 = blocks.skiphead(gr.sizeof_float*1, skip_bins)
        self.blocks_nlog10_ff_0_0_0_0 = blocks.nlog10_ff(10, fft_bins, k)
        self.blocks_nlog10_ff_0_0_0 = blocks.nlog10_ff(10, fft_bins, k)
        self.blocks_nlog10_ff_0_0 = blocks.nlog10_ff(10, fft_bins, k)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10, fft_bins, k)
        self.blocks_moving_average_xx_3_0 = blocks.moving_average_ff(1000, 1/1000, 1000, 1)
        self.blocks_moving_average_xx_2_1 = blocks.moving_average_ff(1000, 1/1000, 1000, 1)
        self.blocks_moving_average_xx_2_0 = blocks.moving_average_ff(1000, 1/1000, 1000, 1)
        self.blocks_moving_average_xx_1_0_1 = blocks.moving_average_ff(1000, 1/1000, 1000, 1)
        self.blocks_moving_average_xx_1_0_0_1 = blocks.moving_average_ff(1000, 1/1000, 1000, 1)
        self.blocks_moving_average_xx_1_0_0_0_0 = blocks.moving_average_ff(1000, 1/1000, 1000, 1)
        self.blocks_moving_average_xx_1_0_0_0 = blocks.moving_average_ff(1000, 1/1000, 1000, 1)
        self.blocks_moving_average_xx_1_0_0 = blocks.moving_average_ff(1000, 1/1000, 1000, 1)
        self.blocks_moving_average_xx_1_0 = blocks.moving_average_ff(1000, 1/1000, 1000, 1)
        self.blocks_keep_one_in_n_0_2_0_0_0_1_0_0 = blocks.keep_one_in_n(gr.sizeof_float*1, 1024)
        self.blocks_keep_one_in_n_0_2_0_0_0_1_0 = blocks.keep_one_in_n(gr.sizeof_float*1, 1024)
        self.blocks_keep_one_in_n_0_2_0_0_0_1 = blocks.keep_one_in_n(gr.sizeof_float*1, 1024)
        self.blocks_keep_one_in_n_0_2_0_0_0_0_0_0_0 = blocks.keep_one_in_n(gr.sizeof_float*1, 1024)
        self.blocks_keep_one_in_n_0_2_0_0_0_0_0_0 = blocks.keep_one_in_n(gr.sizeof_float*1, 1024)
        self.blocks_keep_one_in_n_0_2_0_0_0_0_0 = blocks.keep_one_in_n(gr.sizeof_float*1, 1024)
        self.blocks_keep_one_in_n_0_2_0_0_0_0 = blocks.keep_one_in_n(gr.sizeof_float*1, 1024)
        self.blocks_keep_one_in_n_0_2_0_0_0 = blocks.keep_one_in_n(gr.sizeof_float*1, 1024)
        self.blocks_keep_one_in_n_0_2 = blocks.keep_one_in_n(gr.sizeof_float*1, 1024)
        self.blocks_head_3_0 = blocks.head(gr.sizeof_float*1, head)
        self.blocks_head_2_1 = blocks.head(gr.sizeof_float*1, head)
        self.blocks_head_2_0 = blocks.head(gr.sizeof_float*1, head)
        self.blocks_head_1_0_2 = blocks.head(gr.sizeof_float*1, head)
        self.blocks_head_1_0_1 = blocks.head(gr.sizeof_float*1, head)
        self.blocks_head_1_0_0_1 = blocks.head(gr.sizeof_float*1, head)
        self.blocks_head_1_0_0_0 = blocks.head(gr.sizeof_float*1, head)
        self.blocks_head_1_0_0 = blocks.head(gr.sizeof_float*1, head)
        self.blocks_head_1_0 = blocks.head(gr.sizeof_float*1, head)
        self.blocks_divide_xx_0_0_0_0 = blocks.divide_cc(fft_bins)
        self.blocks_divide_xx_0_0_0 = blocks.divide_cc(fft_bins)
        self.blocks_divide_xx_0_0 = blocks.divide_cc(fft_bins)
        self.blocks_divide_xx_0 = blocks.divide_cc(fft_bins)
        self.blocks_complex_to_mag_squared_0_0_0_0_0_0_0_0 = blocks.complex_to_mag_squared(fft_bins)
        self.blocks_complex_to_mag_squared_0_0_0_0_0_0_0 = blocks.complex_to_mag_squared(fft_bins)
        self.blocks_complex_to_mag_squared_0_0_0_0_0_0 = blocks.complex_to_mag_squared(fft_bins)
        self.blocks_complex_to_mag_squared_0_0_0_0_0 = blocks.complex_to_mag_squared(fft_bins)
        self.blocks_complex_to_arg_0_2_0 = blocks.complex_to_arg(fft_bins)
        self.blocks_complex_to_arg_0_0_0_0_0_0 = blocks.complex_to_arg(fft_bins)
        self.blocks_complex_to_arg_0_0_0_0_0 = blocks.complex_to_arg(fft_bins)
        self.blocks_complex_to_arg_0_0_0_0 = blocks.complex_to_arg(fft_bins)
        self.blocks_complex_to_arg_0_0_0 = blocks.complex_to_arg(fft_bins)
        self.analog_const_source_x_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 0)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_throttle_0_0_0_0, 0))
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_throttle_0_0_0_0_0, 0))
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_throttle_0_0_0_0_0_0, 0))
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_throttle_0_0_0_0_0_0_0, 0))
        self.connect((self.blocks_complex_to_arg_0_0_0, 0), (self.blocks_vector_to_stream_0_1_1_0_0, 0))
        self.connect((self.blocks_complex_to_arg_0_0_0_0, 0), (self.blocks_vector_to_stream_0_1_1_0_0_1, 0))
        self.connect((self.blocks_complex_to_arg_0_0_0_0_0, 0), (self.blocks_vector_to_stream_0_1_1_0_0_1_0, 0))
        self.connect((self.blocks_complex_to_arg_0_0_0_0_0_0, 0), (self.blocks_vector_to_stream_0_1_1_0_0_1_0_0, 0))
        self.connect((self.blocks_complex_to_arg_0_2_0, 0), (self.blocks_vector_to_stream_0_1_0_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0_0_0_0_0, 0), (self.blocks_nlog10_ff_0_0_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0_0_0_0_0_0, 0), (self.blocks_nlog10_ff_0_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0_0_0_0_0_0_0, 0), (self.blocks_nlog10_ff_0_0_0_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0_0_0_0_0_0_0_0, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.blocks_divide_xx_0, 0), (self.blocks_complex_to_arg_0_0_0, 0))
        self.connect((self.blocks_divide_xx_0_0, 0), (self.blocks_complex_to_arg_0_0_0_0, 0))
        self.connect((self.blocks_divide_xx_0_0_0, 0), (self.blocks_complex_to_arg_0_0_0_0_0, 0))
        self.connect((self.blocks_divide_xx_0_0_0_0, 0), (self.blocks_complex_to_arg_0_0_0_0_0_0, 0))
        self.connect((self.blocks_head_1_0, 0), (self.blocks_moving_average_xx_1_0, 0))
        self.connect((self.blocks_head_1_0_0, 0), (self.blocks_moving_average_xx_1_0_0, 0))
        self.connect((self.blocks_head_1_0_0_0, 0), (self.blocks_moving_average_xx_1_0_0_0, 0))
        self.connect((self.blocks_head_1_0_0_1, 0), (self.blocks_moving_average_xx_1_0_0_1, 0))
        self.connect((self.blocks_head_1_0_1, 0), (self.blocks_moving_average_xx_1_0_0_0_0, 0))
        self.connect((self.blocks_head_1_0_2, 0), (self.blocks_moving_average_xx_1_0_1, 0))
        self.connect((self.blocks_head_2_0, 0), (self.blocks_moving_average_xx_2_0, 0))
        self.connect((self.blocks_head_2_1, 0), (self.blocks_moving_average_xx_2_1, 0))
        self.connect((self.blocks_head_3_0, 0), (self.blocks_moving_average_xx_3_0, 0))
        self.connect((self.blocks_keep_one_in_n_0_2, 0), (self.blocks_head_2_1, 0))
        self.connect((self.blocks_keep_one_in_n_0_2_0_0_0, 0), (self.blocks_head_1_0_0_0, 0))
        self.connect((self.blocks_keep_one_in_n_0_2_0_0_0_0, 0), (self.blocks_head_1_0_1, 0))
        self.connect((self.blocks_keep_one_in_n_0_2_0_0_0_0_0, 0), (self.blocks_head_1_0_0, 0))
        self.connect((self.blocks_keep_one_in_n_0_2_0_0_0_0_0_0, 0), (self.blocks_head_1_0_0_1, 0))
        self.connect((self.blocks_keep_one_in_n_0_2_0_0_0_0_0_0_0, 0), (self.blocks_head_2_0, 0))
        self.connect((self.blocks_keep_one_in_n_0_2_0_0_0_1, 0), (self.blocks_head_1_0, 0))
        self.connect((self.blocks_keep_one_in_n_0_2_0_0_0_1_0, 0), (self.blocks_head_1_0_2, 0))
        self.connect((self.blocks_keep_one_in_n_0_2_0_0_0_1_0_0, 0), (self.blocks_head_3_0, 0))
        self.connect((self.blocks_moving_average_xx_1_0, 0), (self.qtgui_number_sink_0_1_1_0, 0))
        self.connect((self.blocks_moving_average_xx_1_0_0, 0), (self.qtgui_number_sink_0_1_1_0_0, 0))
        self.connect((self.blocks_moving_average_xx_1_0_0_0, 0), (self.qtgui_number_sink_0_1_1_0_1, 0))
        self.connect((self.blocks_moving_average_xx_1_0_0_0_0, 0), (self.qtgui_number_sink_0_1_1_0_0_0, 0))
        self.connect((self.blocks_moving_average_xx_1_0_0_1, 0), (self.qtgui_number_sink_0_1_1, 0))
        self.connect((self.blocks_moving_average_xx_1_0_1, 0), (self.qtgui_number_sink_0_1_0_1_0, 0))
        self.connect((self.blocks_moving_average_xx_2_0, 0), (self.qtgui_number_sink_0_1, 0))
        self.connect((self.blocks_moving_average_xx_2_1, 0), (self.qtgui_number_sink_0_1_0, 0))
        self.connect((self.blocks_moving_average_xx_3_0, 0), (self.qtgui_number_sink_0_1_0_1, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.blocks_vector_to_stream_0_1_1_0_0_0_0_0_0, 0))
        self.connect((self.blocks_nlog10_ff_0_0, 0), (self.blocks_vector_to_stream_0_1_1_0_0_0_0, 0))
        self.connect((self.blocks_nlog10_ff_0_0_0, 0), (self.blocks_vector_to_stream_0_1_1_0_0_0, 0))
        self.connect((self.blocks_nlog10_ff_0_0_0_0, 0), (self.blocks_vector_to_stream_0_1_1_0_0_0_0_0, 0))
        self.connect((self.blocks_skiphead_0_1_0_0_0, 0), (self.blocks_keep_one_in_n_0_2_0_0_0, 0))
        self.connect((self.blocks_skiphead_0_1_0_0_0_0, 0), (self.blocks_keep_one_in_n_0_2_0_0_0_0, 0))
        self.connect((self.blocks_skiphead_0_1_0_0_0_0_0, 0), (self.blocks_keep_one_in_n_0_2_0_0_0_0_0, 0))
        self.connect((self.blocks_skiphead_0_1_0_0_0_0_0_0, 0), (self.blocks_keep_one_in_n_0_2_0_0_0_0_0_0, 0))
        self.connect((self.blocks_skiphead_0_1_0_0_0_0_0_0_0, 0), (self.blocks_keep_one_in_n_0_2_0_0_0_0_0_0_0, 0))
        self.connect((self.blocks_skiphead_0_1_0_0_0_1, 0), (self.blocks_keep_one_in_n_0_2_0_0_0_1, 0))
        self.connect((self.blocks_skiphead_0_1_0_0_0_1_0, 0), (self.blocks_keep_one_in_n_0_2_0_0_0_1_0, 0))
        self.connect((self.blocks_skiphead_0_1_0_0_0_1_0_0, 0), (self.blocks_keep_one_in_n_0_2_0_0_0_1_0_0, 0))
        self.connect((self.blocks_skiphead_0_2, 0), (self.blocks_keep_one_in_n_0_2, 0))
        self.connect((self.blocks_stream_to_vector_0, 0), (self.fft_vxx_0, 0))
        self.connect((self.blocks_stream_to_vector_1_0, 0), (self.fft_vxx_0_1_0, 0))
        self.connect((self.blocks_stream_to_vector_1_0_0, 0), (self.fft_vxx_0_1_0_0, 0))
        self.connect((self.blocks_stream_to_vector_1_0_0_0, 0), (self.fft_vxx_0_1_0_0_0, 0))
        self.connect((self.blocks_stream_to_vector_1_0_0_0_0, 0), (self.fft_vxx_0_1_0_0_0_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_stream_to_vector_0, 0))
        self.connect((self.blocks_throttle_0_0_0_0, 0), (self.blocks_stream_to_vector_1_0, 0))
        self.connect((self.blocks_throttle_0_0_0_0_0, 0), (self.blocks_stream_to_vector_1_0_0, 0))
        self.connect((self.blocks_throttle_0_0_0_0_0_0, 0), (self.blocks_stream_to_vector_1_0_0_0, 0))
        self.connect((self.blocks_throttle_0_0_0_0_0_0_0, 0), (self.blocks_stream_to_vector_1_0_0_0_0, 0))
        self.connect((self.blocks_vector_to_stream_0_1_0_0, 0), (self.blocks_skiphead_0_2, 0))
        self.connect((self.blocks_vector_to_stream_0_1_1_0_0, 0), (self.blocks_skiphead_0_1_0_0_0, 0))
        self.connect((self.blocks_vector_to_stream_0_1_1_0_0_0, 0), (self.blocks_skiphead_0_1_0_0_0_0, 0))
        self.connect((self.blocks_vector_to_stream_0_1_1_0_0_0_0, 0), (self.blocks_skiphead_0_1_0_0_0_0_0, 0))
        self.connect((self.blocks_vector_to_stream_0_1_1_0_0_0_0_0, 0), (self.blocks_skiphead_0_1_0_0_0_0_0_0, 0))
        self.connect((self.blocks_vector_to_stream_0_1_1_0_0_0_0_0_0, 0), (self.blocks_skiphead_0_1_0_0_0_0_0_0_0, 0))
        self.connect((self.blocks_vector_to_stream_0_1_1_0_0_1, 0), (self.blocks_skiphead_0_1_0_0_0_1, 0))
        self.connect((self.blocks_vector_to_stream_0_1_1_0_0_1_0, 0), (self.blocks_skiphead_0_1_0_0_0_1_0, 0))
        self.connect((self.blocks_vector_to_stream_0_1_1_0_0_1_0_0, 0), (self.blocks_skiphead_0_1_0_0_0_1_0_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_complex_to_arg_0_2_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_divide_xx_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_divide_xx_0_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_divide_xx_0_0_0, 0))
        self.connect((self.fft_vxx_0, 0), (self.blocks_divide_xx_0_0_0_0, 0))
        self.connect((self.fft_vxx_0_1_0, 0), (self.blocks_complex_to_mag_squared_0_0_0_0_0, 0))
        self.connect((self.fft_vxx_0_1_0, 0), (self.blocks_divide_xx_0, 1))
        self.connect((self.fft_vxx_0_1_0_0, 0), (self.blocks_complex_to_mag_squared_0_0_0_0_0_0, 0))
        self.connect((self.fft_vxx_0_1_0_0, 0), (self.blocks_divide_xx_0_0, 1))
        self.connect((self.fft_vxx_0_1_0_0_0, 0), (self.blocks_complex_to_mag_squared_0_0_0_0_0_0_0, 0))
        self.connect((self.fft_vxx_0_1_0_0_0, 0), (self.blocks_divide_xx_0_0_0, 1))
        self.connect((self.fft_vxx_0_1_0_0_0_0, 0), (self.blocks_complex_to_mag_squared_0_0_0_0_0_0_0_0, 0))
        self.connect((self.fft_vxx_0_1_0_0_0_0, 0), (self.blocks_divide_xx_0_0_0_0, 1))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "the_seer_rx_flow")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_skip_bins(int(self.fft_bins/2+self.fft_bins/self.samp_rate)+1)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle_0_0_0_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle_0_0_0_0_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle_0_0_0_0_0_0.set_sample_rate(self.samp_rate)
        self.blocks_throttle_0_0_0_0_0_0_0.set_sample_rate(self.samp_rate)

    def get_fft_bins(self):
        return self.fft_bins

    def set_fft_bins(self, fft_bins):
        self.fft_bins = fft_bins
        self.set_skip_bins(int(self.fft_bins/2+self.fft_bins/self.samp_rate)+1)

    def get_skip_bins(self):
        return self.skip_bins

    def set_skip_bins(self, skip_bins):
        self.skip_bins = skip_bins

    def get_k(self):
        return self.k

    def set_k(self, k):
        self.k = k

    def get_head(self):
        return self.head

    def set_head(self, head):
        self.head = head
        self.blocks_head_1_0.set_length(self.head)
        self.blocks_head_1_0_0.set_length(self.head)
        self.blocks_head_1_0_0_0.set_length(self.head)
        self.blocks_head_1_0_0_1.set_length(self.head)
        self.blocks_head_1_0_1.set_length(self.head)
        self.blocks_head_1_0_2.set_length(self.head)
        self.blocks_head_2_0.set_length(self.head)
        self.blocks_head_2_1.set_length(self.head)
        self.blocks_head_3_0.set_length(self.head)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq





def main(top_block_cls=the_seer_rx_flow, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def quitting():
        tb.stop()
        tb.wait()

    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()

if __name__ == '__main__':
    main()
