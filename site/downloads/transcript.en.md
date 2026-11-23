# Snapped. Still Not Legal.



## 00:00:00.000 · Snapped, but still not legal?



Global placement leaves fractional coordinates. Moving cells to the nearest sites and rows looks like the last step. Is it really?

Look at these six cells. After snapping, all align, but A and B choose the same location and C intersects them too. Three overlapping pairs remain.



## 00:00:22.033 · First: snap x to the nearest site



The site width is one. A has x equal to three point seven, so its nearest integer is four. B at four point one also chooses four.

Every cell makes its decision independently. The rounding rule never asks whether another cell has already claimed that location.



## 00:00:42.233 · Next: choose the nearest row bottom



Allowed row bottoms are zero, two and four. A at y equal to one point two is point eight from row two, closer than one point two from row zero.

The y coordinate is the lower-left corner, not the center. Cell height equals row height two, so the row bottom plus the full height must remain inside the chip.



## 00:01:05.033 · One location cannot hold two cells



A and B both finish at four, two, while C finishes at five, two. Each has width two, so A/B, A/C and B/C all overlap.

This is the central limitation of greedy snap: it quantizes coordinates only. Perfect site and row alignment does not imply non-overlapping placement.



## 00:01:29.667 · The boundary must fit the full cell width



After rounding, clamp x between zero and W minus w. On a width-six chip, a width-two cell can place its lower-left corner no farther right than four.

Checking x against the chip width alone is insufficient. A width-two cell whose lower-left corner is at five already extends beyond six.



## 00:01:51.433 · Fixed macros follow their locked constraints



The teacher data locks D at eight, four, although the float draft records eight point four, three point eight. The algorithm restores D to its constraint position.

This does not optimize a fixed macro. Restoring the constraint creates a coordinate difference of point six, which must be explicitly included or excluded from displacement.



## 00:02:15.467 · Two displacement definitions, two answers



Summing Manhattan distances between lower-left corners gives all-cell L1 displacement four point four. Fixed D’s constraint restoration contributes point six.

Counting only movable cells gives three point eight. Both quantities can be reported, but you must state which cells were counted.



## 00:02:36.267 · Short wirelength does not prove legality



HPWL uses cell centers: x plus half the width, and y plus half the row height. Counting each of six nets once gives total HPWL thirty-two.

HPWL measures connectivity, not overlap. An attractive metric cannot replace site, row, bounds, fixed-constraint and non-overlap checks.



## 00:03:01.700 · Write down what happens exactly halfway



Python uses ties-to-even: two point five becomes two, and three point five becomes four. JavaScript’s Math.round gives three for two point five.

This site explicitly uses ties-to-even in both languages. Equal row distances choose the first listed row. Random tests do not replace exact boundary cases.



## 00:03:25.767 · Touching edges are not positive-area overlap



Place width-one A at x equal to one and width-one B at two. Their edges touch, but they share no positive area.

Use strict inequalities for interval intersection. Treating contact as overlap would wrongly reject valid adjacent sites.



## 00:03:45.767 · Snapping is a first step, not a complete legalizer



Removing collisions requires later row packing, overlap removal or a method such as Abacus. This lesson explains greedy snap without secretly adding another solver.

Inspect every failed check before choosing the next step. An aligned placement that still overlaps is a useful counterexample, not a successful legalization result.



## 00:04:12.967 · Now snap a placement and audit it yourself



Edit a fractional coordinate in the lab, inspect its target step by step, then try halfway values, boundary clamps and edge contact. Learn the rule, not just the button.

Finally, recompute the same data in real Python. Alignment, displacement, wirelength and legality are four questions that must be explained separately.
