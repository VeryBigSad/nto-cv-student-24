import ruclip
import pandas as pd
import json
#you can change device to "cpu", if it doesn't start like that
import io, base64
from torchvision import transforms
from tqdm.notebook import tqdm
import json
from copy import deepcopy
from PIL import Image
import plotly.graph_objects as go
import json
import torch
from torch import nn
from torchvision.models import resnet18, resnet34, resnet50
import torch.nn.functional as F
import plotly.express as px
from transformers import CLIPImageProcessor, CLIPTextModelWithProjection, CLIPTokenizer, CLIPVisionModelWithProjection


from torch.utils.data import Dataset, DataLoader
def _convert_image_to_rgb(image):
    return image.convert("RGB")


class Predictor:
    def __init__(self, fixes_path, 
                 df_e, df_n, df_v, df_y, latents_path, latents_path2, device='cuda'):
        #self.ind_to_text = json.load(open(ind_to_text_path))
        self.colors = ['#33a0ff', '#33aaff', '#33b4ff', '#33beff', '#33c8ff', '#33d2ff', '#33dcff', '#33e6ff', '#33f0ff', '#33faff'][::-1]
        self.image_encoder = CLIPVisionModelWithProjection.from_pretrained('kandinsky-community/kandinsky-2-1-prior', subfolder='image_encoder').to(device)
        self.text_encoder = CLIPTextModelWithProjection.from_pretrained('kandinsky-community/kandinsky-2-1-prior', subfolder='text_encoder').to(device)
        self.tokenizer = CLIPTokenizer.from_pretrained('kandinsky-community/kandinsky-2-1-prior', subfolder='tokenizer')
        self.processor_img = CLIPImageProcessor.from_pretrained('kandinsky-community/kandinsky-2-1-prior', subfolder='image_processor')
        self.fixes = json.load(open(fixes_path))
        self.categories = ['Железнодорожные станция', 'Биографический музей', 'музей',
              'архитектура', 'мост', 'Театр', 'Стадион', "Историческая архитектура"]
        self.en_categories = ['Railway stations', 'Biographical museum', 'Museum', 'architecture', 'bridge', 'theater', 'stadium', 'historical architecture']
        self.latents = torch.load(latents_path, map_location=device)
        self.latents3 = torch.load(latents_path2, map_location=device)

        self.device = device
        self.df_e = pd.read_csv(df_e)
        self.df_e.index = self.df_e['Name']
        
        self.df_n = pd.read_csv(df_n)
        self.df_n.index = self.df_n['Name']
        
        self.df_v = pd.read_csv(df_v)
        self.df_v.index = self.df_v['Name']
        
        self.df_y = pd.read_csv(df_y)
        self.df_y.index = self.df_y['Name']
        self.main_df = pd.concat([pd.read_csv(df_e), pd.read_csv(df_n), pd.read_csv(df_v), pd.read_csv(df_y)])
        self.main_df.index = self.main_df['XID']
        
        #self.model_e = Net2(len(self.ind_to_text['e'].keys())).to(device)
        #self.model_n = Net2(len(self.ind_to_text['n'].keys())).to(device)
        #self.model_v = Net2(len(self.ind_to_text['v'].keys())).to(device)
        #self.model_y = Net2(len(self.ind_to_text['y'].keys())).to(device)
        #self.model_e.load_state_dict(torch.load(model_e_path))
        #self.model_n.load_state_dict(torch.load(model_n_path))
        #self.model_v.load_state_dict(torch.load(model_v_path))
        #self.model_y.load_state_dict(torch.load(model_y_path))
        self.transform = transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(256),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]) 
            ])
        self.clip, self.processor = ruclip.load("ruclip-vit-base-patch32-384", device=self.device, cache_dir='/home/khroma-son/data')
        templates = ['{}', 'это {}', 'на фото {}']
        self.predictor = ruclip.Predictor(self.clip, self.processor, device, bs=8, templates=templates)
        self.prepare_embeds()
        self.prepare_embeds2()
        self.prepare_cat_latents()
    def prepare_cat_latents(self,):
        tokens = self.tokenizer(
                self.en_categories,
                padding="max_length",
                max_length=self.tokenizer.model_max_length,
                truncation=True,
                return_tensors="pt",
            ).input_ids.to(self.device)
        print(tokens.shape)
        with torch.no_grad():
            self.categories_latents = self.text_encoder(tokens).text_embeds
            self.categories_latents = self.categories_latents / self.categories_latents.norm(dim=1, keepdim=True)
    
    def get_cat_probs(self, image, topk=5):
        with torch.no_grad():
            cond = self.processor_img(image, return_tensors="pt").pixel_values[0].unsqueeze(0).to(dtype=self.image_encoder.dtype, device=self.device)
            img_latents = self.image_encoder(cond)["image_embeds"]
            img_latents = img_latents / img_latents.norm(dim=1, keepdim=True)

            probs = (img_latents @ self.categories_latents.T)[0].cpu()
            top_probs, top_indices = torch.topk(probs, topk)
            top_probs = F.softmax(top_probs, dim=-1)
        top_probs = list(top_probs.numpy())
        cats_str = [self.categories[i] for i in top_indices]
        return cats_str, top_probs

    def return_diagram_cat(self, **args):
        names, probs = self.get_cat_probs(**args)

        colors = self.colors[:len(names)]
        # Create a bar chart
        fig = go.Figure(data=[go.Bar(y=names[::-1], x=probs[::-1], marker_color=colors, orientation='h')])

        # Add titles and labels
        fig.update_layout(title='',
                          xaxis_title='Вероятность',
                          yaxis_title='Название')
        img_bytes = fig.to_image(format="png")
        img = Image.open(io.BytesIO(img_bytes))
        return img

    def return_diagram_text(self, **args):
        names, probs, _ = self.pred_from_text(**args)

        colors = self.colors[:len(names)]
        # Create a bar chart
        fig = go.Figure(data=[go.Bar(y=names[::-1], x=probs[::-1], marker_color=colors, orientation='h')])

        # Add titles and labels
        fig.update_layout(title='',
                          xaxis_title='Вероятность',
                          yaxis_title='Название')
        img_bytes = fig.to_image(format="png")
        img = Image.open(io.BytesIO(img_bytes))
        return img


    def prepare_embeds(self,):
        cities = ['e', 'n', 'v', 'y']
        self.latents2 = {}
        for c in cities:
            d = {}
            latent_key = 'image_latents_' + c
            text_key = 'text_' + c
            latent = self.latents[latent_key].to(self.device)
            texts = self.latents[text_key]
            for i in range(len(latent)):
                if texts[i] not in d.keys():
                    d[texts[i]] = [latent[i], 1]
                else:
                    d[texts[i]] = [d[texts[i]][0] + latent[i],  d[texts[i]][1] + 1]
            texts_new = []
            latents_new = []
            for key in d.keys():
                texts_new.append(key)
                latents_new.append(d[key][0] / d[key][1])
            self.latents2[latent_key] = torch.stack(latents_new)
            self.latents2[text_key] = texts_new

    def prepare_embeds2(self,):
        cities = ['e', 'n', 'v', 'y']
        self.latents4 = {}
        for c in cities:
            d = {}
            latent_key = 'image_latents_' + c
            text_key = 'text_' + c
            latent = self.latents3[latent_key].to(self.device)
            texts = self.latents3[text_key]
            for i in range(len(latent)):
                if texts[i] not in d.keys():
                    d[texts[i]] = [latent[i], 1]
                else:
                    d[texts[i]] = [d[texts[i]][0] + latent[i],  d[texts[i]][1] + 1]
            texts_new = []
            latents_new = []
            for key in d.keys():
                texts_new.append(key)
                latents_new.append(d[key][0] / d[key][1])
            self.latents4[latent_key] = torch.stack(latents_new)
            self.latents4[latent_key] = self.latents4[latent_key] / self.latents4[latent_key].norm(dim=1, keepdim=True)
            self.latents4[text_key] = texts_new

    def pred_from_text(self, text, topk=5, city='e'):
        latent_key = 'image_latents_' + city
        text_key = 'text_' + city
        latent = self.latents2[latent_key].to(self.device)
        texts = self.latents2[text_key]
        with torch.no_grad():
            text_latents = self.predictor.get_text_latents([text]).to(self.device)
            probs = (latent @ text_latents.T)[:, 0].cpu()
            top_probs, top_indices = torch.topk(probs, topk)
            top_probs = F.softmax(top_probs, dim=-1)

        names, f_names = [], []
        
        for i in top_indices.numpy():
            
            name = texts[i]
            f_names.append(name)
            if name in self.fixes[city].keys():
                name = self.fixes[city][name]
            names.append(name)
        return names, list(top_probs.numpy()), f_names
     
    def pred_text2(self, image, topk=5, city='e'):
        latent_key = 'image_latents_' + city
        text_key = 'text_' + city
        latent = self.latents2[latent_key].to(self.device)
        texts = self.latents2[text_key]
        with torch.no_grad():
            img_latents = self.predictor.get_image_latents([image]).to(self.device)
            probs = (latent @ img_latents.T)[:, 0].cpu()
            top_probs, top_indices = torch.topk(probs, topk)
            top_probs = F.softmax(top_probs, dim=-1)

        names, f_names = [], []
        
        for i in top_indices.numpy():
            
            name = texts[i]
            f_names.append(name)
            if name in self.fixes[city].keys():
                name = self.fixes[city][name]
            names.append(name)
        return names, list(top_probs.numpy()), f_names
    
    def pred_text3(self, image, topk=5, city='e'):
        latent_key = 'image_latents_' + city
        text_key = 'text_' + city
        latent = self.latents4[latent_key].to(self.device)
        texts = self.latents4[text_key]
        with torch.no_grad():
            cond = self.processor_img(image, return_tensors="pt").pixel_values[0].unsqueeze(0).to(dtype=self.image_encoder.dtype, device=self.device)
            img_latents = self.image_encoder(cond)["image_embeds"]
            img_latents = img_latents / img_latents.norm(dim=1, keepdim=True)
            #img_latents = self.predictor.get_image_latents([image]).to(self.device)
            probs = (latent @ img_latents.T)[:, 0].cpu()
            top_probs, top_indices = torch.topk(probs, topk)
            top_probs = F.softmax(top_probs, dim=-1)

        names, f_names = [], []
        
        for i in top_indices.numpy():
            
            name = texts[i]
            f_names.append(name)
            if name in self.fixes[city].keys():
                name = self.fixes[city][name]
            names.append(name)
        return names, list(top_probs.numpy()), f_names
    
    def get_cors_text(self, city='e', **args):
        names, probs, f_names = self.pred_from_text(city=city, **args)
        if city == 'e':
            cor = self.df_e.loc[f_names][['Lon', 'Lat']].values
            xid = self.df_e.loc[f_names]['XID'].values
            category = [i.split(',')[0] for i in self.df_e.loc[f_names]['Kind'].values]
            image = self.df_e.loc[f_names]['images'].values

        elif city == 'n':
            cor = self.df_n.loc[f_names][['Lon', 'Lat']].values
            xid = self.df_n.loc[f_names]['XID'].values
            category = [i.split(',')[0] for i in self.df_n.loc[f_names]['Kind'].values]
            image = self.df_n.loc[f_names]['images'].values

        elif city == 'v':
            cor = self.df_v.loc[f_names][['Lon', 'Lat']].values
            xid = self.df_v.loc[f_names]['XID'].values
            category = [i.split(',')[0] for i in self.df_v.loc[f_names]['Kind'].values]
            image = self.df_v.loc[f_names]['images'].values

        elif city == 'y':
            cor = self.df_y.loc[f_names][['Lon', 'Lat']].values
            xid = self.df_y.loc[f_names]['XID'].values
            category = [i.split(',')[0] for i in self.df_y.loc[f_names]['Kind'].values]
            image = self.df_y.loc[f_names]['images'].values
        return names, probs, list([list(i) for i in cor]), xid, category, list(image)
        
        
    def pred_text(self, image, topk=5, city='e'):
        img = self.transform(image).unsqueeze(0).to(self.device)
        if city=='e':
            with torch.no_grad():
                out = self.model_e(img).to('cpu')[0]
        elif city=='n':
            with torch.no_grad():
                out = self.model_n(img).to('cpu')[0]
        elif city=='v':
            with torch.no_grad():
                out = self.model_v(img).to('cpu')[0]
        elif city=='y':
            with torch.no_grad():
                out = self.model_y(img).to('cpu')[0]
        out = torch.nn.functional.softmax(out, dim=0)
        top_probs, top_indices = torch.topk(out, topk)
        names, f_names = [], []
        if city=='e':
            for i in top_indices.numpy():
                name = self.ind_to_text['e'][str(i)]
                f_names.append(name)
                if name in self.fixes['e'].keys():
                    name = self.fixes['e'][name]
                names.append(name)
        elif city=='n':
            for i in top_indices.numpy():
                name = self.ind_to_text['n'][str(i)]
                f_names.append(name)
                if name in self.fixes['n'].keys():
                    name = self.fixes['n'][name]
                names.append(name)
        elif city=='v':
            for i in top_indices.numpy():
                name = self.ind_to_text['v'][str(i)]
                f_names.append(name)
                if name in self.fixes['v'].keys():
                    name = self.fixes['v'][name]
                names.append(name)
        elif city=='y':
            for i in top_indices.numpy():
                name = self.ind_to_text['y'][str(i)]
                f_names.append(name)
                if name in self.fixes['y'].keys():
                    name = self.fixes['y'][name]
                names.append(name)
        return names, list(top_probs.numpy()), f_names
    
    def get_cors_image(self, city='e', **args):
        names, probs, f_names = self.pred_text3(city=city, **args)
        if city == 'e':
            cor = self.df_e.loc[f_names][['Lon', 'Lat']].values
            xid = self.df_e.loc[f_names]['XID'].values
            category = [i.split(',')[0] for i in self.df_e.loc[f_names]['Kind'].values]
        elif city == 'n':
            cor = self.df_n.loc[f_names][['Lon', 'Lat']].values
            xid = self.df_n.loc[f_names]['XID'].values
            category = [i.split(',')[0] for i in self.df_n.loc[f_names]['Kind'].values]
        elif city == 'v':
            cor = self.df_v.loc[f_names][['Lon', 'Lat']].values
            xid = self.df_v.loc[f_names]['XID'].values
            category = [i.split(',')[0] for i in self.df_v.loc[f_names]['Kind'].values]
        elif city == 'y':
            cor = self.df_y.loc[f_names][['Lon', 'Lat']].values
            xid = self.df_y.loc[f_names]['XID'].values
            category = [i.split(',')[0] for i in self.df_y.loc[f_names]['Kind'].values]
        return names, probs, list([list(i) for i in cor]), xid, category
    
    def return_diagram_image(self, **args):
        names, probs, _ = self.pred_text3(**args)

        colors = self.colors[:len(names)]
        # Create a bar chart
        fig = go.Figure(data=[go.Bar(y=names[::-1], x=probs[::-1], marker_color=colors, orientation='h')])

        # Add titles and labels
        fig.update_layout(title='',
                          xaxis_title='Вероятность',
                          yaxis_title='Название')
        img_bytes = fig.to_image(format="png")
        img = Image.open(io.BytesIO(img_bytes))
        return img

    def return_diagram_text(self, **args):
        names, probs, _ = self.pred_from_text(**args)

        colors = self.colors[:len(names)]
        # Create a bar chart
        fig = go.Figure(data=[go.Bar(y=names[::-1], x=probs[::-1], marker_color=colors, orientation='h')])

        # Add titles and labels
        fig.update_layout(title='',
                          xaxis_title='Вероятность',
                          yaxis_title='Название')
        img_bytes = fig.to_image(format="png")
        img = Image.open(io.BytesIO(img_bytes))
        return img
    
    def get_xid(self, xid):
        columns = ['Name', 'Kind', 'City', 'OSM', 'WikiData', 'Rate', 'Lon', 'Lat']
        return list(self.main_df[columns].loc[xid].values)