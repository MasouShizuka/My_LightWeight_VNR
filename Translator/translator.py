class Translator(object):
    label = None
    name = None
    key = None

    working = None
    get_translate = True

    def translate(self, text):
        pass

    def thread(self, text, text_translate, is_floating, textarea, *args):
        text_translate[self.label] = self.translate(text)
        
        if self.get_translate:
            # 更新界面中对应翻译的文本
            if not is_floating:
                textarea.update(
                    self.name + ':\n' +
                    text_translate[self.label] + '\n\n',
                    append=True,
                )
            # 更新浮动窗口中对应翻译的文本
            else:
                textarea.update(text_translate[self.label])

    def update_config(self, config):
        pass
