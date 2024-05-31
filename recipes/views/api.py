from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from tag.models import Tag

from ..models import Recipe
from ..serializers import RecipeSerializer, TagSerializer


@api_view(http_method_names=['get', 'post'])
def recipe_api_list(request):
    if request.method == 'GET':
        recipes = Recipe.objects.get_published()[:10]
        serializer = RecipeSerializer(
            instance=recipes,
            many=True,
            context={'request': request},
        )
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = RecipeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # calls the model's save method
        return Response(
            serializer.validated_data,
            status=status.HTTP_201_CREATED
        )


@api_view()
def recipe_api_detail(request, pk):
    recipe = get_object_or_404(
        Recipe.objects,
        pk=pk
    )
    serializer = RecipeSerializer(
        instance=recipe,
        many=False,
        context={'request': request},
    )
    return Response(serializer.data)

# IF YOU WANT TO CHANGE THE DETAIL MESSAGE AND STATUS CODE #
    # from rest_framework import status
    # recipe = Recipe.objects.get_published().filter(pk=pk).first()

    # if recipe:
    #     serializer = RecipeSerializer(instance=recipe, many=False)
    #     return Response(serializer.data)
    # else:
    #     return Response({
    #         'detail': 'oops',
    #     }, status=status.HTTP_418_IM_A_TEAPOT)


@api_view()
def tag_api_detail(request, pk):
    tag = get_object_or_404(
        Tag.objects,
        pk=pk
    )
    serializer = TagSerializer(
        instance=tag,
        many=False,
        context={'request': request},
    )
    return Response(serializer.data)
