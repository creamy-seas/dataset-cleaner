import pandas as pd
import re
import numpy as np

# Part_number can have values: CD8067303327701, Tray, Duplicate or


def prepare_5_column_string(str1, str2, str3, str4, str5):
    """
    __ Parameters __
    str: string data to write in the 5 column file

    __ Description __
    prepares a tab separated string to write to file
    """

    sout = "%s,%s,%s,%s,%s \n" % (str1, str2, str3, str4, str5)
    return sout


def regular_expressions_extract(string_input, regular_expressions_list):
    """
    __ Parameters __
    [str] string_input: string to extract all matches from
    [array] regular_expressions_list: to search for

    __ Description __
    takes out all the regular expressions from a string input

    __ Return __
    string_output: without the regular expressions found
    match_array: array of all the matches
    """
    match_array = []
    # 1 - iterate through all rgular expressions supplied
    i = 0
    while(i < len(regular_expressions_list)):
        regexp = regular_expressions_list[i]
        # regexp = "((?<=\\+)|(?<=\s)|(?<=^)|(?<=/))" + \
        regexp = "((?<=\\+)|(?<=\s)|(?<=^))" + \
            regexp + "(?=\s|$|,|/|\\+)"

        # 2 - search for a matching description
        matchGroup = re.search(regexp, string_input, flags=re.I)

        if(matchGroup):
            # 3 - if found store and delete the value (regular escape to brackets)
            value = matchGroup.group()
            string_input = re.sub(re.escape(value), "",
                                  string_input, flags=re.I)
            match_array.append(value)
            i = i - 1           # stay on the same regexp for more matches found

        i = i + 1

    return string_input, match_array


def regular_expression_replace(string, remove_array, replace_array):
    """
    __ Parameters __
    [str] string: to change
    [array] remove: array of what to remove
    [array] replace: matching array of what to replace with

    __ Description __
    replace remove elements with replace elements

    __ Return __
    [str] string: everything is replaced
    """

    if(len(remove_array) != len(replace_array)):
        raise ValueError(
            "Remove and replace array for \"regular_expression_replace\" must be the same size")

    for i in range(0, len(remove_array)):
        string = re.sub(
            remove_array[i], replace_array[i], string, flags=re.I, count=10)

    return string


def trim_white_space(string):
    """
    __ Parameters __
    string to trim white space from

    __ Description __
    trip from start and end of string

    __ Return __
    trimmed string or the orignal
    """

    # 1 - search for spaces
    groupMatch = re.match("^(\s*)(.*)(\s*)$", string)
    if(groupMatch):
        return groupMatch.group(2)
    else:
        return string
    # groupMatch = re.match("(\b)(\w+)(\b)", string)
    # if(groupMatch):
    #     return groupMatch.group(2)
    # else:
    #     return string


def extract_unique_id(row):
    """
    __ Parameters __
    row: row to extract from

    __ Description __
    extracts  "Unique_ID" of device

    __ Return __
    [str] Unique_ID
    """

    # 1 - extract values
    unique_id = row["Unique_ID"]

    # 2 - handle unusual situations
    if(len(unique_id.split(" ")) != 1):
        print(row)
        print("----------------------------------------")
        print("[Row %i]\t \"Unique_ID\" is not unique." % (i))
        input("\n\t\tPress key to continue...")

    return unique_id


def extract_group_name(row, regexp_description, regexp_desc_extra, regexp_desc_cut, regexp_junk, regexp_junk_extra, regexp_junk_cut):
    """
    __ Parameters __
    row
    regexp_description: description tags to look for
    regexp_desc_extra: extra description tags to add
    regexp_desc_cut: description tags to remove
    regexp_junk: regexp to clean from final string
    regexp_junk_exta: extra clean variables
    regexp_junk_cut: clean variables to remove

    __ Description __
    extracts "Group_name" of device and description tags that are mixed in

    __ Return __
    [str] Group_name
    [array] Description tags
    """

    group_name_input = row["Group_name"]
    regexp_description = ["[0-9]{1,3}[MK]\sCache",  # 2M cache
                          "[0-9]{1,2}x\s\w+",       # 2x L34234
                          "LGA775",                 # LGA775
                          "[0-9]+[Mm][Hh][Zz]",     # 800MHz
                          "[0-9]{2,4}pins",         # 777pins
                          "\w+\s[bB][iI][tT]"  # 64 bit
                          ]
    # add and remove regexp
    regexp_description = regexp_desc_extra + regexp_description
    for i in regexp_desc_cut:
        regexp_description.remove(i)
    regexp_junk = regexp_junk_extra + regexp_junk
    for i in regexp_junk_cut:
        regexp_junk.remove(i)

    # 1 - extract descriptions tags
    group_name, descTags = regular_expressions_extract(
        group_name_input, regexp_description)

    # 2 - cleanup junk
    group_name = regular_expression_replace(
        group_name, regexp_junk, [""] * len(regexp_junk))

    # 3 - remove whitespace
    group_name = trim_white_space(group_name)

    return group_name, descTags


