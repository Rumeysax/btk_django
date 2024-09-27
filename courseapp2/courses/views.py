from django.shortcuts import get_object_or_404, redirect, render
from courses.forms import CourseCreateForm, CourseEditForm, UploadForm
from .models import Course, Category, Slider, UploadModel
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test


def index(request):
    #kurslar = [course for course in db["courses"] if course["isActive"]==True]
    kurslar = Course.objects.filter(isActive=1, isHome=1)
    kategoriler = Category.objects.all()
    sliders = Slider.objects.filter(isActive=True)

    return render(request, 'courses/index.html', {
        'categories': kategoriler,
        'courses': kurslar,
        'sliders': sliders,
    })

def isAdmin (user):
    return user.is_superuser

@user_passes_test(isAdmin)
def create_course(request):
    # if not request.user.is_authenticated:
    #     return redirect("index")  # bu kullanımı bütün viewlerde kullanmak gerekir 
    #is_authenticated bunun karşılığı @login_required dır bunun kullanılması kesin bir giriş yapmasını gerektirir
    # yani @login_required eklenen herhangi bir view metodu bir giriş gerektirir
    # sadece ı bekler eğer sadece admin görsün isteniyorsa @user_passes_test(isAdmin) kullanılır
    if request.method == "POST":
        form = CourseCreateForm(request.POST, request.FILES)

        if form.is_valid():
            # kurs = Course(title=form.cleaned_data["title"],
            #               description=form.cleaned_data["description"],
            #               imageUrl=form.cleaned_data["imageUrl"],
            #               slug = form.cleaned_data["slug"])
            # kurs.save()
            form.save()
            return redirect("/kurslar")
        # kurs = Course(title=title, description=description, imageUrl=imageUrl, slug=slug, isActive=isActive,isHome=isHome)
        # kurs.save()#veri tabanına kaydeder
        # return redirect("/kurslar")#kurs eklendikten sonra kurslar sayfasına gider
    else:    
        form = CourseCreateForm()
    return render(request, "courses/create_course.html", {"form":form})

@user_passes_test(isAdmin)
def course_list(request):
     kurslar = Course.objects.all()

     return render(request, 'courses/course-list.html', {
        'courses': kurslar
    })

@login_required
def course_edit(request,id):
    course = get_object_or_404(Course, pk=id)

    if request.method == "POST":
        form = CourseEditForm(request.POST, request.FILES ,instance=course,)
        form.save()
        return redirect("course_list")
    else:
        form = CourseEditForm(instance=course)

    return render(request, "courses/edit-course.html", {"form":form})

def course_delete(request, id):
    course =  get_object_or_404(Course, pk=id)

    if request.methos == "POST":
        #Course.objects.get(pk=id).delete()
        Course.delete()
        return redirect("course_list")

    return render(request, 'courses/course-delete.html', {"course":course})

# def upload (request):
#     if request.method == "POST":
#         form = UploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             uploaded_images = request.FILES["image"]
#             handle_uploaded_files(uploaded_images)
#             return render(request, 'courses/succes.html')
#     else:
#         form = UploadForm()
#     return render(request, 'courses/upload.html', {"form":form})
# #uploaded_image = request.FILES['image'] tek bir dosya yükler FILES.get('images') yine tek dosya yükler
# #FILES.getlist("images") birden fazla dosya yüklemek için

# def handle_uploaded_files(file):
#     number = random.randint(1,99999)
#     file_name, file_extension = os.path.splitext(file.name)
#     name = file_name+"_"+ str(number)+ file_extension
#     with open("temp/" + name, "wb+") as destination:
#         for chunk in file.chunks():
#             destination.write(chunk)

def upload (request):
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            model = UploadModel(image = request.FILES["image"])
            model.save()
            return render(request, 'courses/succes.html')
    else:
        form = UploadForm()
    return render(request, 'courses/upload.html', {"form":form})


def search (request):
    if "q" in request.GET and request.GET["q"] != "":
        q = request.GET["q"]
        kurslar = Course.objects.filter(isActive=True, title__contains=q).order_by("date")
        kategoriler = Category.objects.all()
    else:
        return redirect("/kurslar")

    return render(request, 'courses/search.html', {
        'categories': kategoriler,
        'courses': kurslar,
    })

def details(request, slug):
    course = get_object_or_404(Course, slug=slug)

    context = {
        'course': course
    }
    return render(request, 'courses/details.html', context)

def getCoursesByCategory(request, slug):
    kurslar = Course.objects.filter(categories__slug=slug, isActive=True).order_by("date")
    kategoriler = Category.objects.all()

    paginator = Paginator(kurslar,2)
    page = request.GET.get('page',1)
    page_obj = paginator.page(page)

    print(paginator.count)
    print(paginator.num_pages)

    return render(request, 'courses/list.html', {
        'categories': kategoriler,
        'page_obj': page_obj,
        'seciliKategori': slug
    })








   
   
   
    # paginator = Paginator(kurslar,2)
    # page = request.GET.get('page',1)
    # page_obj = paginator.page(page)
    #sayfalama linkleri