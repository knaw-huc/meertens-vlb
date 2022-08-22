# meertens-vlb
`convertPdf` splits a multipage pdf into single jpeg files. If the width of a jpeg is greater than its height it is also split into left and right.

`convertTif` splits a multipage tif into single jpeg files.;

Both scripts call `makeCmdi` to produce an xml file for each converted input file.
