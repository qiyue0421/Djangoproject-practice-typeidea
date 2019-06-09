from django import forms
from .models import Comment
import mistune  # 第三方库，支持markdown格式处理
from ckeditor.widgets import CKEditorWidget


class CommentForm(forms.ModelForm):
    nickname = forms.CharField(label='昵称', max_length=50, widget=forms.widgets.Input(attrs={'class': 'form-control', 'style': "width: 60%;"}))
    email = forms.CharField(label='Email', max_length=50, widget=forms.widgets.EmailInput(attrs={'class': 'form-control', 'style': "width: 60%;"}))
    website = forms.CharField(label='网站', max_length=100, widget=forms.widgets.URLInput(attrs={'class': 'form-control', 'style': "width: 60%;"}))
    content = forms.CharField(label='内容', max_length=500, widget=forms.widgets.Textarea(attrs={'rows': 6, 'cols': 60, 'class': 'form-control'}))
    # content = forms.CharField(widget=CKEditorWidget(), label='内容', required=True)

    def clean_content(self):  # 清洗数据，控制评论内容的长度
        content = self.cleaned_data.get('content')
        if len(content) < 10:
            raise forms.ValidationError('内容长度怎么能这么能短呢！！')
        content = mistune.markdown(content, escape=True)  # 转换为markdown格式的数据
        return content

    class Meta:
        model = Comment
        fields = ['nickname', 'email', 'website', 'content']
