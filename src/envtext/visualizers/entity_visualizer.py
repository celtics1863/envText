
# 模板采用 spacy 的模板： https://github.com/explosion/spaCy/blob/master/spacy/displacy/render.py

from .visualizer_base import VisualizerBase
class EntityVisualizer(VisualizerBase):
    TMP = """ 
        <mark class="entity" style="background: {bg}; padding: 0.45em 0.6em; margin: 0 0.25em; line-height: 1; border-radius: 0.35em"> 
            {text} 
            <span style="font-size: 0.8em; font-weight: bold; line-height: 1; border-radius: 0.35em; vertical-align: middle; margin-right: 0.5rem">{label}{kb_link}</span>
        </mark>
        """
    
    def generate_html(self,text,words,poses,*args,**kwargs):
        html = '<div style="line-height:2.5;"/>'
        params = {
          "label": '标签',
          "text": '实体',
          "bg": 'red',
          "kb_link": ''
            }

        #重新整理标注和文本，前提是words按位置从前至后排列
        new_words = []
        new_poses = []
        new_text = "".join(list(text))
        for word,pos in zip(words,poses):
            loc = new_text.find(word)
            if loc == -1:
                continue
            elif loc == 0:
                new_text = new_text[len(word):]
                new_words.append(word)
                new_poses.append(pos)
            else:
                new_words.extend(list(new_text[:loc]))
                new_poses.extend(["" for i in range(loc)])
                new_words.append(word)
                new_poses.append(pos)
                new_text = new_text[loc + len(word):]


        #嵌入模板
        for word,pos in zip(words,poses):
            if pos in self.DEFAULT_LABEL_COLORS:
                param = params.copy()
                param['bg'] = self.DEFAULT_LABEL_COLORS[pos]
                param['text'] = "".join(word)
                param['label'] = pos
                html += self.TMP.format(**param)
            elif pos:
                #随机分配颜色
                import random
                self.DEFAULT_LABEL_COLORS[pos] = random.choice(self.COLORS)
                param = params.copy()
                param['bg'] = self.DEFAULT_LABEL_COLORS[pos]
                param['text'] = "".join(word)
                param['label'] = pos
                html += self.TMP.format(**param)
            else:
                html += "".join(word)
        
        return html

    def generate_text(self,text,words,poses,*args,**kwargs):
        text = "".join(list(text))
        for word,pos in zip(words,poses):
            if pos:
                text += f"\t{word}\t{pos}\n"


