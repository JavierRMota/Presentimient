# -*- coding: utf-8 -*-
"""
Copyright (c) 2022-2023 Alejandro Ramsés D'León.

This file is part of Presentiment Project.
See https://github.com/Ramses-Dleon/Presentimiento for further info.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import pandas

# ? Both functions take plain text and transform it to lists, maybe is better to just take lists directly

def export_CSV_phys(
        str_session_id,
        str_phys_trial_id,
        str_phys_instance_id,
        str_skin_conductance_values,
        str_skin_conductance_timestamp,
        str_skin_conductance_media,
        str_skin_conductance_sd,
        str_skin_conductance_Z,
        str_skin_conductance_f,
        str_heart_rate_values,
        str_heart_rate_timestamp,
        str_heart_rate_media,
        str_heart_rate_sd,
        str_heart_rate_Z,
        str_heart_rate_f,
        str_brainwaves_values,
        str_brainwaves_timestamp,
        str_brainwaves_media,
        str_brainwaves_sd,
        str_brainwaves_Z,
        str_brainwaves_f,
        save_path_name):
    # & Convert string to list
    list_session_id = str_session_id.split("\n")
    list_phys_trial_id = str_phys_trial_id.split("\n")
    list_phys_instance_id = str_phys_instance_id.split("\n")
    list_skin_conductance_values = str_skin_conductance_values.split("\n")
    list_skin_conductance_timestamp = str_skin_conductance_timestamp.split(
        "\n")
    list_skin_conductance_media = str_skin_conductance_media.split("\n")
    list_skin_conductance_sd = str_skin_conductance_sd.split("\n")
    list_skin_conductance_Z = str_skin_conductance_Z.split("\n")
    list_skin_conductance_f = str_skin_conductance_f.split("\n")
    list_heart_rate_values = str_heart_rate_values.split("\n")
    list_heart_rate_timestamp = str_heart_rate_timestamp.split("\n")
    list_heart_rate_media = str_heart_rate_media.split("\n")
    list_heart_rate_sd = str_heart_rate_sd.split("\n")
    list_heart_rate_Z = str_heart_rate_Z.split("\n")
    list_heart_rate_f = str_heart_rate_f.split("\n")
    list_brainwaves_values = str_brainwaves_values.split("\n")
    list_brainwaves_timestamp = str_brainwaves_timestamp.split("\n")
    list_brainwaves_media = str_brainwaves_media.split("\n")
    list_brainwaves_sd = str_brainwaves_sd.split("\n")
    list_brainwaves_Z = str_brainwaves_Z.split("\n")
    list_brainwaves_f = str_brainwaves_f.split("\n")
    # & Remove first line in each of the session data lists
    del list_phys_trial_id[0]
    del list_phys_instance_id[0]
    del list_skin_conductance_values[0]
    del list_skin_conductance_timestamp[0]
    del list_skin_conductance_media[0]
    del list_skin_conductance_sd[0]
    del list_skin_conductance_Z[0]
    del list_skin_conductance_f[0]
    del list_heart_rate_values[0]
    del list_heart_rate_timestamp[0]
    del list_heart_rate_media[0]
    del list_heart_rate_sd[0]
    del list_heart_rate_Z[0]
    del list_heart_rate_f[0]
    del list_brainwaves_values[0]
    del list_brainwaves_timestamp[0]
    del list_brainwaves_media[0]
    del list_brainwaves_sd[0]
    del list_brainwaves_Z[0]
    del list_brainwaves_f[0]
    # & Convert list to series
    ser_session_id = pandas.Series(list_session_id, name='Session ID [S]:')
    ser_phys_trial_id = pandas.Series(list_phys_trial_id, name='Trial ID [n]:')
    ser_phys_instance_id = pandas.Series(
        list_phys_instance_id, name='Instance ID [i]:')
    ser_skin_conductance_values = pandas.Series(
        list_skin_conductance_values, name='Skin Conductance Values[xi]:')
    ser_skin_conductance_timestamp = pandas.Series(
        list_skin_conductance_timestamp, name='Skin Conductance Timestamp[t_xi]:')
    ser_skin_conductance_media = pandas.Series(
        list_skin_conductance_media, name='Skin Conductance Media[mx_paa]:')
    ser_skin_conductance_sd = pandas.Series(
        list_skin_conductance_sd, name='Skin Conductance SD [sx_paa]:')
    ser_skin_conductance_Z = pandas.Series(
        list_skin_conductance_Z, name='Skin Conductance Z [Z_xi]:')
    ser_skin_conductance_f = pandas.Series(
        list_skin_conductance_f, name='Skin Conductance f [f_xi]:')
    ser_heart_rate_values = pandas.Series(
        list_heart_rate_values, name='Heart Rate Values [yi]:')
    ser_heart_rate_timestamp = pandas.Series(
        list_heart_rate_timestamp, name='Heart Rate Timestamp [t_yi]:')
    ser_heart_rate_media = pandas.Series(
        list_heart_rate_media, name='Heart Rate Media [my_paa]:')
    ser_heart_rate_sd = pandas.Series(
        list_heart_rate_sd, name='Heart Rate SD [sy_paa]:')
    ser_heart_rate_Z = pandas.Series(
        list_heart_rate_Z, name='Heart Rate Z [Z_yi]:')
    ser_heart_rate_f = pandas.Series(
        list_heart_rate_f, name='Heart Rate f [f_yi]:')
    ser_brainwaves_values = pandas.Series(
        list_brainwaves_values, name='Brainwaves Values [zi]:')
    ser_brainwaves_timestamp = pandas.Series(
        list_brainwaves_timestamp, name='Brainwaves Timestamp [t_zi]:')
    ser_brainwaves_media = pandas.Series(
        list_brainwaves_media, name='Brainwaves Media [mz_paa]:')
    ser_brainwaves_sd = pandas.Series(
        list_brainwaves_sd, name='Brainwaves SD [sz_paa]:')
    ser_brainwaves_Z = pandas.Series(
        list_brainwaves_Z, name='Brainwaves Z [Z_zi]:')
    ser_brainwaves_f = pandas.Series(
        list_brainwaves_f, name='Brainwaves f [f_zi]:')
    # & Generate dataframe by concatenating the series
    df = pandas.concat([ser_session_id,
                        ser_phys_trial_id,
                        ser_phys_instance_id,
                        ser_skin_conductance_values,
                        ser_skin_conductance_timestamp,
                        ser_skin_conductance_media,
                        ser_skin_conductance_sd,
                        ser_skin_conductance_Z,
                        ser_skin_conductance_f,
                        ser_heart_rate_values,
                        ser_heart_rate_timestamp,
                        ser_heart_rate_media,
                        ser_heart_rate_sd,
                        ser_heart_rate_Z,
                        ser_heart_rate_f,
                        ser_brainwaves_values,
                        ser_brainwaves_timestamp,
                        ser_brainwaves_media,
                        ser_brainwaves_sd,
                        ser_brainwaves_Z,
                        ser_brainwaves_f], axis=1)
    # ? "header=False" if want to remove headers
    df.to_csv(save_path_name, index=False, encoding='ANSI')
    print(save_path_name)


def export_CSV(
        str_start_at,
        str_finish_at,
        str_onset_at,
        str_skin_conductance_D,
        str_heart_rate_D,
        str_brainwaves_D,
        str_trial_id,
        str_stimulus_id,
        str_time_start_trial,
        str_onset_to_trial,
        str_seconds_end_trial,
        str_dur_after_interval,
        str_dur_before_interval,
        str_time_end_trial,
        str_skin_conductance_Fn,
        str_heart_rate_Fn,
        str_brainwaves_Fn,
        save_path_name):
    # & Convert string to list
    list_start_at = str_start_at.split("\n")
    list_finish_at = str_finish_at.split("\n")
    list_onset_at = str_onset_at.split("\n")
    list_skin_conductance_D = str_skin_conductance_D.split("\n")
    list_heart_rate_D = str_heart_rate_D.split("\n")
    list_brainwaves_D = str_brainwaves_D.split("\n")
    list_trial_id = str_trial_id.split("\n")
    list_stimulus_id = str_stimulus_id.split("\n")
    list_time_start_trial = str_time_start_trial.split("\n")
    list_onset_to_trial = str_onset_to_trial.split("\n")
    list_seconds_end_trial = str_seconds_end_trial.split("\n")
    list_dur_after_interval = str_dur_after_interval.split("\n")
    list_dur_before_interval = str_dur_before_interval.split("\n")
    list_time_end_trial = str_time_end_trial.split("\n")
    list_skin_conductance_Fn = str_skin_conductance_Fn.split("\n")
    list_heart_rate_Fn = str_heart_rate_Fn.split("\n")
    list_brainwaves_Fn = str_brainwaves_Fn.split("\n")
    # & Remove first line in each of the session data lists
    del list_trial_id[0]
    del list_stimulus_id[0]
    del list_time_start_trial[0]
    del list_onset_to_trial[0]
    del list_seconds_end_trial[0]
    del list_dur_after_interval[0]
    del list_dur_before_interval[0]
    del list_time_end_trial[0]
    del list_skin_conductance_Fn[0]
    del list_heart_rate_Fn[0]
    del list_brainwaves_Fn[0]
    # & Convert list to series
    ser_start_at = pandas.Series(list_start_at, name='Session started at:')
    ser_finish_at = pandas.Series(list_finish_at, name='Session finished at:')
    ser_onset_at = pandas.Series(list_onset_at, name='First trial started at:')
    ser_skin_conductance_D = pandas.Series(
        list_skin_conductance_D, name='Skin conductance D [SUM(FnE)-SUM(FnN)]:')
    ser_heart_rate_D = pandas.Series(
        list_heart_rate_D, name='Heart rate D [SUM(FnE)-SUM(FnN)]:')
    ser_brainwaves_D = pandas.Series(
        list_brainwaves_D, name='Brainwaves D [SUM(FnE)-SUM(FnN)]:')
    ser_trial_id = pandas.Series(list_trial_id, name='Trial ID:')
    ser_stimulus_id = pandas.Series(list_stimulus_id, name='Stimulus ID:')
    ser_time_start_trial = pandas.Series(
        list_time_start_trial, name='Time at the start of trial:')
    ser_onset_to_trial = pandas.Series(
        list_onset_to_trial, name='First trial to end of this trial (s):')
    ser_seconds_end_trial = pandas.Series(
        list_seconds_end_trial, name='Duration of each trial (s):')
    ser_dur_after_interval = pandas.Series(
        list_dur_after_interval, name='Interval after of each trial (s):')
    ser_dur_before_interval = pandas.Series(
        list_dur_before_interval, name='Interval before of each trial (s):')
    ser_time_end_trial = pandas.Series(
        list_time_end_trial, name='Time at the end of trial:')
    ser_skin_conductance_Fn = pandas.Series(
        list_skin_conductance_Fn, name='Skin conductance Fn [SUM_fx_paa]:')
    ser_heart_rate_Fn = pandas.Series(
        list_heart_rate_Fn, name='Heart rate Fn [SUM_fy_paa]:')
    ser_brainwaves_Fn = pandas.Series(
        list_brainwaves_Fn, name='Brainwaves Fn [SUM_fz_paa]:')
    # & Generate dataframe by concatenating the series
    df = pandas.concat([ser_start_at,
                        ser_finish_at,
                        ser_onset_at,
                        ser_skin_conductance_D,
                        ser_heart_rate_D,
                        ser_brainwaves_D,
                        ser_trial_id,
                        ser_stimulus_id,
                        ser_time_start_trial,
                        ser_time_end_trial,
                        ser_dur_before_interval,
                        ser_dur_after_interval,
                        ser_seconds_end_trial,
                        ser_onset_to_trial,
                        ser_skin_conductance_Fn,
                        ser_heart_rate_Fn,
                        ser_brainwaves_Fn], axis=1)

    # ? "header=False" if want to remove headers
    df.to_csv(save_path_name, index=False, encoding='ANSI')
    print(save_path_name)
