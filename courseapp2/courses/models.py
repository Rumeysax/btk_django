from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField(default="", null=False,unique=True,db_index=True, max_length=50)

    def __str__(self):
        return f"{self.name}"

# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=100, default="")
    description = RichTextField()
    image = models.ImageField(upload_to="images", default="")
    date= models.DateField(auto_now=True,)
    isActive = models.BooleanField(default=False)
    isHome = models.BooleanField(default=False)
    slug = models.SlugField(default="",blank=True,null=False, unique=True, db_index=True) 
    categories = models.ManyToManyField(Category)
    #kayıtlı olanlar için boş karakter gönderildi diğer parametre ise boş olmamasını sağlar
    #tekrardan silip migation oluşturmamak için böyle yapıldı
    #unique ve db_index pk yani id için otomatik olarak var bu sayede duüzgün bir sorgulama işlemi yapılabiliyor
    #primary_key ile istenen yerin pk olması sağlanır bu olduğunda id alanı silinir ve istenen alan pk olmuş olur
    #blank ile formda boş değerin gitmesi sağlanır zaten save metodu bir slug değeri oluşturur veri tabanına gider
    #editable false olması durumunda zaten slaug değeri oluşturuluduğundan ve boş gitmesinden dolayı kurs eklerken çıkmasına gerek kalmaz
    #CASCADE kullanarak eğer bir kategori silinirse onun bağlı olan kurslarda otomatik olarak veri tabnından silinir
    #set_null kullanırsa bir kategori silindiğinde kurslar gitmesin o kategoriye null denmesini sağlıyor
    #set-default se_null a benzerdir

    

    #obje üzerinden save metotdu çağrıldığında önce slug bilgisini title a göre otomatik olarak gerçekleştirir
    # sonra temel sınıftaki save metodunu çağırır    

    def __str__(self):
        return f"{self.title}"
    

class Slider(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images")
    isActive = models.BooleanField(default=False)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.title}"    

class UploadModel (models.Model):
    image = models.ImageField(upload_to="images")
    