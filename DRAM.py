import pandas as pd
import splice as spl

if (__name__ == "__main__"):
    # 1 - load data
    chosen_data = "DRAM_OfferScraperOutput.pkl"
    data_in = pd.read_pickle("datasets/%s" % (chosen_data))

    # 2 - prepare for iteration
    file_name = chosen_data.split("_")[0]
    data_out = open("output/%s.csv" % (file_name), "w")

    # 3 - iterate through dataset and write output
    for i, row in data_in.iterrows():

        univeral_regexp = [
            # ####################
            # Space Separated Phrases
            # ####################
            "i\\. o\\. data",     # i. o. data
            "\w+\sEd(ition|\\.)",  # black edition
            "\d+ pcs/pack",        # 2pcs/pack
            "so(?=\s)?dimm",       # so-dimm
            "w/metal cover|(w/)?metal plate|w/diode|w/(?=\s)data",
            "w/(?=\s)?heat(?=\s)?sink",
            "w/o?\s?Cooling Fan|w/metal cover|w/metal plate",  # w/metal plate
            "(cooling\s)?fan(\sfor \w+)?|cooler fan",  # cooling fan for CPU
            "Wrong model|no(t in| longer) use|No Turbo",  #
            "(\w{4,20})\s(I{2,4})",  # Pentinum II
            # ####################
            # Space Separated Parameters
            # ####################
            "\d+(\\.\d+)?\s?(\"|\s?inch)",  # 2.5 inch
            "SATA(-|\s)?II{2,4}",           # sata III
            "class\s?\d+",                  # class10
            "TFBGA\s?\d+",                  # TFBGA2412
            "\d+(?=\s)?chips",              # 16 chips
            "CL\d+\\.\d+",                  # CL2.5
            "\d\\.\dv",                     # 2.2v
            "\d+(\\.\d+)?(\s)?[GMK]b?/s",   # 6.0Gb/s
            "\d+(\\.\d+)?(\s)?[gmk]bps",    # 8.0 Gbps
            # 4x2.0Mb Cache
            "(\d+\s?x\s?)?\d+(\\.\d+)?[MK]b?(\sL[123])?(\sCache)",
            "\d{1,3}(\\.\d+)?\s?(GT/s(ec)?)",         # 2.5 GT/s
            "[0-9\\.]{1,4}\s?(x\d+)?\s?([GMK](hz)?)",  # 20Ghz
            "\d{2,4}[MKb]?\sL[123]",                   # 2Mb L1
            "\d{2,4}(?=\s|-)?(bit)",                   # 64 bit
            ".*\\*.*",          # anything with *
            "\\(.*\\)",         # (anything in bracket)
            "\\[.*\\]",         # [anything in bracket]
            "\w+[-\\./]\w+",    # dot, slash, dash
            "\w+-\w+-\w+",      # 3-3-3
            # ####################
            # Phrases (non description)
            # ####################
            # "((?<=\\+)|(?<=\s)|(?<=^)|(?<=/))tin(?=\s|$|,|/|\\+)",
            "(heat(?=\s)?shield|hyper|EEC|Reg|Chip(s)|BGA|CSP|quad)",
            "(mobile|b[op]x|giant|gold|lead|dual|die|tray|tin)",
            "(legacy|sodimm|(s)?TSOP|stack(ed)?|layer|SDRAM|cache)",
            "(CPU|coated|Orig(inal)?|FBGA|for|sorting|down|grade)",
            "(scalable|bridge|north|south|type|core|duo|dual)",
            # ####################
            # Parameters (non description)
            # ####################
            "\d{1,4}[GMk]b?(?=\s)?x\d+",  # 12GBx8
            "\d{1,4}[GMk]b?",             # 12MB
            "\d{2,4}C",                   # 16C
            "(PC\d{3})",                  # PC1333
            "UHS-(I{1,2}|\d{1,2})",       # UHS-II
            "DC\d{1,2}V",                 # DC12V
            "\d+(\\.\d+)A",               # 0.58A
            "PC\d{4}",                    # PC1333
        ]
        universal_cut = [
            "\\(", "\\)",          # leftover brackets
            "(\s|^)-{1,10}(\s|$)",                         # dashes
            "((^|\s)(/|\\.|,|\\+))|((/|\\.|,|\\+)(\s|$))",  # floating ./,+
            # phrases
            "((?<=^)|(?<=\s))(set|(low)?profile|brand|marking|downgrade|half)(?=\s|$)",
            "((?<=^)|(?<=\s))(product|cross line|blank|mspd|\\(n)(?=\s|$)",
            "((?<=^)|(?<=\s))(record)(?=\s|$)",
        ]

        ########################################
        # a - parameter extraction
        ########################################
        unique_id = spl.extract_unique_id(row)

        group_name, group_name_descTags = spl.extract_group_name(
            row, ["\w+"], [], [], ["\\+"], [], [])

        brand, brand_descTags = spl.extract_brand(
            row,
            [[], []],
            univeral_regexp, [], [],
            universal_cut, [], [])

        part_number, part_number_descTags = spl.extract_part_number(
            row,
            [[], []],
            univeral_regexp, [],
            [
                "\w+[-\\./]\w+",    # dot, slash, dash
                "\w+-\w+-\w+"      # 3-3-3
            ],
            universal_cut,
            [                   # cut
                "(Smart Modular|HP|ramos|transcend|spectek|kingmax|corsair|dynet|elpida)",
                "(Infineon|nanya|mosel|Syncmax|no[nc]o[cn]a|series)",
                "(\\+?alcor|kreton|starex|excel|barun|ceon|iphone|sony)",
                "(sams[ui]ng|incomm|TransFlash|AMD|Phenom|enhanced)",
                "(skymedia|s-file|legend|taiwan|qimonda|tech|Infineon|celeron)",
                "(hagiwara|kodak|taikwa|renesas|intel|dane|elec|takiwa|muse)",
                "(Hynix|ETT|DDR3|micron|promoe|majors|novax)",
                "((?<=\s)|(?<=^)|(?<=\\+))(OEM|LG)(?=\s|$|,|\\+)",
                # "Lexar|micro|T-flash|Hynix|Novax|Brand|A-data|du[pl]{2}icated",
                "ball|bearing|PIII|P4|i7Pen|socket\s\w+|Pentium|PGA",
                # short words
                "((?<=\s)|(?<=^))\w{1,4}((?=\s)|(?=$))",
                "512Mx",
                "((?<=\s)|(?<=^))(128x8)?/667((?=\s)|(?=$))",
                "OEM\\(",
                "\\?new_brand=Elixir"
            ], [])

        descTags = spl.extract_description(
            row,
            [[], []],
            [
                # ####################
                # Space Separated Phrases
                # ####################
                "i\\. o\\. data",     # i. o. data
                "\w+\sEd(ition|\\.)",  # black edition
                "\d+ pcs/pack",        # 2pcs/pack
                "so(?=\s)?dimm",       # so-dimm
                "w/metal cover|(w/)?metal plate|w/diode|w/(?=\s)data",
                "w/(?=\s)?heat(?=\s)?sink",
                "w/o?\s?Cooling Fan|w/metal cover|w/metal plate",  # w/metal plate
                "(cooling\s)?fan(\sfor \w+)?|cooler fan",  # cooling fan for CPU
                "Wrong model|no(t in| longer) use|No Turbo",  #
                "(\w{4,20})\s(I{2,4})",  # Pentinum II
                # ####################
                # Space Separated Parameters
                # ####################
                "\d+(\\.\d+)?\s?(\"|\s?inch)",  # 2.5 inch
                "SATA(-|\s)?II{2,4}",           # sata III
                "class\s?\d+",                  # class10
                "TFBGA\s?\d+",                  # TFBGA2412
                "\d+(?=\s)?chips",              # 16 chips
                "CL\d+\\.\d+",                  # CL2.5
                "\d\\.\dv",                     # 2.2v
                "\d+(\\.\d+)?(\s)?[GMK]b?/s",   # 6.0Gb/s
                "\d+(\\.\d+)?(\s)?[gmk]bps",    # 8.0 Gbps
                # 4x2.0Mb Cache
                "(\d+\s?x\s?)?\d+(\\.\d+)?[MK]b?(\sL[123])?(\sCache)",
                "\d{1,3}(\\.\d+)?\s?(GT/s(ec)?)",         # 2.5 GT/s
                "[0-9\\.]{1,4}\s?(x\d+)?\s?([GMK](hz)?)",  # 20Ghz
                "\d{2,4}[MKb]?\sL[123]",                   # 2Mb L1
                "\d{2,4}(?=\s|-)?(bit)",                   # 64 bit
                ".*\\*.*",          # anything with *
                "\\(.*\\)",         # (anything in bracket)
                "\\[.*\\]",         # [anything in bracket]
                "\w+[-\\./]\w+",    # dot, slash, dash
                "\w+-\w+-\w+",      # 3-3-3
            ], [], [])

        descTags = descTags + group_name_descTags + \
            brand_descTags + part_number_descTags

        ########################################
        # X - testing
        ########################################
        # leading_string = [unique_id]
        # descTags = []
        # leading_string = [group_name]
        # descTags = group_name_descTags
        # descTags.append("\t||\t%s" % (row["Group_name"]))
        # leading_string = brand
        # descTags = brand_descTags
        # descTags.append("\t||\t%s" % (row["Brand"]))
        # leading_string = part_number
        # descTags = part_number_descTags
        # descTags.append("\t||\t%s" % (row["Part_number"]))
        # leading_string = ["%s\t\t||" % row["Description"]]
        # descTags = descTags
        # spl.write_test_file(data_out, leading_string, descTags, False)

        ########################################
        # b - deal with brand
        ########################################
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
