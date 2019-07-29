from django.shortcuts import render

# Create your views here.

# def frontendRenderView(request):
#     return render(request, 'pages/front-end-render.html')

def test_sub_page(request):
    return render(request, 'subpages/pdf.html')
