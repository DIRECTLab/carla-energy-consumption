# Video Stuff

## Things to note about videos
- In DWARF_20230928142255845, DWARF_20230928142526510, only parts of the vehicles are shown
- In DWARF_20230928142432431, the truck at the beginning swerves into a different lane; make sure it is ignored
- The viewpoint changes significantly starting with DWARF_20230928144311791
- The intersection changes at DWARF_20231024150226248
- DWARF_20231024150305135 should not detect any vehicles because they are all in the wrong lane. If that's not the case, we might have issues with some of the neighboring videos as well
- I'm not sure if DWARF_20231026144020657 will take because the vehicles are already pretty far forward when the video starts

## splitall.py
This script splits the videos into frames, similar to the shell script you sent me but without any duplicates.

## offset_linreg.py
This script computes the lane offset for each vehicle (with sufficient data) in a CSV file. The following scaling factors (`--scale` option) will convert from pixels to meters:
- Videos from DWARF_20230928141733807 through DWARF_20230928143746929 (1st intersection): `0.00349`
- Videos from DWARF_20230928144311791 through DWARF_20230928150805759 (1st intersection): `0.00343`
- Videos from DWARF_20231024150226248 through the end (2nd intersection): `0.00339`

I recommend computing all the offsets for the 1st and 2nd intersections separately and finding distributions for both of them. The main reason for this is that the lane used in the first intersection was significantly wider than the second (4.36 m vs. 3.42 m), which might have affected how people drove in them. To work in the simulation, the distribution should be centered around 0 with negative numbers indicating the vehicle was right of center (left from driver's perspective). The "center" value of 0 can just indicate the mean offset. If distributions vary significantly between the 1st and 2nd intersections, I would recommend the 2nd intersection because that part of the data is a little cleaner and the lanes in the simulation are pretty narrow.

Good luck! Let me know if you have any questions.
-Gabe