def extract_description(row, regexp_replace, regexp_description, regexp_desc_extra, regexp_desc_cut):
    """
    __ Parameters __
    row
    [[arr],[arr]] regexp_replace: things to replace before main run
    [arr] regexp_description: description tags to look for
    [arr] regexp_desc_extra: extra description tags to add
    [arr] regexp_desc_cut: description tags to remove

    __ Description __
    extract description tags

    __ Return __
    [array] Description tags
    """

    description_input = row["Description"]
    # add and remove description tags before run
    regexp_description = regexp_desc_extra + regexp_description
    for i in regexp_desc_cut:
        regexp_description.remove(i)
    regexp_description.append("\w+")  # add whole words tags

    # 1 replace common errors
    counter = 0
    for i in regexp_replace[0]:
        description_input = regular_expression_replace(
            description_input, i, regexp_replace[0][counter])
        counter = counter + 1

    # 2 - extract descriptions
    temp, descTags = regular_expressions_extract(
        description_input, regexp_description)

    return descTags


def extract_brand(row, regexp_replace, regexp_description, regexp_desc_extra, regexp_desc_cut, regexp_junk, regexp_junk_extra, regexp_junk_cut):
    """
    __ Parameters __
    row
    [[arr],[arr]] regexp_replace: things to replace before main run
    [arr] regexp_description: description tags to look for
    [arr] regexp_desc_extra: extra description tags to add
    [arr] regexp_desc_cut: description tags to remove
    [arr] regexp_junk: regexp to clean from final string
    [arr] regexp_junk_exta: extra clean variables
    [arr] regexp_junk_cut: clean variables to remove

    __ Description __
    extracts "Brand" of device and description tags that are mixed in

    __ Return __
    [array] Brand
    [array] Description tags
    """

    brand_input = row["Brand"]
    # add and remove description tags before run
    regexp_description = regexp_desc_extra + regexp_description
    for i in regexp_desc_cut:
        regexp_description.remove(i)
    regexp_junk = regexp_junk_extra + regexp_junk
    for i in regexp_junk_cut:
        regexp_junk.remove(i)

    # 1 - replace common errors
    brand_input = regular_expression_replace(
        brand_input, regexp_replace[0], regexp_replace[1])

    # 2 - extract descriptions
    brand, descTags = regular_expressions_extract(
        brand_input, regexp_description)

    # 3 - cleanup junk
    brand = regular_expression_replace(
        brand, regexp_junk, [""] * len(regexp_junk))

    # 4 - remove whitespace
    brand = brand.split(" ")
    brand = [trim_white_space(i) for i in brand if (i != "")]

    return brand, descTags


def extract_part_number(row, regexp_replace, regexp_description, regexp_desc_extra, regexp_desc_cut, regexp_junk, regexp_junk_extra, regexp_junk_cut):
    """
    __ Parameters __
    row
    [[arr],[arr]] regexp_replace: things to replace before main run
    regexp_description: description tags to look for
    regexp_desc_extra: extra description tags to add
    regexp_desc_cut: description tags to remove
    regexp_junk: regexp to clean from final string
    regexp_junk_exta: extra clean variables
    regexp_junk_cut: clean variables to remove

    __ Description __
    extracts "Part_number" of device and description tags that are mixed in

    __ Return __
    [array] Part_number(s)
    [array] Description tags
    """

    part_number_input = row["Part_number"]
    # add and remove description tags before run
    regexp_description = regexp_desc_extra + regexp_description
    for i in regexp_desc_cut:
        regexp_description.remove(i)
    regexp_junk = regexp_junk_extra + regexp_junk
    for i in regexp_junk_cut:
        regexp_junk.remove(i)

    # 1 - replace common errors
    part_number_input = regular_expression_replace(
        part_number_input, regexp_replace[0], regexp_replace[1])

    # 2 - extract descriptions tags
    part_number, descTags = regular_expressions_extract(
        part_number_input, regexp_description)

    # 3 - clean junk
    part_number = regular_expression_replace(
        part_number, regexp_junk, [""] * len(regexp_junk))

    # 4 - remove whitespace
    part_number = part_number.split(" ")
    part_number = [trim_white_space(i) for i in part_number if (i != "")]

    return part_number, descTags


def write_test_file(fout, leading_string, descTags, reverse):
    """
    __ Parameters __
    fout: file to write to
    [array] leading_string: array of leading string to write
    [array] descTags: description tags to follow
    [bool] reverse: flip order of writting description

    __ Description __
    write to output file for  debugging purposes
    """
    sout = []

    for i in leading_string:
        sout.append("%s\t" % (i))
    sout.append("\t\t")

    if (reverse):
        descTags = np.flip(descTags)

    for i in descTags:
        sout.append("\t\t%s" % (i))

    sout.append("\n")

    fout.write("".join(sout))


