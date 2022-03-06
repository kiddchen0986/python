import json
import os
import sys
import argparse
from collections import OrderedDict
import logging


def json_load(path, filename, data_type):
    if data_type not in filename:
        print("Error: please check the 1st argument is testsettings.json, 2nd is tesetlimits.json!")
        sys.exit(0)

    try:
        with open(os.path.join(path, data_type, filename)) as f_obj:
            settings = json.load(f_obj)
    except FileNotFoundError:
        print("Error: file {} is not found, please check file or path is correct!")
    else:
        return settings


def get_valid_test_settings(test_settings_json_data):
    register_items = ['groupName', 'comment', 'registers']
    test_settings_valid_data = test_settings_json_data.get("root").get("doc").get("data").get('registerGroups')

    if type(test_settings_valid_data) is list:
        for test_settings in test_settings_valid_data:
            for key in list(test_settings.keys()):
                if key not in register_items:
                    test_settings.pop(key)
                if test_settings['groupName'] == "#current_consumption_active_hp":
                    test_settings['groupName'] = "#active_hp"
                    test_settings['comment'] = "active_hp settings for the sensor"
                if test_settings['groupName'] == "#current_consumption_deep_sleep":
                    test_settings['groupName'] = "#deep_sleep"
                    test_settings['comment'] = "deep sleep settings for the sensor"

    return test_settings_json_data


def separate_checkboard_limits(limits_valid_data):
    groups = ['enabled', 'maxDeviation', 'pixelErrorsUpperLimit', 'subAreasErrorsUpperLimit', 'histogramDeviation',
              'medianDeltaLimit']
    checkboard_types = ['swingingCheckerboard', 'swingingInvertedCheckerboard']
    data = limits_valid_data.get('gradientCheckerboard')

    if data.get("swingingCheckerboard") is None:
        return

    flag_1 = False
    flag_2 = False
    if type(data) is dict:
        for key in list(data.keys()):
            swing_data = {}
            if key == "maxDeviation_usl_typ":
                data.pop(key)
            if key in checkboard_types:
                swing_data[key] = limits_valid_data['gradientCheckerboard'].pop(key)
                if not flag_1 and key == "swingingCheckerboard":
                    limits_valid_data[key] = {}
                    for group in groups:
                        limits_valid_data[key][group] = limits_valid_data['gradientCheckerboard'].get(group)
                        if limits_valid_data['gradientCheckerboard'].get(group) is None:
                            limits_valid_data[key][group] = False
                    limits_valid_data[key][key[8:].lower()] = swing_data[key]
                    flag_1 = True

                if not flag_2 and key == 'swingingInvertedCheckerboard':
                    limits_valid_data['swingingCheckerboard']['invertedCheckerboard'] = swing_data[key]
                    flag_2 = True


def handle_current_consumption_limits_group(limits_valid_data):
    try:
        if limits_valid_data.get("currentConsumption"):
            current_consumption_data = limits_valid_data.get("currentConsumption")
            ordered_dict = OrderedDict()

            key_items = ["rails", "samples"]
            for item in key_items:
                if current_consumption_data.get(item):
                    ordered_dict[item] = current_consumption_data.get(item)
                else:
                    ordered_dict[item] = "TBD - Don't define it in pt-doc"
                    print("**warning**: '{}' in currentConsumption is not defined in pt_doc limits json file".format(
                        item))

            if current_consumption_data.get("deep_sleep"):
                ordered_dict["deep_sleep"] = {}
                ordered_dict["deep_sleep"]["low"] = float(
                    current_consumption_data["deep_sleep"]["deep_sleep_current_total"]["low"]) * 0.001
                ordered_dict["deep_sleep"]["high"] = float(
                    current_consumption_data["deep_sleep"]["deep_sleep_current_total"]["high"]) * 0.001
                del current_consumption_data.get("deep_sleep")["deep_sleep_current_total"]
            if current_consumption_data.get("active_hp"):
                ordered_dict["active_hp"] = {}
                ordered_dict["active_hp"]["low"] = float(
                    current_consumption_data["active_hp"]["current_consumption_Active_HP"]["low"])
                ordered_dict["active_hp"]["high"] = float(
                    current_consumption_data["active_hp"]["current_consumption_Active_HP"]["high"])
                del current_consumption_data.get("active_hp")["current_consumption_Active_HP"]
            limits_valid_data["currentConsumption"] = dict(ordered_dict)
    except KeyError as e:
        logging.error(
            'KeyError {} happens {}, might be no test result, regard all nan'.format(e, sys._getframe().f_lineno))

    return limits_valid_data


