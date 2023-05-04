from django.db import models
from categorias.models import Categoria
from django.contrib.auth.models import User
from PIL import Image
from django.conf import settings
from pathlib import Path

class Post(models.Model):
    titulo_post = models.CharField(max_length=255, verbose_name='Titulo')
    autor_post = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Autor')
    data_post = models.DateTimeField(auto_now_add=True, verbose_name='Data')
    conteudo_post = models.TextField(verbose_name='Conteudo')
    excerto_post = models.TextField(verbose_name='Excerto')
    categoria_post = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING, 
                                       blank=True, null=True, verbose_name='Categoria')
    imagem_post = models.ImageField(upload_to='post_img/', blank=True, 
                                    null=True, verbose_name='Imagem')
    publicado_post = models.BooleanField(default=False, verbose_name='Publicado')
    
    def __str__(self):
        return self.titulo_post
    
    def save(self, *args, **kwargs):
        super.save(*args, **kwargs)
        
        self.rezise_image(self.imagem_post, 800)
        
    # Função para reduzir resolução das imagens 
    @staticmethod
    def rezise_image(img_name, new_width):
        img_path = Path(settings.MEDIA_ROOT, img_name)
        img = Image.open(img_path)
        width, height = img.size
        # Regra de 3 para definir a altura nova da imagem
        new_height = round((new_width * height) / width)
        
        # Não faz nada se a imagem tiver resolução igual ou menor a nova resolução
        if width <= new_width:
            img.close()
            return
        
        new_img = img.resize((new_width, new_height), Image.ANTIALIAS)
        new_img.save(
            img_path,
            optimize=True,
            quality=60
        )
        new_img.close()