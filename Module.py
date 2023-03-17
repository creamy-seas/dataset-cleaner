import pandas as pd
import splice as spl


if (__name__ == "__main__"):
    # 1 - load data
    chosen_data = "Module_OfferScraperOutput.pkl"
    data_in = pd.read_pickle("datasets/%s" % (chosen_data))

    # 2 - prepare for iteration
    file_name = chosen_data.split("_")[0]
    data_out = open("output/%s.csv" % (file_name), "w")

    # 3 - iterate through dataset and write output
    for i, row in data_in.iterrows():

        univeral_regexp = [
            # Universal
            # space separated phrases
            "i\\. o\\. data",                                     # i. o. data
            "\w+\sEdition",                           # black edition
            "\d+ pcs/pack",                           # 2pcs/pack
            "so(?=\s)?dimm",                          # so-dimm
            "w/metal cover|(w/)?metal plate|w/diode",  # w/metal cover
            "w/(?=\s)?heat(?=\s)?sink",                # w/heatsink
            "w/(?=o )Cooling Fan|w/metal cover|w/metal plate",  # w/metal plate
            "(cooling\s)?fan(\sfor \w+)?|cooler fan",  # cooling fan for CPU
            "Wrong model|no longer use|No Turbo",      #
            # space separated parameters
            "class\s?\d+",                  # class10
            "TFBGA\s?\d+",      # TFBGA2412
            "\d+(?=\s)?chips",  # 16 chips
            "\w+[-\\./]\w+",    # dot, slash, dash
            "\w+-\w+-\w+",      # 3-3-3
            "((?<=\s)|(?<=^)|(?<=\\())CL\d+\\.\d+(?=\s|$|,)",  # CL2.5
            "\d\\.\dv",                                        # 2.2v
            ".*\\*.*",                   # anything with *
            "\\(.*\\)",         # (anything in bracket)
            "\\[.*\\]",          # [anything in bracket]
            # Universal end
            #
            # phrases
            "((?<=^)|(?<=\s))(heat(?=\s)?shield|coated|Orig(inal)?|FBGA|hyper|EEC|Reg|Chip(s)|BGA|CSP|quad)(?=\s|$)",
            "((?<=^)|(?<=\s))(mobile|box|giant|tin|gold|lead)(?=\s|$)",
            "retail|bulk",      #
            "dual|die",         #
            "legacy|sodimm|(s)?TSOP|stack(ed)?|layer|SDRAM",
            #
            # parameters
            # 12GBx8
            "((?<=\s)|(?<=/)|(?<=^)|(?<=\\+))(\d+[GMk]b?)(?=\s)?x\d+(?=\s|$|,|\\+|/)",
            "((?<=\s)|(?<=^))(\d+[GMk]b?)(?=\s|$|,|x)",  # 12MB
            "(?<=\s)?(\d+C)(?=\s|$)",                    # 16C
            "(?<=\s)(PC\d{3})(?=\s|$)",                  # PC1333
            "UHS-(I{1,2}|\d{1,2})",                      # UHS-II
        ]
        universal_cut = [
            "\\(", "\\)",          # leftover brackets
            "(\s|^)-{1,10}(\s|$)",                         # dashes
            "((^|\s)(/|\\.|,|\\+))|((/|\\.|,|\\+)(\s|$))",  # floating ./,+
            # phrases
            "((?<=^)|(?<=\s))(set|(low)?profile|brand|marking|downgrade|half|product|cross line|blank)(?=\s|$)",
            "mspd|\\(n"
        ]

        ########################################
        # a - parameter extraction
        ########################################
        unique_id = spl.extract_unique_id(row)

        group_name, group_name_descTags = spl.extract_group_name(
            row, ["\w+"], [], [], ["\\+"], [], [])

        brand, brand_descTags = spl.extract_brand(
            row,
            [                   # replace
                ["[Ee]lpida[Nn]anya", "die", "org",
                    "\\(|\\)"],
                ["Elpida Nanya", "die", "orig", " "]
            ],
            univeral_regexp,
            [], [],
            universal_cut,
            [                   # cut
                "400 mil|3rd",
                "((?<=^)|(?<=\s))(on|to|no|bit|from)(?=\s|$)",
                "((?<=\s)|(?<=^))\w{1}((?=\s)|(?=$))"  # short words
            ], [])

        part_number, part_number_descTags = spl.extract_part_number(
            row,
            univeral_regexp,
            [
                # "\\(|\\)",
                "(°ïÅ|¦¡)",
                "((?<=\s)|(?<=^))\w{1,2}((?=\s)|(?=$))",  # short words
                "((?<=^)|(?<=\s))(long|dimm|OEM|DDR2|16chip|>>>|3rd|[VA]-DATA)(?=\s|$)"
            ],
            [
                "\w+[-\\./]\w+",    # dot, slash, dash
                "\w+-\w+-\w+"      # 3-3-3
            ],
            universal_cut,
            [                   # cut
                "\\+",
                # brands
                "Smart Modular|HP|ramos|transcend|spectek|kingmax|corsair|dynet|elpida",
                "Infineon|nanya|mosel|Syncmax",
                "alcor|kreton|starex|excel|barun|ceon|iphone|sony|whie",
                "\\+Alcor|sams[ui]ng|incomm|TransFlash"
            ], [])

        descTags = spl.extract_description(
            row,
            [["SO DIMM"],
             ["SO-DIMM"]],
            [],
            [
                # Universal
                # space separated phrases
                "i\\. o\\. data",                                     # i. o. data
                "\w+\sEdition",                           # black edition
                "\d+ pcs/pack",                           # 2pcs/pack
                "so(?=\s)?dimm",                          # so-dimm
                "w/metal cover|(w/)?metal plate|w/diode",  # w/metal cover
                "w/(?=\s)?heat(?=\s)?sink",                # w/heatsink
                "w/(?=o )Cooling Fan|w/metal cover|w/metal plate",  # w/metal plate
                "(cooling\s)?fan(\sfor \w+)?|cooler fan",  # cooling fan for CPU
                "Wrong model|no longer use|No Turbo",      #
                # space separated parameters
                "class\s?\d+",                  # class10
                "TFBGA\s?\d+",      # TFBGA2412
                "\d+(?=\s)?chips",  # 16 chips
                "\w+[-\\./]\w+",    # dot, slash, dash
                "\w+-\w+-\w+",      # 3-3-3
                "((?<=\s)|(?<=^)|(?<=\\())CL\d+\\.\d+(?=\s|$|,)",  # CL2.5
                "\d\\.\dv",                                        # 2.2v
                ".*\\*.*",                   # anything with *
                "\\(.*\\)",         # (anything in bracket)
                "\\[.*\\]",          # [anything in bracket]
                # Universal end
            ],
            [])

        descTags = descTags + group_name_descTags + \
            brand_descTags + part_number_descTags

        ########################################
        # X - testing
        ########################################
        # leading_string = ["%s\t\t||" % row["Description"]]
        # # leading_string = part_number
        # descTags = descTags
        # # descTags.append("\t||\t%s" % (row["Part_number"]))
        # # descTags.append("\t||\t%s" % (row["Part_number"]))
        # # descTags.append("\t||\t%s" % (row["Description"]))
        # spl.write_test_file(data_out, leading_string, descTags, False)

        # ########################################
        # # b - deal with brand
        # ########################################
        for i in brand:
            if(i != ""):
                sout = spl.prepare_5_column_string(
                    i,
                    "Brand",
                    group_name,
                    file_name,
                    unique_id)
                data_out.write(sout)

        # ########################################
        # # c - deal with part number
        # ########################################
        for i in part_number:
            if(i != ""):
                sout = spl.prepare_5_column_string(
                    i,
                    "Part_number",
                    group_name,
                    file_name,
                    unique_id)
                data_out.write(sout)

        # ########################################
        # # d - deal with description tags
        # ########################################
        for i in descTags:
            if(i != ""):
                sout = spl.prepare_5_column_string(
                    i,
                    "Description",
                    group_name,
                    file_name,
                    unique_id)
                data_out.write(sout)
    data_out.close()