def add_test_image_global_cfg(limits_valid_data, test_image_global_cfg):
    try:
        test_data_groups = ['gradientCheckerboard', 'swingingCheckerboard', 'imageConstant']
        for group in test_data_groups:
            ordered_dict = OrderedDict()
            if limits_valid_data.get(group):
                for sub_item in limits_valid_data[group].keys():
                    ordered_dict[sub_item] = limits_valid_data[group][sub_item]
                    if (sub_item == "histogramDeviation" and group != "imageConstant") or (
                            sub_item == "pixelErrorsUpperLimit" and group == "imageConstant"):
                        for item in test_image_global_cfg.keys():
                            ordered_dict[item] = test_image_global_cfg[item]
            limits_valid_data[group] = dict(ordered_dict)

    except KeyError as e:
        logging.error(
            'KeyError {} happens {}, might be no test result, regard all nan'.format(e, sys._getframe().f_lineno))

    return limits_valid_data


def get_valid_test_limts(limits_json_data):
    groups = ['gradientCheckerboard', 'swingingCheckerboard', 'imageConstant', 'currentConsumption', 'imageDrive',
              'moduleQuality2']
    limits_data_temp = limits_json_data.get("root").get("doc").get("testLimits")
    test_image_global_cfg = limits_json_data.get("root").get("doc").get("testLimits").get("testImageGlobalCfg")

    # remove some unuseful data group from raw limits data groups from json file
    if type(limits_data_temp) is dict:
        for key in list(limits_data_temp.keys()):
            if key not in groups:
                limits_data_temp.pop(key)

    # separate gradientCheckerboard into gradientCheckerboard and swingingCheckerboard
    # due to some pt_doc combined the swing and non-swing into one
    separate_checkboard_limits(limits_data_temp)

    # Ensure that these vector types are in the right order
    limits_valid_data = {}
    for group in groups:
        if limits_data_temp.get(group):
            limits_valid_data[group] = limits_data_temp[group]

    # Need to rearrange currentConsumption group test data due to its format in pt_doc is not what want in testdata file
    handle_current_consumption_limits_group(limits_valid_data)
    # Add subAreaGrps and subAreaGrpSizeRows if testImageGlobalCfg group in ptc_doc is existed
    if test_image_global_cfg:
        add_test_image_global_cfg(limits_valid_data, test_image_global_cfg)
    else:
        print("**Warning**: testImageGlobalCfg group is not defined in pt_doc limits json file!")

    return limits_valid_data


is_changed = False
flag_break_whole_loop = False  # True means break out all Recursive function below
def is_data_value_changed(origin_json_data, new_json_data):
    # Fix me: I think here need to do improvement, though almost most of difference can be detected, not sure 100% cover
    global is_changed
    global flag_break_whole_loop
    for key1, key2 in zip(sorted(origin_json_data.keys()), sorted(new_json_data.keys())):
        if len(origin_json_data.keys()) == len(new_json_data.keys()):
            if str(key1).strip() == str(key2).strip():
                data_type = type(origin_json_data[key1])
                type_is_same = (type(origin_json_data[key1]) == type(new_json_data[key2]))
                if type_is_same:
                    if data_type is dict:
                        is_data_value_changed(origin_json_data[key1], new_json_data[key2])
                        if flag_break_whole_loop:
                            break
                    elif data_type is list:
                        for x, y in zip(origin_json_data[key1], new_json_data[key2]):
                            if type(x) is dict:
                                for x1, y1 in zip(sorted(x.keys()), sorted(y.keys())):
                                    if x[x1] != y[y1]:
                                        is_changed = True
                                        print("{} and {} value is not equal".format(x, y))
                            elif type(x) is str:
                                if str(x).strip() != str(y).strip():
                                    is_changed = True
                                    print("The field {} and {} is not equal".format(key1, key2))
                            elif type(x) is int or type(x) is float:
                                if x != y:
                                    is_changed = True
                                    print("The field {} and {} is not equal".format(key1, key2))

                    elif data_type is str:
                        if str(origin_json_data[key1]).strip() != str(new_json_data[key2]).strip():
                            if key1 == "comment" and new_json_data.get('docVersion'):
                                continue   # ignore this difference
                            if 'TBD' in new_json_data[key2]:
                                print("Seems some new data fields are not defined, so will not to do over write")
                                is_changed = False
                                flag_break_whole_loop = True
                                break
                            print("{}'s value is different: they are '{}' and '{}' ".format(key1, origin_json_data[key1],
                                                                                            new_json_data[key2]))
                            is_changed = True
                    elif data_type is int or data_type is float:
                        if origin_json_data[key1] != new_json_data[key2]:
                            is_changed = True
                else:
                    if 'TBD' in new_json_data[key2]:
                        print("Seems some new data fields are not defined, so will not to do over write")
                        is_changed = False
                        flag_break_whole_loop = True
                        break
                    is_changed = True
                    print("The two type of data is different{} {}!".format(type(origin_json_data[key1]),
                                                                           type(new_json_data[key2])))
            else:
                print("Seems {} is new added".format(key2))
                is_changed = True
        else:
            if "subAreaGrps" in origin_json_data.keys() and "subAreaGrps" not in "new_json_data.keys()":
                print("Seems some new data fields are not defined, so will not to do over write")
                is_changed = False
                flag_break_whole_loop = True
                break
            print("There are different length data content between {} and {}".format(origin_json_data, new_json_data))
            is_changed = True

    return is_changed


