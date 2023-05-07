from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
from rest_framework.views import APIView

from song.models import Song


@xframe_options_exempt
def player_view(request):
    song = Song.objects.first()
    context = {"song": song}
    return render(request, "player.html", context)


class SongView(APIView):
    # def get(self, request, *args, **kwargs):
    #     song = Song.objects.first()
    #     serializer = SongSerializer(song)
    #     return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        song = Song.objects.filter(id=request.data['song']).first()
        song.no_plays += 1
        song.save()
        return HttpResponse("Song updated")
