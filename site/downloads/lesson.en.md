# Snapped. Still Not Legal: Greedy Site/Row Snap

## Problem and learning goals

Inputs are fractional lower-left cell positions, widths, chip dimensions, site and row grids, and fixed constraints. Outputs are snapped coordinates. The algorithm aligns each cell and enforces boundaries; it does not reserve room for neighbors, so it does not guarantee non-overlap.

You should be able to calculate rounding, width-aware clamping and nearest rows, explain halfway ties and fixed macros, distinguish all-cell from movable displacement, and calculate cell-center HPWL. Learn what is missing between snapping and legal placement, rather than merely learning a button.

## Coordinates and grid

Site width is one. The teacher chip is W=12, H=6 with rowH=2 and row bottoms [0,2,4]. Every cell has row-height height; its width comes from the data. Coordinates are lower-left corners, and a rectangle occupies [x,x+w] and [y,y+rowH].

The diagram’s y-axis points upward. Float inputs may cross rows, exceed a boundary or disagree with a fixed constraint; these are diagnostics, not hidden assumptions. Rectangles use their actual widths and height. Treating cells as points cannot establish non-overlap.

## Core loop and termination

Process each cell once. For movable cells, round x to the nearest integer and clamp it to [0,W-w]. Choose the closest allowed row for y. Fixed macros use the coordinates explicitly stated by their constraints. Stop after all cells; there is no free-space search.

```text
for cell in cells:
    if fixed(cell):
        output[cell] = locked_position[cell]
    else:
        x = clamp(round_even(input.x), 0, W - width[cell])
        y = first_argmin(rows, abs(row - input.y))
        output[cell] = (x,y)
# No overlap search or row packing occurs here.
```

## Teacher float golden

```text
Cell  width   before        after    L1
A       2     (3.7,1.2)     (4,2)    1.1
B       2     (4.1,1.4)     (4,2)    0.7
C       2     (5.2,2.3)     (5,2)    0.5
D       2     (8.4,3.8)     (8,4)    0.6  fixed constraint
E       1     (0.3,4.6)     (0,4)    0.9
F       1     (10.2,0.4)    (10,0)   0.6
```

A is 0.8 from row two, closer than its 1.2 distance to row zero. B also chooses row two. Both x coordinates become four. C becomes five, and width two makes it intersect both A and B. Site, row, boundary and fixed checks can all pass while non-overlap fails.

## Halfway ties and cross-language reproduction

Python round uses ties-to-even: 0.5→0, 1.5→2, 2.5→2 and 3.5→4. JavaScript Math.round(2.5) gives three. The original language ports therefore need not agree on every boundary. This site explicitly implements Python’s tie rule in JavaScript and cross-checks it independently.

Row ties are a different rule. The first row in the supplied list wins, so y=1 chooses zero in [0,2,4], and y=3 chooses two. Reordering the list can change a tied result; the default list is fixed in ascending order. Random floats almost never hit exact halves, so explicit boundary tests are necessary.

## Fit the whole cell inside the boundary

A width-w cell on a width-W chip can place its lower-left corner at most at W-w, not W. In the boundary preset, W=6 and w=2. B.x=5.7 rounds to six, then clamps to four; the interval [4,6] fits exactly.

Negative x also rounds before clamping to zero. Allowed rows must leave room for the full height, with row+rowH≤H. A lower-left corner inside the chip is not enough to prove that its whole rectangle fits.

## Why three overlapping pairs remain

A and B both occupy [4,6]×[2,4], while C occupies [5,7]×[2,4]. The A/B intersection has area four; A/C and B/C each have area two. There are three pairs. Pairwise areas are not a union-area measurement, so do not rename their sum as unique total overlap area.

Rectangles overlap only when both axis intersections have positive length. Width-one A at (1,0) and B at (2,0) touch but share no positive area. Strict interval comparisons permit that contact. After alignment, this agrees with the source’s same-row check; for fractional inputs, the lesson also displays full two-dimensional intersections to explain cross-row cases.

## Fixed D and two displacement definitions

The fixed constraint says D=(8,4), but starter_float records D=(8.4,3.8). Greedy snap restores the stated lock, rather than optimizing D as a movable cell. Its restoration distance is |8-8.4|+|4-3.8|=0.6.

The source total_displacement counts every cell even when its API accepts a fixed argument. All-cell L1 is 1.1+0.7+0.5+0.6+0.9+0.6=4.4. Excluding D gives movable-only L1=3.8. Both definitions appear side by side so that the counting scope is explicit.

## Cell-center HPWL does not prove legality

A cell center is (x+w/2,y+rowH/2). Net HPWL is its center-coordinate x range plus y range. Count each of six nets once with unit weight. The final contributions are 0,5,1,6,6,14, totaling 32.

The float input has total HPWL 36. Snapping lowers it to 32 while leaving three overlapping pairs. Better wirelength does not imply legality, and smaller displacement cannot replace site, row, bounds, fixed and non-overlap checks. For mixed widths, lower-left and center distances can differ; do not silently reuse a point-pin model.

## Use the live lab

Both boards share one input. The left shows the float placement and the right initially shows the complete result. Previous, next and replay expose real processing prefixes; unprocessed cells retain their original coordinates. Editing an input recomputes the trace rather than preserving stale results.

Drag, arrow keys and the coordinate table provide equivalent input. Fixed D is read-only. Consecutive keyboard edits and inspections remain usable. Reduced-motion mode retains manual stepping. Questions use the fixed teacher golden, independently of free experiments; only correct submissions record completion. Revealing an explanation does not score, and denied local storage does not block learning.

## Real CPython and reproduction

The workspace runs CPython in an independent Worker. Edit, run, use live mode, inspect exceptions, stop, or recover after the five-second limit. Returning through the browser’s back-forward cache rebuilds the interpreter while retaining code. Bundled Pyodide loads on demand; no local Python installation or external CDN is required.

The independent reference uses native Python round and explicit row selection, returning coordinates, both displacement definitions, HPWL, overlap pairs and legality. Complete snap_x and nearest_row in the exercise; the full loop is supplied. Six primitive checks cover exact halves, negative and full-width boundaries, and equal-distance rows before extending to the teacher data.

## Complexity and what comes next

Core snapping scans r rows for each of n cells: O(nr) time and O(n) output. This teaching implementation additionally stores every prefix, with O(n²) copying/storage. Full rectangle-pair diagnostics take O(n²), and HPWL traverses net members. The core loop’s complexity is not the cost of the whole teaching interface.

Removing collisions requires later overlap removal, row packing or Abacus-like methods. This lesson does not implement them or relabel their output as greedy snap. Identify the failed checks accurately before choosing the next tool.

## Sources and skill transfer

Based on Yongfu Li’s eda-learning module02-01-greedy-snap and common implementation at commit 003bcd49e3794e6cfd2680181cdbd347d673ad07, corresponding to issue #36. The Python tie rule, original JavaScript difference, fixed-D restoration and metric scope are explicitly documented.

This lesson consumes frozen skill v2.0.0 once after the congestion pilot’s real website/film iteration. Five file hashes are recorded in docs/skill-transfer.json. It reuses validated player, Worker and media mechanisms with new lesson-specific algorithms, diagrams, notes and narration. New code is MIT, new teaching content CC BY 4.0; fonts and Pyodide retain their licenses.