if __name__ == '__main__':
    '''
    This is auto generate testdata json file <ProductType_foundry>_testdata_new.json, like fpc1553_s_cansemi_testdata_new.json
    the settings file name and limits file name need to be provided from pt_doc that you want to generate
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("settings_filename", help=r"settings file name in deliveries_mts\settings", type=str)
    parser.add_argument("limits_filename", help=r"file name of limits in deliveries_mts\limits", type=str)
    parser.add_argument("-o", "--overwrite", help="over write data using new generate file", type=bool, default=False)

    path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "pt_doc", "deliveries_mts"))
    if os.path.exists(path) is False:
        exit("pt_doc path is not correct, not found in sensor folder!")

    args = parser.parse_args()
    settings_filename = args.settings_filename
    limits_filename = args.limits_filename

    print("1. Check settings_filename and limits_filename are consistent......")
    if settings_filename[:-17] != limits_filename[:-15]:
        print("Error: please check if settings_filename and limits_filename is consistent!")
        sys.exit(0)

    print("2. Getting json data from {}......".format(settings_filename))
    test_settings_json_data = json_load(path, settings_filename, "settings")

    print("3. Getting json data from {}......".format(limits_filename))
    test_limits_json_data = json_load(path, limits_filename, "limits")

    print(r"4. Generating testdata json file {}testdata_new.json to sensor_settings\json\testdata......".format(
        settings_filename[:-17]))
    get_test_settings = get_valid_test_settings(test_settings_json_data)
    get_test_limits = get_valid_test_limts(test_limits_json_data)

    if test_settings_json_data.get("root").get("doc").get("data"):
        test_settings_json_data['root']['doc']["testLimits"] = get_test_limits

        json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, "json", "testdata"))
        filename = os.path.join(json_path, settings_filename[:-17] + "testdata_new.json")
        with open(file=filename, mode='w') as f:
            json.dump(test_settings_json_data, f, indent=4, sort_keys=False)

    # detect if overwrite data, here set default as False due to some group are updating, will do improvement in the
    # future, please see the function is_data_value_changed() for details.
    if args.overwrite:
        testdata_json_file_name = settings_filename[:-17] + "testdata.json"
        if testdata_json_file_name in os.listdir(json_path):
            origin_json_data = json_load(os.path.join(json_path, os.pardir), testdata_json_file_name, "testdata")
            new_json_data = test_settings_json_data
            print("\nCheck if needs to do over write...")
            if is_data_value_changed(origin_json_data, new_json_data):
                new_json_data["root"]["doc"]["header"]["docInfo"]["comment"] = \
                origin_json_data["root"]["doc"]["header"]["docInfo"]["comment"]
                with open(file=os.path.join(json_path, testdata_json_file_name), mode='w') as f:
                    json.dump(new_json_data, f, indent=4, sort_keys=False)
                os.remove(filename)
                print("Over write done!")
            else:
                print(
                    "Not to do over write, reasons: Not have data changed, "
                    "Or check if pt_doc missing some important data!")
        else:
            print("The testdata json file is not existed at all, cannot over write it!")

    print('\nFinished')
