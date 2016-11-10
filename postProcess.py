# -*- coding: utf-8 -*-
"""
Created on Tue May 24 10:41:50 2016

@author: dahoiv
"""

# import os
import util


def _process(folder, glioma_grades):
    util.setup(folder)
    params = ['Index_value', 'Global_index', 'Mobility', 'Selfcare', 'Activity', 'Pain', 'Anxiety', 'karnofsky']
    exclude_pid = [1307, 1461]
    (image_ids, qol) = util.get_image_id_and_qol(None, exclude_pid, glioma_grades=glioma_grades)
    result = util.post_calculations(image_ids)
    util.avg_calculation(result['all'], 'all', None, True, folder, save_sum=True)

    util.avg_calculation(result['img'], 'img', None, True, folder)

    (image_ids, qol) = util.get_image_id_and_qol('Index_value', exclude_pid, glioma_grades=glioma_grades)
    print(image_ids, len(image_ids))
    result = util.post_calculations(image_ids)
    util.calculate_t_test(result['all'], 1)

    for qol_param in params:
        (image_ids, qol) = util.get_image_id_and_qol(qol_param, exclude_pid)
        qol = [_temp * 100 for _temp in qol]
        print(image_ids)
        result = util.post_calculations(image_ids)
        for label in result:
            print(label)
            if label == 'img':
                continue
            util.avg_calculation(result[label], label + '_' + qol_param, qol, True, folder)


if __name__ == "__main__":
    folder = "RES_1b/"
    glioma_grades = [2, 3, 4]
    _process(folder, glioma_grades)

    folder = "RES_2b/"
    glioma_grades = [4]
    _process(folder, glioma_grades)

    folder = "RES_3b/"
    glioma_grades = [3, 4]
    _process(folder, glioma_grades)