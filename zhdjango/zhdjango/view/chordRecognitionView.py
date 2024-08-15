import json
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from zhdjango.task.chords.recognize.musicPy import musicPy as musicChord


@method_decorator(csrf_exempt, name='dispatch')
class ChordRecognitionView(View):
    def post(self, request):
        try:
            # 从请求中获取音符列表
            data = json.loads(request.body)
            notes = data.get('notes', [])

            if not notes:
                return JsonResponse({'error': 'No notes provided'}, status=400)

            # 使用 musicpy 解析和弦
            musicPy = musicChord(notes)
            chord = musicPy.getNormalChord()
            print('chord: ', chord)

            return JsonResponse({'chord_name': chord})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
