import logging
import webbrowser
from PyQt5.QtCore import QObject, pyqtSlot
from constants import Constants, Messages
from switchable_label import SwitchableLabelsIterable
from weatherdata import SpaceWeatherData
from utilities import pop_up


class SpaceWeatherManager(QObject):
    """Class to manage the spaceweather screen."""

    def __init__(self, owner):
        super().__init__()
        self._owner = owner
        self._owner.info_now_btn.clicked.connect(
            lambda: webbrowser.open(Constants.SPACE_WEATHER_INFO)
        )
        self._owner.update_now_bar.clicked.connect(self._start_update_space_weather)
        self._owner.update_now_bar.set_idle()
        self._owner.space_weather_data = SpaceWeatherData()
        self._owner.space_weather_data.update_complete.connect(self._update_space_weather)

        self.space_weather_labels = (
            self._owner.space_weather_lbl_0,
            self._owner.space_weather_lbl_1,
            self._owner.space_weather_lbl_2,
            self._owner.space_weather_lbl_3,
            self._owner.space_weather_lbl_4,
            self._owner.space_weather_lbl_5,
            self._owner.space_weather_lbl_6,
            self._owner.space_weather_lbl_7,
            self._owner.space_weather_lbl_8
        )

        for lab in self.space_weather_labels:
            lab.set_default_stylesheet()

        self._owner.space_weather_label_container.labels = self.space_weather_labels
        self._owner.space_weather_label_name_container.labels = [
            self._owner.eme_lbl,
            self._owner.ms_lbl,
            self._owner.muf_lbl,
            self._owner.hi_lbl,
            self._owner.eu50_lbl,
            self._owner.eu70_lbl,
            self._owner.eu144_lbl,
            self._owner.na_lbl,
            self._owner.aurora_lbl
        ]

        self._switchable_r_labels = SwitchableLabelsIterable(
            self._owner.r0_now_lbl,
            self._owner.r1_now_lbl,
            self._owner.r2_now_lbl,
            self._owner.r3_now_lbl,
            self._owner.r4_now_lbl,
            self._owner.r5_now_lbl
        )

        self._switchable_s_labels = SwitchableLabelsIterable(
            self._owner.s0_now_lbl,
            self._owner.s1_now_lbl,
            self._owner.s2_now_lbl,
            self._owner.s3_now_lbl,
            self._owner.s4_now_lbl,
            self._owner.s5_now_lbl
        )

        self._switchable_g_now_labels = SwitchableLabelsIterable(
            self._owner.g0_now_lbl,
            self._owner.g1_now_lbl,
            self._owner.g2_now_lbl,
            self._owner.g3_now_lbl,
            self._owner.g4_now_lbl,
            self._owner.g5_now_lbl
        )

        self._switchable_g_today_labels = SwitchableLabelsIterable(
            self._owner.g0_today_lbl,
            self._owner.g1_today_lbl,
            self._owner.g2_today_lbl,
            self._owner.g3_today_lbl,
            self._owner.g4_today_lbl,
            self._owner.g5_today_lbl
        )

        self._k_storm_labels = SwitchableLabelsIterable(
            self._owner.k_ex_sev_storm_lbl,
            self._owner.k_very_sev_storm_lbl,
            self._owner.k_sev_storm_lbl,
            self._owner.k_maj_storm_lbl,
            self._owner.k_min_storm_lbl,
            self._owner.k_active_lbl,
            self._owner.k_unsettled_lbl,
            self._owner.k_quiet_lbl,
            self._owner.k_very_quiet_lbl,
            self._owner.k_inactive_lbl
        )

        self._a_storm_labels = SwitchableLabelsIterable(
            self._owner.a_sev_storm_lbl,
            self._owner.a_maj_storm_lbl,
            self._owner.a_min_storm_lbl,
            self._owner.a_active_lbl,
            self._owner.a_unsettled_lbl,
            self._owner.a_quiet_lbl
        )

        # Used by ThemeManager.
        self.refreshable_labels = SwitchableLabelsIterable(
            *self._switchable_r_labels,
            *self._switchable_s_labels,
            *self._switchable_g_now_labels,
            *self._switchable_g_today_labels,
            *self._k_storm_labels,
            *self._a_storm_labels,
            self._owner.expected_noise_lbl
        )

    @pyqtSlot()
    def _start_update_space_weather(self):
        """Start the update of the space weather screen.

        Start the corresponding thread.
        """
        if not self._owner.space_weather_data.is_updating:
            self._owner.update_now_bar.set_updating()
            self._owner.space_weather_data.update()

    @pyqtSlot(bool)
    def _update_space_weather(self, status_ok):
        """Update the space weather screen after a successful download.

        If the download was not successful throw a warning. In any case remove
        the downloaded data.
        """
        self._owner.update_now_bar.set_idle()
        if status_ok:
            try:
                xray_long = float(self._owner.space_weather_data.xray)

                def format_text(letter, power):
                    return letter + f"{xray_long * 10**power:.1f}"

                if xray_long < 1e-8 and xray_long != -1.00e+05:
                    self._owner.peak_flux_lbl.setText(format_text("<A", 8))
                elif xray_long >= 1e-8 and xray_long < 1e-7:
                    self._owner.peak_flux_lbl.setText(format_text("A", 8))
                elif xray_long >= 1e-7 and xray_long < 1e-6:
                    self._owner.peak_flux_lbl.setText(format_text("B", 7))
                elif xray_long >= 1e-6 and xray_long < 1e-5:
                    self._owner.peak_flux_lbl.setText(format_text("C", 6))
                elif xray_long >= 1e-5 and xray_long < 1e-4:
                    self._owner.peak_flux_lbl.setText(format_text("M", 5))
                elif xray_long >= 1e-4:
                    self._owner.peak_flux_lbl.setText(format_text("X", 4))
                elif xray_long == -1.00e+05:
                    self._owner.peak_flux_lbl.setText("No Data")

                if xray_long < 1e-5 and xray_long != -1.00e+05:
                    self._switchable_r_labels.switch_on(self._owner.r0_now_lbl)
                elif xray_long >= 1e-5 and xray_long < 5e-5:
                    self._switchable_r_labels.switch_on(self._owner.r1_now_lbl)
                elif xray_long >= 5e-5 and xray_long < 1e-4:
                    self._switchable_r_labels.switch_on(self._owner.r2_now_lbl)
                elif xray_long >= 1e-4 and xray_long < 1e-3:
                    self._switchable_r_labels.switch_on(self._owner.r3_now_lbl)
                elif xray_long >= 1e-3 and xray_long < 2e-3:
                    self._switchable_r_labels.switch_on(self._owner.r4_now_lbl)
                elif xray_long >= 2e-3:
                    self._switchable_r_labels.switch_on(self._owner.r5_now_lbl)
                elif xray_long == -1.00e+05:
                    self._switchable_r_labels.switch_off_all()

                pro10 = float(self._owner.space_weather_data.prot_el)
                if pro10 < 10 and pro10 != -1.00e+05:
                    self._switchable_s_labels.switch_on(self._owner.s0_now_lbl)
                elif pro10 >= 10 and pro10 < 100:
                    self._switchable_s_labels.switch_on(self._owner.s1_now_lbl)
                elif pro10 >= 100 and pro10 < 1000:
                    self._switchable_s_labels.switch_on(self._owner.s2_now_lbl)
                elif pro10 >= 1000 and pro10 < 10000:
                    self._switchable_s_labels.switch_on(self._owner.s3_now_lbl)
                elif pro10 >= 10000 and pro10 < 100000:
                    self._switchable_s_labels.switch_on(self._owner.s4_now_lbl)
                elif pro10 >= 100000:
                    self._switchable_s_labels.switch_on(self._owner.s5_now_lbl)
                elif pro10 == -1.00e+05:
                    self._switchable_s_labels.switch_off_all()

                k_index = int(self._owner.space_weather_data.ak_index[8][11].replace('.', ''))
                self._owner.k_index_lbl.setText(str(k_index))
                a_index = int(self._owner.space_weather_data.ak_index[7][7].replace('.', ''))
                self._owner.a_index_lbl.setText(str(a_index))

                if k_index == 0:
                    self._switchable_g_now_labels.switch_on(self._owner.g0_now_lbl)
                    self._k_storm_labels.switch_on(self._owner.k_inactive_lbl)
                    self._owner.expected_noise_lbl.setText("  S0 - S1 (<-120 dBm)  ")
                elif k_index == 1:
                    self._switchable_g_now_labels.switch_on(self._owner.g0_now_lbl)
                    self._k_storm_labels.switch_on(self._owner.k_very_quiet_lbl)
                    self._owner.expected_noise_lbl.setText("  S0 - S1 (<-120 dBm)  ")
                elif k_index == 2:
                    self._switchable_g_now_labels.switch_on(self._owner.g0_now_lbl)
                    self._k_storm_labels.switch_on(self._owner.k_quiet_lbl)
                    self._owner.expected_noise_lbl.setText("  S1 - S2 (-115 dBm)  ")
                elif k_index == 3:
                    self._switchable_g_now_labels.switch_on(self._owner.g0_now_lbl)
                    self._k_storm_labels.switch_on(self._owner.k_unsettled_lbl)
                    self._owner.expected_noise_lbl.setText("  S2 - S3 (-110 dBm)  ")
                elif k_index == 4:
                    self._switchable_g_now_labels.switch_on(self._owner.g0_now_lbl)
                    self._k_storm_labels.switch_on(self._owner.k_active_lbl)
                    self._owner.expected_noise_lbl.setText("  S3 - S4 (-100 dBm)  ")
                elif k_index == 5:
                    self._switchable_g_now_labels.switch_on(self._owner.g1_now_lbl)
                    self._k_storm_labels.switch_on(self._owner.k_min_storm_lbl)
                    self._owner.expected_noise_lbl.setText("  S4 - S6 (-90 dBm)  ")
                elif k_index == 6:
                    self._switchable_g_now_labels.switch_on(self._owner.g2_now_lbl)
                    self._k_storm_labels.switch_on(self._owner.k_maj_storm_lbl)
                    self._owner.expected_noise_lbl.setText("  S6 - S9 (-80 dBm)  ")
                elif k_index == 7:
                    self._switchable_g_now_labels.switch_on(self._owner.g3_now_lbl)
                    self._k_storm_labels.switch_on(self._owner.k_sev_storm_lbl)
                    self._owner.expected_noise_lbl.setText("  S9 - S20 (>-60 dBm)  ")
                elif k_index == 8:
                    self._switchable_g_now_labels.switch_on(self._owner.g4_now_lbl)
                    self._k_storm_labels.switch_on(self._owner.k_very_sev_storm_lbl)
                    self._owner.expected_noise_lbl.setText("  S20 - S30 (>-60 dBm)  ")
                elif k_index == 9:
                    self._switchable_g_now_labels.switch_on(self._owner.g5_now_lbl)
                    self._k_storm_labels.switch_on(self._owner.k_ex_sev_storm_lbl)
                    self._owner.expected_noise_lbl.setText("  S30+ (>>-60 dBm)  ")
                self._owner.expected_noise_lbl.switch_on()

                if a_index >= 0 and a_index < 8:
                    self._a_storm_labels.switch_on(self._owner.a_quiet_lbl)
                elif a_index >= 8 and a_index < 16:
                    self._a_storm_labels.switch_on(self._owner.a_unsettled_lbl)
                elif a_index >= 16 and a_index < 30:
                    self._a_storm_labels.switch_on(self._owner.a_active_lbl)
                elif a_index >= 30 and a_index < 50:
                    self._a_storm_labels.switch_on(self._owner.a_min_storm_lbl)
                elif a_index >= 50 and a_index < 100:
                    self._a_storm_labels.switch_on(self._owner.a_maj_storm_lbl)
                elif a_index >= 100 and a_index < 400:
                    self._a_storm_labels.switch_on(self._owner.a_sev_storm_lbl)

                index = self._owner.space_weather_data.geo_storm[6].index("was") + 1
                k_index_24_hmax = int(self._owner.space_weather_data.geo_storm[6][index])
                if k_index_24_hmax == 0:
                    self._switchable_g_today_labels.switch_on(self._owner.g0_today_lbl)
                elif k_index_24_hmax == 1:
                    self._switchable_g_today_labels.switch_on(self._owner.g0_today_lbl)
                elif k_index_24_hmax == 2:
                    self._switchable_g_today_labels.switch_on(self._owner.g0_today_lbl)
                elif k_index_24_hmax == 3:
                    self._switchable_g_today_labels.switch_on(self._owner.g0_today_lbl)
                elif k_index_24_hmax == 4:
                    self._switchable_g_today_labels.switch_on(self._owner.g0_today_lbl)
                elif k_index_24_hmax == 5:
                    self._switchable_g_today_labels.switch_on(self._owner.g1_today_lbl)
                elif k_index_24_hmax == 6:
                    self._switchable_g_today_labels.switch_on(self._owner.g2_today_lbl)
                elif k_index_24_hmax == 7:
                    self._switchable_g_today_labels.switch_on(self._owner.g3_today_lbl)
                elif k_index_24_hmax == 8:
                    self._switchable_g_today_labels.switch_on(self._owner.g4_today_lbl)
                elif k_index_24_hmax == 9:
                    self._switchable_g_today_labels.switch_on(self._owner.g5_today_lbl)

                val = int(self._owner.space_weather_data.ak_index[7][2].replace('.', ''))
                self._owner.sfi_lbl.setText(f"{val}")
                val = int(
                    [x[4] for x in self._owner.space_weather_data.sgas if "SSN" in x][0]
                )
                self._owner.sn_lbl.setText(f"{val:d}")

                for label, pixmap in zip(self.space_weather_labels,
                                         self._owner.space_weather_data.images):
                    label.pixmap = pixmap
                    label.make_transparent()
                    label.apply_pixmap()
            except Exception as e:  # This is a mess, so log an error and give up
                logging.error(f"Forecast update failure: {e}")
                pop_up(
                    self._owner,
                    title=Messages.SCREEN_UPDATE_FAIL,
                    text=Messages.SCREEN_UPDATE_FAIL_MSG
                ).show()

        elif not self._owner.closing:
            pop_up(self._owner, title=Messages.BAD_DOWNLOAD,
                   text=Messages.BAD_DOWNLOAD_MSG).show()
        self._owner.space_weather_data.remove_data()
