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
Step 4: Send text

```python3
text = "церковь"
city_letter = 'n'
async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{API_URL}/text?",
            headers={
                "x-node-id": X_NODE_ID,
                "Authorization": f"Bearer {IAM_TOKEN}",
                "x-folder-id": X_FOLDER_ID
            },
            json={"text": text, "city": city_letter},
        )
        response_json_categories = resp.json()
```
Out:
```
[{'name': 'Казанская церковь (Кстово)',
  'probs': 0.20118318498134613,
  'coord': [44.172501, 56.181389],
  'xid': 'Q96240614',
  'category': 'religion'},
 {'name': 'Храм святителей Московских',
  'probs': 0.20096348226070404,
  'coord': [43.997238, 56.312874],
  'xid': 'R5393060',
  'category': 'religion'},
 {'name': 'Храм Сергия Радонежского',
  'probs': 0.20090050995349884,
  'coord': [43.987236, 56.323441],
  'xid': 'W147129128',
  'category': 'religion'},
 {'name': 'Церковь Знамения Божией Матери и святых Жен-Мироносиц',
  'probs': 0.19884654879570007,
  'coord': [43.995018, 56.324314],
  'xid': 'W52464978',
  'category': 'religion'},
 {'name': 'Церковь во имя Всемирлостивейшего Спаса',
  'probs': 0.19810636341571808,
  'coord': [44.024479, 56.319065],
  'xid': 'W151905901',
  'category': 'religion'}]
```