####################
# global parameters for seach
####################
regexp_description = ["\\(.+\\)",
                      "Tray",
                      "Du[pl]{2}icated",
                      "Wrong model",
                      "no longer use",
                      "Mobile",
                      "Tualatin",
                      "No Turbo",
                      "(\s|^)B[op]x",
                      "\w+\sEdition",
                      "(Cooling\s)?Fan(\sfor \w+)?",
                      "Cooler Fan",
                      "w/o Cooling Fan",
                      "not\s(in\s)?use",
                      "celeron",
                      "Nocona(\sSeries)?",
                      "series",
                      "¥þ§Ó",
                      "\sSocket",
                      "\sLGA775",
                      "\sd+[GMK]b?/s",                 # 100M/s
                      "\s\d{1,3}[GBk]b?\s",            # 12M
                      "\d+(\s)?x|x(\s)?\d+",           # x8 or 8 x
                      "DDR[0-9]\s",                     # DDR3
                      "\d+(\\.\d+)?(\s)?[gmk]bps",     # 8.0Gbps
                      "\d+[MKb]+(\sL[123])?(\sCache)",  # 2Mb cache
                      "\d+[MKb]?\sL[123]",              # 2Mb L1
                      "cache",
                      "\sS[LU]\w+",                # SL234
                      "i\d[-\s]\w+",               # i7-21421
                      "(\d+)[\s-]?(bit)",          # 64 bit
                      "\w{0,2}1333",               # PC1333
                      "(\w{4,20})\s(I{2,4})",      # Pentinum II
                      "E[0-9]-\w{4,6}",            # E2-12421
                      "(\d+\\.\d+)\s?(GT/s[ec]?)",  # 2.5 GT/s
                      "[0-9]{1,2}x\s\w+",           # 2x L34234
                      "\d+[\s-]{1,2}pin(s)?",       # 123pins
                      "([0-9\\.]+)(\s?)([GMK]hz)",  # 20 Ghz
                      "[0-9]+[GMK](byte|bit|b)?",      # 2KB
                      "\b\w{1,2}\b",                # 2 characters
                      "\w+[\\.-/]\w+"               # dot, slash, dash
                      ]

regexp_junk = ["\\(\\)", "/", "orig", "\\[", "\\]", "-", "\++"]

# if (__name__ == "__main__"):

#     chosen_set = 1

#     # 1 - load data
#     datasets = ["CPU_OfferScraperOutput.pkl",
#                 "DRAM_OfferScraperOutput.pkl",
#                 "FlashCard_OfferScraperOutput.pkl",
#                 "Module_OfferScraperOutput.pkl",
#                 "SSD_OfferScraperOutput.pkl"]
#     chosen_data = datasets[chosen_set]
#     data_in = pd.read_pickle("datasets/%s" % (chosen_data))

#     # 2 - prepare for iteration
#     file_name = chosen_data.split("_")[0]
#     data_out = open("output/%s.csv" % (file_name), "w")

#     # 3 - iterate through dataset and write output
#     for i, row in data_in.iterrows():

#         ########################################
#         # a - parameter extraction
#         ########################################
#         unique_id = extract_unique_id(row)
#         data_out.write("%s\n" % unique_id)
#         # group_name, group_name_descTags = extract_group_name(
#         #     row, regexp_description, [], regexp_junk)

#         # brand, brand_descTags = extract_brand(
#         #     row, regexp_description, [], regexp_junk)

#         # part_number, part_number_descTags = extract_part_number(
#         #     row, regexp_description, ["\s\d+x",
#         #                               "Series",
#         #                               "Dual Core",
#         #                               "CPU",
#         #                               "for \w+",
#         #                               "AMD",
#         #                               "Intel",
#         #                               "\s\w\s"], regexp_junk)

#         # descTags = extract_description(
#         #     row, regexp_description, ["2 Duo"])

#         # descTags = descTags + group_name_descTags + \
#         #     brand_descTags + part_number_descTags

#         # ########################################
#         # # b - deal with brand
#         # ########################################
#         # sout = prepare_5_column_string(
#         #     brand,
#         #     "Brand",
#         #     group_name,
#         #     file_name,
#         #     unique_id)
#         # data_out.write(sout)

#         # ########################################
#         # # c - deal with part number
#         # ########################################
#         # for i in range(0, len(part_number)):
#         #     sout = prepare_5_column_string(
#         #         part_number[i],
#         #         "Part_number",
#         #         group_name,
#         #         file_name,
#         #         unique_id)
#         #     data_out.write(sout)

#         # ########################################
#         # # d - deal with description tags
#         # ########################################
#         # for i in range(0, len(descTags)):
#         #     sout = prepare_5_column_string(
#         #         descTags[i],
#         #         "Description",
#         #         group_name,
#         #         file_name,
#         #         unique_id)
#         #     data_out.write(sout)

#     data_out.close()
