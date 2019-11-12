from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class BaseModel(models.Model):
    created_at = models.DateTimeField('Data de criação', auto_now_add=True)
    updated_at = models.DateTimeField('Data de modificação', auto_now=True)
    deleted = models.BooleanField('Deletado?', default=False)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Criador',
                                null=True, blank=True)

    class Meta:
        abstract = True


class Role(object):
    ROLE_ADMIN = 'admin'
    ROLE_OPERATIONAL = 'operational'
    ROLE_VIEWER = 'viewer'

    ROLES_CHOICES = (
        (ROLE_ADMIN, 'Administrador'),
        (ROLE_OPERATIONAL, 'Operador'),
        (ROLE_VIEWER, 'Visualizador'),
    )


class Organization(BaseModel):
    name = models.CharField('Nome', max_length=120)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Organização'
        verbose_name_plural = 'Organizações'
        ordering = ('name',)


class Project(BaseModel):
    STATUS_OPEN = 'open'
    STATUS_CLOSED = 'closed'

    STATUS_CHOICES = (
        (STATUS_OPEN, 'Aberto'),
        (STATUS_CLOSED, 'Finalizado')
    )

    organization = models.ForeignKey(Organization, verbose_name='Organização', on_delete=models.CASCADE,
                                     related_name='projects', null=True, blank=True)
    title = models.CharField('Título', max_length=120)
    description = models.TextField('Descrição', blank=True)
    status = models.CharField('Status', max_length=80, choices=STATUS_CHOICES, default=STATUS_OPEN)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Projeto'
        verbose_name_plural = 'Projetos'
        ordering = ('title',)


class ObjectRole(BaseModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    object = GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Usuário',
                             related_name='roles')
    role = models.CharField('Papel', choices=Role.ROLES_CHOICES, default=Role.ROLE_VIEWER, max_length=80)

    def __str__(self):
        return f'{self.object} - {self.user} - {self.role}'

    class Meta:
        verbose_name = 'Papel'
        verbose_name_plural = 'Papéis'
        ordering = ('created_at',)


class ObjectAttachment(BaseModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    object = GenericForeignKey('content_type', 'object_id')

    attachment = models.FileField('Anexo')

    def __str__(self):
        return f'{self.object} - {self.attachment.name}'

    class Meta:
        verbose_name = 'Anexo'
        verbose_name_plural = 'Anexos'
        ordering = ('created_at',)


class Task(BaseModel):
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


class TaskNote(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name='Entrega', related_name='notes')
    title = models.CharField('Título', max_length=120)
    content = models.TextField('Anotação')
    resolved = models.BooleanField('Resolvido?', default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Nota'
        verbose_name_plural = 'Notas'
        ordering = ('created_at',)

    # participantes do time
    # stakeholders
    # escopos
    # entregas relacionadas
