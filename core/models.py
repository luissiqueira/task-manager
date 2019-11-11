from django.db import models


class Project(models.Model):
    STATUS_OPEN = 'open'
    STATUS_CLOSED = 'closed'

    STATUS_CHOICES = (
        (STATUS_OPEN, 'Aberto'),
        (STATUS_CLOSED, 'Finalizado')
    )

    title = models.CharField('Título', max_length=120)
    description = models.TextField('Descrição', blank=True)
    status = models.CharField('Status', max_length=80, choices=STATUS_CHOICES, default=STATUS_OPEN)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Projeto'
        verbose_name_plural = 'Projetos'
        ordering = ('title',)


class Task(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_DOING = 'doing'
    STATUS_DONE = 'done'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = (
        (STATUS_PENDING, 'Pendente'),
        (STATUS_DOING, 'Em andamento'),
        (STATUS_DONE, 'Finalizada'),
        (STATUS_CANCELLED, 'Cancelada')
    )

    PRIORITY_LOW = 'low'
    PRIORITY_MEDIUM = 'medium'
    PRIORITY_HIGH = 'high'

    PRIORITY_CHOICES = (
        (PRIORITY_LOW, 'Baixa'),
        (PRIORITY_MEDIUM, 'Média'),
        (PRIORITY_HIGH, 'Alta')
    )

    created_at = models.DateTimeField('Data de criação', auto_now_add=True)
    updated_at = models.DateTimeField('Data de modificação', auto_now=True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Projeto', related_name='tasks')
    title = models.CharField('Título', max_length=120)
    description = models.TextField('Descrição', blank=True)
    status = models.CharField('Status', max_length=80, choices=STATUS_CHOICES, default=STATUS_PENDING)
    priority = models.CharField('Prioridade', max_length=80, choices=PRIORITY_CHOICES, default=PRIORITY_LOW)

    agreed_date = models.DateTimeField('Data combinada', null=True, blank=True)
    final_date = models.DateTimeField('Data da entrega', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Entrega'
        verbose_name_plural = 'Entregas'
        ordering = ('agreed_date', 'created_at')

    # participantes do time
    # stakeholders
    # escopos
    # entregas relacionadas
