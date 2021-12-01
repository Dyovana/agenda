from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Evento(models.Model):
    # usa o models do import, especifica o tipo do campo e o tamanho dele
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)# pode estar em branco ou nulo
    data_evento = models.DateTimeField(verbose_name='Data do evento')
    data_criacao = models.DateTimeField(auto_now=True)# Quando criar o registro vai inserir a hora atual automaticamente
    local = models.CharField(blank=True, max_length=100, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        #Informa que o nome da tabela tem que ser evento
        db_table = 'evento'

    def __str__(self):
        # Faz o titulo aparecer mesmo sem clicar nele
        return self.titulo

    def get_data_evento(self):
        return self.data_evento.strftime('%d/%m/%Y %H:%MHrs')

    def get_data_input_evento(self):
        return self.data_evento.strftime('%Y-%m-%dT%H:%M')
