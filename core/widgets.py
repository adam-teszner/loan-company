from django.forms.widgets import ClearableFileInput 


class MyFileInput(ClearableFileInput):
    template_name = "widget_templates/file_input.html"

    def clear_label_name(self, name):

        n = name.split('_')
        return ' '.join([word[0].upper() + word[1:] for word in n])

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        label_name = self.clear_label_name(name)
        context["widget"].update(
            {
                'label_name': label_name
            }
        )
        return context

