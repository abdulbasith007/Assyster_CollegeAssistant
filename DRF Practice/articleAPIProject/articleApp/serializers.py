from rest_framework import serializers
from .models import Articles

'''
class articlesSerializer(serializers.Serializer):
    #id=serializers.AutoField(primary_key=True)
    name=serializers.CharField()
    #profile_pic=models.FileField(null=True,blank=True)
    description=serializers.CharField()
'''
class articleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Articles
        fields='__all__'
'''
#To test serializer in shell mode
class Marks(object):
    def __init__(self, integers):
        self.arr = integers
'''
class MarksSerializer(serializers.Serializer):
    arr = serializers.ListField(child=serializers.IntegerField())
    

    class Meta:
        fields = ('arr',)

class ImageSerializer(serializers.Serializer):
    # intialize fields
    image = serializers.ImageField()