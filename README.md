# Parsing Dataset files #

The set of programs, runs through the =.pkl= files and reads in all the information from `$SECTION`s:
- *Group_name*
- *Brand*
- *Part_number*
- *Description*

and creates an output file with the following lines to train a neural network
`$VALUE, $SECTION, Group_name, File_name, Unique_ID`

## Extracting the `$VALUES` ##
It's not a trivial task to take out the `$VALUES` from the relevant `$SECTIONS`, with a typical information being a jumble such as:

> Opteron 246 2000Mhz (940 pins) 64 bits

in the *Description* section and

> OS246B Box 800 Mhz 1M Cache

in the *Part_number* section. 

This results in two main tasks, which the program completes:
- Grouping related space-separated tags such as `64 bits` into a single `$VALUE`;
- Removing irrelevant tags that were mixed into incorrect sections. e.g. `Box` or `800 MHz` are removed from the *Part_number* section, since they don't belong there.

-------------------------------------------------------------------------------
# Description tags that the program extracts
- `i. o. data`
- `black edition`
- `2pcs/pack`
- `so-dimm`
- `w/ metal cover` `w/ metal plate` etc
- `cooling fan for CPU`
- `wrong model`
- `16 chips`
- `2.2V`
- `12 GB`
- `1200 MHz`
- `2.5 inch`
- `SATA III`
- `8.0 Gbps`
