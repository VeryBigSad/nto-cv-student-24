#ML API

```
обозначение города(city) в api:
'e' - Екатеринбург
'n' - Нижний Новгород
'v': Владимир
'y' - Ярославль
```
Step 1: Install
```python3
pip install httpx plotly kaleido
```
Step 2: Import 
```python3
from PIL import Image
import httpx
import io
import plotly.graph_objects as go
colors = ['#33a0ff', '#33aaff', '#33b4ff', '#33beff', '#33c8ff', '#33d2ff', '#33dcff', '#33e6ff', '#33f0ff', '#33faff'][::-1]
def return_diagram_image(out, colors):
    names = [i['name'] for i in out][::-1]
    probs = [i['probs'] for i in out][::-1]
    colors = colors[:len(names)]
    fig = go.Figure(data=[go.Bar(y=names, x=probs, marker_color=colors, orientation='h')])

        # Add titles and labels
    fig.update_layout(title='',
                          xaxis_title='Вероятность',
                          yaxis_title='Название')
    img_bytes = fig.to_image(format="png")
    img = Image.open(io.BytesIO(img_bytes))
    return img
```
Step 3: Define variables 

```python3

API_URL = 'https://node-api.datasphere.yandexcloud.net'
X_NODE_ID = 'bt162oc8pa1upv6u39g3'
X_FOLDER_ID = 'b1g8eh6dhbr3jt8au86a'
IAM_TOKEN = 'PUT YOUR TOKEN'
```
