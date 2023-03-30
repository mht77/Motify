from django.shortcuts import render


def test_view(request):
    context = {'title': 'Test Title'}
    return render(request, 'Test.html', context)
