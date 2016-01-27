# pyPdfTools
tools to manage PDF files easily

### pdfMerger

This tool merge multiple PDF files in a single one:

```
usage: pdfMerger [-h] [-s | -a] [-o OUTPUT] [-r i [i ...]] [-q | -v]
                 firstFile otherFile [otherFile ...]
positional arguments:
  firstFile             First file to be merged
  otherFile             Other pdf Files that have to be merged with first

optional arguments:
  -h, --help            show this help message and exit
  -s, --sequential      Sequential method, files will be merged in the same
                        order as user specified them
  -a, --alternate       Alternate method, files will be merged taking one page
                        from each file at a time
  -o OUTPUT, --output OUTPUT
                        FileName for the output file
  -r i [i ...], --reverse i [i ...]
                        Select index of otherFile that have to be reversed
                        before merging
  -q, --quiet           Set a Quiet Output for the Script
  -v, --verbose         Set a Verbose Output for the Script

```

###### Example:
If you have to **scan** a document composed by a lot of sheet you can scan first the _odd pages_, after that you can _turn paper block_ and scan the _even pages_ in **reverse** order, with this tool you can simply **merge odd and even pages** in final document in this way:

```bash
pdfMerger -q -r 0 -o final.pdf -a odd.pdf even.pdf
```
###### Using it in python Project

```python
from pdfMerger import PdfMerger
```
