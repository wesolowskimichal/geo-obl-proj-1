### How to run

1. Clone repo
2. Create virtual environment (optional but recommended)

WINDOWS:
```
python -m venv venv
.\venv\Scripts\Activate.ps1
```

LINUX:
```
python -m venv venv
source venv/bin/activate
```
3. Run code:
Console mode - result will be outputed in outputted:
```
python main.py cli  x1 y1 x2 y2 x3 y3 x4 y4
```
Visualization mode - lines will be represented on a chart
```
python main.py viz  x1 y1 x2 y2 x3 y3 x4 y4
```
