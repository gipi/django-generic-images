from django import template
from django.contrib.contenttypes.models import ContentType

from generic_images.models import AttachedImage


register = template.Library()

@register.simple_tag
def generic_slideshow_js():
    """
    This must be placed in the <head> after the jquery <script>.
    """
    return "<script type=\"text/javascript\" src=\"http://cloud.github.com/downloads/malsup/cycle/jquery.cycle.all.latest.js\"></script>"

def generic_slideshow(parser, token):
    """
    Inserts a slideshow with the images related to the given object.

    It has a mandatory argument that is the class of the element
    containing the slideshow.


    {% generic_slideshow object as "class" %}

    TODO: if there is more than one generic field?
    """
    try:
        tag_name, obj, _as, class_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("tag generic_slideshow has the signature bla bla")

    return SlideshowNode(obj, class_name)

class SlideshowNode(template.Node):
    """
    Return a slideshow
    """
    def __init__(self, obj, class_name):
        self.obj = template.Variable(obj)
        self.class_name = class_name.strip('"')

    def render(self, context):
        linked_obj = self.obj.resolve(context)
        obj_type = ContentType.objects.get_for_model(linked_obj)
        images = AttachedImage.objects.filter(content_type__pk=obj_type.id, object_id=linked_obj.id)

        # TODO: how indicate styles and javascript properties?
        html_slideshow = ("<div class=\"%s\">" % self.class_name) + "".join(["<img src=\"%s\" width=\"200px\" height=\"200px\"/>" % c.image.url for c in images]) + "</div>"
        js_slideshow = "<script>$('.%s').cycle({fx:'fade'})</script>" % self.class_name


        # self.class_name is the string with double quote included
        return html_slideshow + js_slideshow

register.tag('generic_slideshow', generic_slideshow)
