from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.destinos.models import Categoria, Destino, FotoDestino, Avaliacao
from apps.grupos.models import GrupoExpedicao, PontoEncontro
from apps.comentarios.models import Comentario

Usuario = get_user_model()

DESTINOS = [
    {
        'nome': 'Trilha do Pico Paraná',
        'descricao': 'O ponto mais alto do Sul do Brasil com 1.877 m de altitude. Vista panorâmica deslumbrante da Serra do Mar paranaense.',
        'latitude': -25.2483, 'longitude': -48.8401,
        'dificuldade': 'dificil', 'categoria': 'trilha', 'distancia_km': 14.0,
        'fotos': ['https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=800&q=80',
                  'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=80'],
    },
    {
        'nome': 'Praia da Lagoinha do Leste',
        'descricao': 'Praia paradisíaca acessível apenas por trilha de 3 horas. Águas cristalinas, sem construções e com lagoa de água doce ao lado.',
        'latitude': -27.6937, 'longitude': -48.4689,
        'dificuldade': 'moderado', 'categoria': 'ponto_turistico', 'distancia_km': 9.0,
        'fotos': ['https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=800&q=80'],
    },
    {
        'nome': 'Cachoeira Véu da Noiva',
        'descricao': 'Uma das mais belas cachoeiras de Santa Catarina com 50 m de queda d\'água. Rodeada de Mata Atlântica exuberante.',
        'latitude': -26.6219, 'longitude': -49.0711,
        'dificuldade': 'facil', 'categoria': 'ponto_turistico', 'distancia_km': 2.5,
        'fotos': ['https://images.unsplash.com/photo-1596401057633-54a8c8e80f14?w=800&q=80'],
    },
    {
        'nome': 'Acampamento Morro do Cambirela',
        'descricao': 'Área de acampamento com estrutura básica e trilha de acesso de dificuldade moderada. Vista para o oceano Atlântico.',
        'latitude': -27.7234, 'longitude': -48.5612,
        'dificuldade': 'moderado', 'categoria': 'acampamento', 'distancia_km': 6.0,
        'fotos': ['https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=800&q=80'],
    },
    {
        'nome': 'Trilha da Serra Gaúcha',
        'descricao': 'Percurso entre vinhedos e florestas de araucária na região de Gramado. Especialmente bonita no outono com as cores das folhas.',
        'latitude': -29.3768, 'longitude': -50.8763,
        'dificuldade': 'facil', 'categoria': 'trilha', 'distancia_km': 8.0,
        'fotos': ['https://images.unsplash.com/photo-1448375240586-882707db888b?w=800&q=80'],
    },
    {
        'nome': 'Parque Nacional da Chapada Diamantina',
        'descricao': 'Paraíso ecológico na Bahia com grutas, cachoeiras, rios e formações rochosas únicas. Destino imperdível para amantes da natureza.',
        'latitude': -12.5722, 'longitude': -41.4181,
        'dificuldade': 'moderado', 'categoria': 'ponto_turistico', 'distancia_km': 25.0,
        'fotos': ['https://images.unsplash.com/photo-1551632811-561732d1e306?w=800&q=80'],
    },
    {
        'nome': 'Acampamento Vale do Pati',
        'descricao': 'Um dos mais belos vales do Brasil, localizado na Chapada Diamantina. Acampamento de alto nível com roteiro de 5 dias.',
        'latitude': -12.6124, 'longitude': -41.5356,
        'dificuldade': 'dificil', 'categoria': 'acampamento', 'distancia_km': 65.0,
        'fotos': ['https://images.unsplash.com/photo-1478131143081-80f7f84ca84d?w=800&q=80'],
    },
    {
        'nome': 'Pico das Agulhas Negras',
        'descricao': 'Ponto culminante do Estado do Rio de Janeiro com 2.791 m. Trilha desafiadora no Parque Nacional de Itatiaia.',
        'latitude': -22.3802, 'longitude': -44.6561,
        'dificuldade': 'dificil', 'categoria': 'trilha', 'distancia_km': 12.0,
        'fotos': ['https://images.unsplash.com/photo-1519681393784-d120267933ba?w=800&q=80'],
    },
]

AVALIACOES = [5, 4, 5, 3, 4, 5, 4, 5]


class Command(BaseCommand):
    help = 'Popula o banco com dados iniciais para demonstração'

    def handle(self, *args, **options):
        if Destino.objects.exists():
            self.stdout.write('Dados já existem, pulando seed.')
            return

        # Categories
        cats = {}
        icones = {'trilha': 'bi-signpost-2', 'acampamento': 'bi-tent', 'ponto_turistico': 'bi-geo-alt'}
        for nome, icone in icones.items():
            cat, _ = Categoria.objects.get_or_create(nome=nome, defaults={'icone': icone})
            cats[nome] = cat
        self.stdout.write('Categorias criadas.')

        # Admin user
        admin, created = Usuario.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@explorabrasil.com', 'first_name': 'Admin',
                      'last_name': 'ExploraBrasil', 'is_staff': True, 'is_superuser': True}
        )
        if created:
            admin.set_password('admin123')
            admin.bio = 'Administrador da plataforma ExploraBrasil'
            admin.save()

        # Demo users
        usuarios = [admin]
        for i, (nome, sobrenome) in enumerate([('Ana', 'Santos'), ('Carlos', 'Oliveira'), ('Beatriz', 'Lima')]):
            username = nome.lower()
            u, created = Usuario.objects.get_or_create(
                username=username,
                defaults={'email': f'{username}@exemplo.com', 'first_name': nome, 'last_name': sobrenome,
                          'bio': f'Aventureira apaixonada por trilhas e natureza.'}
            )
            if created:
                u.set_password('demo123')
                u.save()
            usuarios.append(u)

        self.stdout.write('Usuários criados.')

        # Destinations
        for i, dados in enumerate(DESTINOS):
            fotos = dados.pop('fotos')
            cat_nome = dados.pop('categoria')
            destino = Destino.objects.create(
                categoria=cats[cat_nome],
                criador=usuarios[i % len(usuarios)],
                aprovado=True,
                **dados
            )
            for j, url in enumerate(fotos):
                FotoDestino.objects.create(destino=destino, url=url, ordem=j)

            Avaliacao.objects.create(destino=destino, usuario=usuarios[0], nota=AVALIACOES[i])

            Comentario.objects.create(
                destino=destino, usuario=usuarios[1 % len(usuarios)],
                texto='Lugar incrível! Recomendo muito a visita. A trilha está bem sinalizada e a vista compensa o esforço.'
            )

        self.stdout.write('Destinos criados.')

        # Sample expedition group
        d1 = Destino.objects.filter(aprovado=True).first()
        if d1:
            grupo = GrupoExpedicao.objects.create(
                nome='Trilheiros do Sul 2025',
                destino=d1,
                criador=admin,
                descricao='Grupo para a expedição de verão. Todos os níveis são bem-vindos!',
                vagas=15
            )
            grupo.membros.set(usuarios[:3])
            PontoEncontro.objects.create(
                nome='Estacionamento da trilha',
                destino=d1,
                grupo=grupo,
                latitude=float(d1.latitude) + 0.01,
                longitude=float(d1.longitude) + 0.01,
                criador=admin,
                descricao='Nos encontramos às 7h no estacionamento principal'
            )

        self.stdout.write(self.style.SUCCESS('Seed concluído com sucesso!'))
        self.stdout.write('Login admin: admin / admin123')
        self.stdout.write('Login demo: ana / demo123')
