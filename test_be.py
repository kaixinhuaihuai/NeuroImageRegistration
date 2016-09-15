# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 14:15:23 2016

@author: dahoiv
"""

import os
import nipype.interfaces.ants as ants
from os.path import basename
from os.path import splitext

import image_registration
import util
import do_img_registration_GBM


def _test_be(moving_image_id, reg):
    img = image_registration.img_data(moving_image_id, util.DATA_FOLDER, util.TEMP_FOLDER_PATH)
    img = image_registration.pre_process(img, False)

    resampled_file = img.pre_processed_filepath
    name = splitext(splitext(basename(resampled_file))[0])[0] + "_bet"

    reg.inputs.fixed_image = resampled_file
    reg.inputs.fixed_image_mask = img.label_inv_filepath
    reg.inputs.output_transform_prefix = util.TEMP_FOLDER_PATH + name
    reg.inputs.output_warped_image = util.TEMP_FOLDER_PATH + name + '_betReg.nii'
    transform = util.TEMP_FOLDER_PATH + name + 'InverseComposite.h5'

    print("starting be registration")
    reg.run()
    print("Finished be registration")

    img.init_transform = transform

    reg_volume = util.transform_volume(resampled_file, transform)

    mult = ants.MultiplyImages()
    mult.inputs.dimension = 3
    mult.inputs.first_input = reg_volume
    mult.inputs.second_input = image_registration.TEMPLATE_MASK
    mult.inputs.output_product_image = img.pre_processed_filepath
    mult.run()

    util.generate_image(img.pre_processed_filepath, image_registration.TEMPLATE_VOLUME)


def test_be(moving_image_ids, reg):
    for moving_image_id in moving_datasets_ids:
        _test_be(moving_image_id, reg)


# pylint: disable= invalid-name
if __name__ == "__main__":
    os.nice(19)
    util.setup("GBM_test/", "GBM")
    moving_datasets_ids = do_img_registration_GBM.find_images()[:5]

    reg = ants.Registration()
    # reg.inputs.args = "--verbose 1"
    reg.inputs.collapse_output_transforms = True
    reg.inputs.moving_image = image_registration.TEMPLATE_VOLUME

    reg.inputs.num_threads = 8
    reg.inputs.initial_moving_transform_com = True

    reg.inputs.transforms = ['Rigid', 'Affine']
    reg.inputs.metric = ['MI', 'MI']
    reg.inputs.radius_or_number_of_bins = [32, 32]
    reg.inputs.metric_weight = [1, 1]
    reg.inputs.convergence_window_size = [5, 5]
    reg.inputs.number_of_iterations = ([[10000, 10000, 10000, 10000],
                                        [10000, 10000, 10000, 10000]])
    reg.inputs.convergence_threshold = [1.e-6]*2
    reg.inputs.shrink_factors = [[9, 5, 3, 1], [9, 5, 3, 1]]
    reg.inputs.smoothing_sigmas = [[8, 4, 1, 0], [8, 4, 1, 0]]
    reg.inputs.transform_parameters = [(0.25,), (0.25,)]
    reg.inputs.sigma_units = ['vox']*2
    reg.inputs.use_estimate_learning_rate_once = [True, True]

    reg.inputs.write_composite_transform = True
    reg.output_inverse_warped_image = True

    # test 0
    util.setup("GBM_test_0/", "GBM")
    if not os.path.exists(util.TEMP_FOLDER_PATH):
        os.makedirs(util.TEMP_FOLDER_PATH)
    image_registration.prepare_template(image_registration.TEMPLATE_VOLUME,
                                        image_registration.TEMPLATE_MASK)
    test_be(moving_datasets_ids, reg)

    # test 1
    util.setup("GBM_test_1/", "GBM")
    if not os.path.exists(util.TEMP_FOLDER_PATH):
        os.makedirs(util.TEMP_FOLDER_PATH)
    image_registration.prepare_template(image_registration.TEMPLATE_VOLUME,
                                        image_registration.TEMPLATE_MASK)
    reg.inputs.number_of_iterations = ([[10000, 5000, 1000, 500],
                                        [10000, 5000, 1000, 500]])
    test_be(moving_datasets_ids, reg)

    # test 2
    util.setup("GBM_test_2/", "GBM")
    if not os.path.exists(util.TEMP_FOLDER_PATH):
        os.makedirs(util.TEMP_FOLDER_PATH)
    image_registration.prepare_template(image_registration.TEMPLATE_VOLUME,
                                        image_registration.TEMPLATE_MASK)
    reg.inputs.transform_parameters = [(0.75,), (0.75,)]
    test_be(moving_datasets_ids, reg)

    # test 3
    util.setup("GBM_test_3/", "GBM")
    if not os.path.exists(util.TEMP_FOLDER_PATH):
        os.makedirs(util.TEMP_FOLDER_PATH)
    image_registration.prepare_template(image_registration.TEMPLATE_VOLUME,
                                        image_registration.TEMPLATE_MASK)
    reg.inputs.transform_parameters = [(0.50,), (0.50,)]
    test_be(moving_datasets_ids, reg)

    # test 4
    util.setup("GBM_test_4/", "GBM")
    if not os.path.exists(util.TEMP_FOLDER_PATH):
        os.makedirs(util.TEMP_FOLDER_PATH)
    image_registration.prepare_template(image_registration.TEMPLATE_VOLUME,
                                        image_registration.TEMPLATE_MASK)
    reg.inputs.transform_parameters = [(0.25,), (0.25,)]
    reg.inputs.radius_or_number_of_bins = [32, 5]
    reg.inputs.metric = ['MI', 'CC']
    test_be(moving_datasets_ids, reg)

    # test 5
    util.setup("GBM_test_5/", "GBM")
    if not os.path.exists(util.TEMP_FOLDER_PATH):
        os.makedirs(util.TEMP_FOLDER_PATH)
    image_registration.prepare_template(image_registration.TEMPLATE_VOLUME,
                                        image_registration.TEMPLATE_MASK)
    reg.inputs.radius_or_number_of_bins = [32, 32]
    reg.inputs.metric = ['MI', 'MI']
    reg.inputs.use_histogram_matching = [False, True]
    test_be(moving_datasets_ids, reg)
