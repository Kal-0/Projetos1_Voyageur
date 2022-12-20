import pickle
import os

def saveData(obj):
  with open("usuarioTeste.pickle", 'wb') as arquivo:
      pickle.dump(obj, arquivo)
      pickle.dump(obj, arquivo)
      arquivo.close

def loadData():
  with open("usuarioTeste.pickle", 'rb') as arquivo:
    teste = pickle.load(arquivo)
    arquivo.close
    return teste
  
  
logado = False
usuarioAtual = None
global archive
 
  
def atualizaEndereco(objSelf, listaArchive):
  global archive
  for obj in listaArchive:
      if obj.idd == objSelf.idd:
        indexDecoy = listaArchive.index(obj)       
        listaArchive[indexDecoy] = objSelf
        saveData(archive)
        archive = loadData()

class Usuario:
    def __init__(self, idd, nome, email, senha):
        self.idd = idd
        self.nome = nome
        self.email = email
        self.senha = senha
        self.curtidas = []
        self.roteiros = []  

    def curtir(self, atividade):
      global archive
      for atvCurtida in self.curtidas:
        if(atividade.idd == atvCurtida.idd):
          print("Atividade foi adicionada!")
          break
      else:
        self.curtidas.append(atividade)
        atualizaEndereco(self, archive["usuarios"])

    def verCurtidas(self):
      
      if not self.curtidas:
        print("Você ainda não curtiu nenhuma atividade.")
      else:
        print("ATIVIDADES CURTIDAS: ")
        for curtida in self.curtidas:
          print(curtida.nome)

    def verRoteiros(self):
      if not self.roteiros:
        print("Você nao criou roteiros ainda.")
      else:
        cont = 1
        print("------------------------\n")
        for roteiro in self.roteiros:
          print(f"Roteiro {cont}\n")
          for atividade in roteiro:
              print(f"* {atividade.nome}") 
          print("\n------------------------\n") 
          cont+=1

    @staticmethod
    def criaUsusario():
      global archive
      vef = True
      idd = len(archive["usuarios"])+1
      print("\n-- CRIE A SUA CONTA --\n")
      nome = input("Insira seu nome: ")
      email = input("Insira seu email: ")
      senha = input("Insira sua senha: ")
      for usuario in archive["usuarios"]:
          if usuario.email == email:
              print("email já cadastrado!")
              vef = False
      if vef == True:    
        usuario = Usuario(idd, nome, email, senha)
        return usuario

    def removeCurtida(self, atividade):
      global archive
      while True:
        if atividade in self.curtidas:
          self.curtidas.remove(atividade)
          
          atualizaEndereco(self, archive["usuarios"])
          break
        

    def adicionarAtividadeRoteiro(self, atividade):
      global archive
      if type(atividade) != list:
        while True:
          cont = 1
          print("Escolha o roteiro que você quer.")
          print("[0] - criar roteiro")
          for roteiro in self.roteiros:
            print(f"{cont} - Roteiro {cont}")
            cont += 1
          roteiroSelecionado = int(input())
          if roteiroSelecionado == 0:
            self.roteiros.append([])
            atualizaEndereco(self, archive["usuarios"])
          else:
            self.roteiros[roteiroSelecionado-1].append(atividade)
            print(f"== atividade adicionada ao roteiro {roteiroSelecionado} ==\n")
            
            atualizaEndereco(self, archive["usuarios"])
            break
      else:
        self.roteiros.append(atividade)
        atualizaEndereco(self, archive["usuarios"])
          
        

    def fazComentario(self, atividade: object, texto: str, nota: int, imagem: str):
        global archive
        comentarioAtual = Comentario(self, atividade, texto, nota, imagem)
        listaComentarios = []
        for comentarioAtividade in atividade.comentario:
            listaComentarios.append(comentarioAtividade.usuario_c.email)
        if not atividade.comentario:
            atividade.comentario.append(comentarioAtual)
            atividade.nota.append(nota)
            atualizaEndereco(atividade, archive["atividades"])
            atualizaEndereco(atividade, archive[atividade.categoria])
        else:
            if self.email in listaComentarios:
                print("voce ja fez um comentario nessa atividade!")
            else:
                atividade.comentario.append(comentarioAtual)
                atividade.nota.append(nota)
                atualizaEndereco(atividade, archive["atividades"])
                atualizaEndereco(atividade, archive[atividade.categoria])
class Comentario:
  def __init__(self, usuario_c, atividade_c, texto, nota, imagem):
    self.usuario_c = usuario_c
    self.atividade_c = atividade_c
    self.texto = texto
    self.nota = nota
    self.imagem = imagem

class Atividade:
    def __init__(self, idd, imagem,  nome, nota, descricao, duracaoAtividade, tags, servicos, localizacao, comentario, categoria):
        self.idd = idd
        self.imagem = imagem
        self.nome = nome
        self.nota = nota
        self.descricao = descricao
        self.duracaoAtividade = duracaoAtividade
        self.tags = tags
        self.servicos = servicos
        self.localizacao = localizacao
        self.comentario = comentario
        self.categoria = categoria

    def calculaNota(self):
        return round((sum(self.nota)/len(self.nota))) * "*"

    def calculaNotaInt(self):
        return round((sum(self.nota)/len(self.nota)))

    def verComentarios(self):
        if not self.comentario:
            print("Esta publicacão ainda não tem avaliações.\n")
        else:
            print("\n","-"*30,"\n")
            for comentarioUsuario in self.comentario:
                avaliacao = comentarioUsuario.nota * "*"
                print(f"{comentarioUsuario.usuario_c.nome}\t{avaliacao}\n")
                print(f"{comentarioUsuario.texto}\n{comentarioUsuario.imagem}")
                print("\n","-"*30,"\n")

def verAtividades(atividades, todasAtividades, filtros):
  while True:
    print("------------------------\n")
    for i in range(len(atividades)):
      print(f"{atividades[i].nome} - {atividades[i].calculaNota()}")
      print()
      print(atividades[i].imagem)
      print(f"Categoria: {atividades[i].categoria}")
      print(f"Tags: {atividades[i].tags}")
      print()
      print(f"Digite [{i+1}] para ver informações mais detalhadas")
      print("\n------------------------\n")
    print("----- MENU ---- ")
    print("[-1] Pesquisar")
    print("[-2] Aplicar Filtros")
    print("[-3] Abrir Navbar")
    print("[0] Retornar para a Home")
    toDo = int(input("Digite o número da atividade que deseja ver informações mais detalhadas: "))
    print()
    if toDo > 0:
      visualizarAtividade(atividades[toDo-1], todasAtividades)
    elif toDo == 0: 
      break
    elif toDo == -1:
      pesquisa = input()
      verAtividades(pesquisar(pesquisa, todasAtividades), todasAtividades, filtros)
    elif toDo == -2:
      verAtividades(filtrar(filtros, atividades), todasAtividades, filtros)
    elif toDo == -3:
      navBar()

def visualizarAtividade(visualizar, todasAtividades):
  
  global usuarioAtual
  while True:
    print("-----------------------------------------\n")  
    print(f"{visualizar.nome} - {visualizar.calculaNota()}")  
    print()        
    print(visualizar.localizacao)
    print()
    print(visualizar.imagem)
    print("Descrição: ", visualizar.descricao)
    for tag in visualizar.tags:    
        print(f"{tag}", end=" ")
    print("\n\n--------- AVALIAÇÕES ---------")
    visualizar.verComentarios()
    print("---- MENU ----")
    print("[ 0] - Voltar")
    print("[-1] - Pesquisar")
    print("[-2] - Fazer Comentário")
    print("[-3] - Adicionar ao Roteiro")
    print("[-4] - Curtir atividade")
    print("[-5] - Abrir Navbar")
    toDo = int(input())
    if toDo == 0:
      break
    if toDo == -1:
      pesquisa = input()
      verAtividades(pesquisar(pesquisa, todasAtividades), todasAtividades, [''])
    if toDo == -2:
      if not usuarioAtual:
        verPerfil()
      else:
        
        avaliacao = input(f"Digite aqui sua avaliação para {visualizar.nome}.\n")
        while avaliacao == "":
          print("Digite uma avaliação.")
          avaliacao = input(f"Digite aqui sua avaliação para {visualizar.nome}\n.")
        nota = int(input("Digite sua nota de 0 a 5. Apenas números inteiros.\n"))
        while nota < 0 or nota > 5:
          print("A nota que voce digitou é inválida.")
          nota = int(input("Digite sua nota de 0 a 5. Apenas números inteiros.\n"))
        imagem = input("Poste sua imagem.\n")
        usuarioAtual.fazComentario(visualizar, avaliacao, nota, imagem)
        
    if toDo == -3:
      if not usuarioAtual:
        verPerfil()
      else:
        usuarioAtual.adicionarAtividadeRoteiro(visualizar)
        print("\n\n\nFoi adicionado ao seu roteiro.\n")
    if toDo == -4:
      if not usuarioAtual:
        verPerfil()
      else:
        usuarioAtual.curtir(visualizar)
        
    if toDo == -5:
      navBar()
    
def navBar():
  
  global usuarioAtual
  while True:
    print("\n----- NAVBAR ----")
    print("[0] - Voltar")
    print("[1] - Home")
    print("[2] - Aba de Meus Roteiros")
    print("[3] - Atividades Curtidas")
    print("[4] - Aba de Meu Perfil")
    goTo = int(input())
    if goTo == 0:
      break
    if goTo == 1:
      #main()
      pass
    if goTo == 2:
      if not usuarioAtual:
        verPerfil()
      else:
        usuarioAtual.verRoteiros()
    if goTo == 3:
      if not usuarioAtual:
        verPerfil()
      else:
        usuarioAtual.verCurtidas()
    if goTo == 4:
      verPerfil()
    
def pesquisar(pesquisa, atividades):
  
  atividadesFiltradas = []
  if(type(pesquisa) == str):
    for atividade in atividades:
      if pesquisa.lower() == atividade.nome.lower():
        atividadesFiltradas.append(atividade)
      for tag in atividade.tags:
        if tag.lower() == pesquisa.lower():
          atividadesFiltradas.append(atividade)
    if len(atividadesFiltradas) == 0:
      print("Opa! Não encontramos nada relacionado.")
    return atividadesFiltradas
  else:
    for item in pesquisa:
      for atividade in atividades:
        for tag in atividade.tags:
          if tag.lower() == item.lower() and atividade not in atividadesFiltradas:
            atividadesFiltradas.append(atividade)
    if len(atividadesFiltradas) == 0:
      print("Opa! Não encontramos nada relacionado.")
    return atividadesFiltradas

def verPerfil(): 
  global logado
  global usuarioAtual
  global archive
  archive["usuarios"]
  while True:
    if logado == False:
      print( "\n----- MENU SIGN IN OU LOGIN -----")
      print("[1] - Você já possui uma conta?")
      print("[2] - Quer criar a sua conta?")
      conta = int(input("Digite: "))
      if conta == 1:
        login = input("Digite Seu email: ")
        senha = input("Digite sua senha: ")
        for usuario in archive["usuarios"]:
          if usuario.email == login and usuario.senha == senha:
            logado = True
            usuarioAtual = usuario
      else:

        usuarioAtual = Usuario.criaUsusario()
        while usuarioAtual == None:
            usuarioAtual = Usuario.criaUsusario()
        logado = True
        archive["usuarios"].append(usuarioAtual)
        saveData(archive)
        archive = loadData()
    if logado == True:
      # print(usuarioAtual.nome)
      # print(usuarioAtual.email)
      # print(usuarioAtual.senha)
      print("\n ---- MENU ----\n")
      print("[2] - Deslogar.")
      print("[1] - Editar perfil.")
      print("[0] - Voltar para onde estava.")
      goTo = int(input())
      if goTo == 0:
        break
      if goTo == 1:
        novoNome = input("digite seu Nome: ")
        novoEmail = input("Digite seu novo email: ")
        novaSenha = input("digite sua novaSenha: ")
        usuarioAtual.nome = novoNome
        usuarioAtual.email = novoEmail
        usuarioAtual.senha = novaSenha
        
        atualizaEndereco(usuarioAtual, archive["usuarios"])
      if goTo == 2:
        usuarioAtual = None
        logado = False

def filtrar(filtros, atividades):
    filtrosEscolhidos = []
    print("Selecione o(s) filtro(s) que você deseja aplicar: ")
    for i in range(len(filtros)):
        print(f"[{i+1}] - {filtros[i]}")
    for i in range(2):
        valorEscolhido = int(input())
        if(valorEscolhido == 0):  
            break
        filtrosEscolhidos.append(filtros[valorEscolhido-1])
    teste = pesquisar(filtrosEscolhidos, atividades)
    return teste


def todasTags(atividades):
    filtros = []
    for atividade in atividades:
        for filtro in atividade.tags:
            if filtro not in filtros:
                filtros.append(filtro)
            else:
                pass
    return filtros


def bubbleSort(array):
  for i in range(len(array)):
    swapped = False
    for j in range(0, len(array) - i - 1):
      if array[j].calculaNotaInt() < array[j + 1].calculaNotaInt():
        temp = array[j]
        array[j] = array[j+1]
        array[j+1] = temp
        swapped = True
    if not swapped:
      break	
  return array


def escolherPasseio(passeios):
    
    print("\nEscolha o passeio que você quer ver: ")
    print("[-1] - Filtrar passeios")
    print("[ 0] - Para voltar para as opções de passeios")
    for i in range(len(passeios)):
        print(f"[{i+1}] - {passeios[i]}")
    valorEscolhido = int(input())
    print(passeios[i].nome)
    if(valorEscolhido == 0):  
        main()
    if valorEscolhido == -1:
        filtrar()   

def bemAvaliadas(atividades):
    atividadesFiltradas = []
    filtrado = bubbleSort(atividades)
    for atividade in filtrado:
        if atividade.calculaNotaInt() > 3:
            atividadesFiltradas.append(atividade)
    return atividadesFiltradas


def perguntaGastronomica():
    print("\nVocê prefere uma experiência: ")
    print("[1] - Intimista, como um Bistrô.")
    print("[2] - Animada, como um bar.")
    print("[3] - Algo rápido, como Fast Food.")
    print("[4] - Um ambiente familiar, como um restaurante.")
    int(input("Digite: "))
    

def perguntaCultural():
    print("\nEm relação à cultura, você prefere uma experiência: ")
    print("[1] - Mais artesanal, como uma feira.")
    print("[2] - Mais performático, como um concerto ou show.")
    print("[3] - Lugares que contam um pouco da história da região alagoense, como Museus e centros históricos.")
    int(input("Digite: "))

     
    
def perguntaNatureza():
    print("\nEm relação ao contato com a natureza, você prefere uma experiência: ")
    print("[1] - Desbravadora como uma trilha.")
    print("[2] - Relaxante, como uma praia.")
    print("[3] - Que permita observar a fauna maceioense e brasileira, como um zoológico.")
    int(input("Digite: "))
    

def perguntaFamilia():
    print("Em relação à viagem com a família, você prefere uma experiência: ")
    print("Algo relaxante, como passar o dia na praia.")
    print("Algo divertido, como ir a um parque aquático.")
    print("Algo aventureiro, como ir em uma trilha com cachoeira.")
    int(input("Digite: "))
    


def perguntaRomantica():
    print("\nEm relação ao romance, você prefere uma experiência: ")
    print("[1] - Algo mais intimista, como um jantar à luz de velas.")  
    print("[2] - Algo mais aventureiro, como um passeio de caiaque à dois.")
    int(input("Digite:"))
     
def retornarAtividadesQuiz(tag, todasAtividades):
  while True:
    listaAtividades = []
    for atv in todasAtividades:
      if tag in atv.tags:
        listaAtividades.append(atv)
    return listaAtividades
        
      
  
def menuSeleciona(atividades):
  while True:
    print("\n--- ATIVIDADES IDEAIS PARA VOCÊ ---")
    print("-------------------------------------\n")
    print("Selecione a atividade que deseja adicionar ao seu roteiro \n")  
    print("-------------------------------\n")  
    for i in range(len(atividades)):
      print(f"{atividades[i].nome} - {atividades[i].calculaNota()}")
      print()
      print(atividades[i].imagem)
      print(f"Tags: {atividades[i].tags}\n")
      print(f"Categoria: {atividades[i].categoria}")
      print(f"\nDigite [{i+1}] para adicionar essa atividade ao seu roteiro!")
      print("\n------------------------\n")
    print("[0] Para retornar para Home")
    atividadeSel = int(input("Digite o número da atividade escolhida: "))
    if atividadeSel > 0:
      return atividades[atividadeSel-1]
    elif atividadeSel == 0:
      break

def menuSelecionaRoteiro(roteiros):
  global usuarioAtual
  cont = 1
  while True:
    print("\n------  ROTEIROS PRONTOS -------")
    print("----------------------------------\n")
    print("Escolha um roteiro para sua viagem! \n")
    print("--------------------------\n")   
    for roteiro in roteiros:
      for atividade in roteiro:
        print(f"{atividade.nome} - {atividade.calculaNota()}")
        print()
        print(atividade.imagem)
        print(f"Categoria: {atividade.categoria}\n")
      print(f"\nDigite [{cont}] para adicionar este roteiro a aba de meus roteiros.\n")
      print("------------------------\n")
      cont+=1
    print("[0] Para retornar para Home")
    selecionaRoteiro = int(input("Digite o número do roteiro selecionado: "))
    if selecionaRoteiro > 0:
      if not usuarioAtual:
        verPerfil()

      usuarioAtual.adicionarAtividadeRoteiro(roteiros[selecionaRoteiro-1])
      print("Este roteiro foi adicionado à aba de Meus Roteiros")
      break
    elif selecionaRoteiro == 0:
      break


def quiz():
    global archive
    global usuarioAtual
    listaResposta = []
    while True:
      while True:
        resposta = int(input("\nSelecione as experiências que você quer na sua viagem: \n" +
              "[1]  - Gastronômico \n" +
              "[2]  - Natureza \n" +
              "[3]  - Famila \n" +
              "[4]  - Romântico \n" +
              "[5]  - Cultural \n" +
              "[0]  - Caso não deseje mais nenhuma outra opção, digite 0 para ir para a próxima pergunta.\n" +
              "Digite: "))
        if resposta != 0:
          if resposta not in listaResposta:
            listaResposta.append(resposta)
          else:
            print("Categoria ja selecionada!")
        else: 
          break
      
      roteiroQuiz = []
      for opcao in listaResposta:
        if opcao == 1:
            perguntaGastronomica()
            roteiroQuiz.append(menuSeleciona(retornarAtividadesQuiz("Restaurantes", archive["atividades"])))
        elif opcao == 2:
            perguntaNatureza()
            roteiroQuiz.append(menuSeleciona(retornarAtividadesQuiz("Natureza", archive["atividades"])))
        elif opcao == 3:
            perguntaFamilia()
            roteiroQuiz.append(menuSeleciona(retornarAtividadesQuiz("Bom para crianças", archive["atividades"])))
        elif opcao == 4:
            perguntaRomantica()
            roteiroQuiz.append(menuSeleciona(retornarAtividadesQuiz("Cultural", archive["atividades"])))
        elif opcao == 5:
            perguntaCultural()
            roteiroQuiz.append(menuSeleciona(retornarAtividadesQuiz("Para casais", archive["atividades"])))
        
        
      print("Roteiro personalizado:")
      for atvRoteiro in roteiroQuiz:
        print(atvRoteiro.nome)
      print()
        
      selecao = int(input("adicionar roteiro? \n[1] - sim \n[2] - não\n"))
      if selecao == 1:
        if not usuarioAtual:
          verPerfil()
       
        usuarioAtual.adicionarAtividadeRoteiro(roteiroQuiz)
        print("roteiro adicionado aos meus roteiros")
        break
      
      else:
        break
      

def main():
    
    global logado
    global usuarioAtual
    global archive
    while True:
        print(" __      __                                     ")
        print(" \ \    / /                                     ")
        print("  \ \  / /__  _   _  __ _  __ _  ___ _   _ _ __ ")
        print("   \ \/ / _ \| | | |/ _` |/ _` |/ _ \ | | | '__|")
        print("    \  / (_) | |_| | (_| | (_| |  __/ |_| | |   ")
        print("     \/ \___/ \__, |\__,_|\__, |\___|\__,_|_|   ")
        print("               __/ |       __/ |                ")
        print("              |___/       |___/                 ")
        print("-- MENU INICIAL --")
        print("[0] - SAIR")
        print("[1] - PESQUISAR")
        print("[2] - QUIZ")
        print("[4] - ROTEIROS PRONTOS")
        print("[5] - PASSEIOS")
        print("[6] - RESTAURANTES")
        print("[7] - PRAIAS")
        print("[8] - ATIVIDADES BEM AVALIADAS")
        print("[10] - ABRIR NAVBAR")
        select = int(input("Escolha sua opção: "))
        if select == 0:
            break
        if select == 1:
            pesquisa = input("Digite o que deseja pesquisar (Como tags ou o nome da atividade): ")
            verAtividades(pesquisar(pesquisa, archive["atividades"]), archive["atividades"], todasTags(archive["atividades"]))
        if select == 2:
            quiz()
        if select == 4:
            menuSelecionaRoteiro(archive["roteiros"])
        if select == 5:
            verAtividades(archive["passeios"], archive["atividades"], todasTags(archive["passeios"]))
        if select == 6:
            verAtividades(archive["restaurantes"], archive["atividades"], todasTags(archive["restaurantes"]))
        if select == 7:
            verAtividades(archive["praias"], archive["atividades"], todasTags(archive["praias"]))
        if select == 8:
            verAtividades(bemAvaliadas(archive["atividades"]), archive["atividades"], todasTags(archive["atividades"]))
        if select == 10:
            navBar()
        if select == 11:
          saveData(archive)
          archive = loadData()

  
# passeioMaragogi = Atividade( 1, "imagem passeio Maragogi",  "Passeio à maragogi", [5, 4, 3], "Saindo de maceió, ao norte, você visitará piscinas naturais", "9h", ["Bom para crianças","Natureza","Praia","Pet friendly", "Bom para idosos"], ["Catamarã", "Apoio no Restaurante pontal do maragogi"], "Pontal do Maragogi, Rodovia AL 101 Norte, Km 130 s/n Burgalhau - Barra Grande, Maragogi - AL, 57799-000, Brazil", [], "passeios")
# passeioMarape = Atividade(2, "imagem passeio Marapé",  "Passeio às Dunas de Marapé", [5, 4, 3], "Paraíso ecológico formado entre a Praia de Duas Barras e o Rio Jequiá. Além disso, pode também visualizar falésias.", "7h", ["Natureza","Aventura"], ["passeio de buggy", "Barraquinha","Day-use", "Circuito Pau-de-Arara", "Trilha dos Caetés"], "Povoado Barra de Jequia SN Duas Barras - Jequiá da Praia - Litoral Sul de Alagoas - 50 min de Maceió, Jequiá da Praia, Alagoas 57244-000 Brasil", [], "passeios")
# passeioHibiscus = Atividade(3, "imagem passeio Hibiscus",  "Passeio à ipipoca no Hibiscus beach club", [5, 4, 3], "Ida a praia de IPIOCA pra aproveitar um dia relaxante no beach club.", "3h30", ["Relaxante","Para casais","Bom para crianças","Natureza","Praia"], ["Passeios Náuticos", "Massagem relaxante","Área HIBISQUINHO para crianças","Passeio de lancha, Stand-up paddling e Caiaque"], "Rodovia AL 101 Norte, Bairro Ipioca Residencial Angra de Ipioca, Maceió, Alagoas 57039-705 Brasil", [], "passeios")
# resturanteJanga = Atividade(4, "imagem peixe frito", "Resturante Janga Praia", [4,4,5], " Restaurante em Maceió de comida Brasileira e de Frutos do mar, que tem opções vegetarianas", "1h", ["Restaurantes", "Bom para criança", "Para casais", "Bom para idoso", "Relaxante"], [],"Avenida Silvio Carlos Viana 1731 Ponta Verde, Maceió, Alagoas 57035-160 Brasil",[], "restaurantes")
# resturanteMaria = Atividade(5, "imagem prato italiano e taça de vinho", "Resturante Maria Antonieta", [5,4,2], " Restaurante em Maceió de comida Italiana, Frutos do mar e Grelhados", "1h30", ["Restaurantes", "Para casais", "Bom para idoso", "Cultural"], [], "Avenida Doutor Antônio Gomes de Barros 150 Jatiuca, Maceió, Alagoas 57036-000 Brasil",[], "restaurantes")
# resturanteWanchako = Atividade(6, "imagem de ceviche", "Resturante Wanchako", [4,4,4], " Restaurante em Maceió de comida Peruana, Latina e de Frutos do mar", "1h30", ["Restaurantes", "Para casais", "Bom para idoso", "Cultural"], []," Rua São Francisco de Assis, 93 Jatiúca, Maceió, Alagoas 57045-690 Brasil",[], "restaurantes")
# praiaDeIpioca = Atividade( 7, "imagem praia de Ipioca",  "Praia de Ipioca", [5, 5, 5], "Praia ao sul de Maceió, meio deserta e de águas calmas", "3h", ["Bom para crianças","Natureza","Praia","Pet friendly", "Só para casais"], ["Passeio de bike", "Passeio de jangada"], "AL-101 rua Antônio Sabino de Sá 251, Maceió, Alagoas 57039-705 Brasil",[], "praias")
# praiaDoGunga = Atividade( 8, "imagem do Mirante do Gunga",  "Praia do Gunga", [2, 4, 3], "Praia ao norte de Maceió, bem turistica e movimentada, com muitos coqueirinhos", "5h", ["Bom para crianças","Natureza","Praia","Pet friendly", "Só para casais", "Bom para Idoso", "Aventura"], ["Passeio de Quadriciclo", "Passeio de jangada"], "Praia do Gunga, AL",[], "praias")
# praiaDoFrances = Atividade( 9, "imagem praia do Francês",  "Praia do Francês", [4, 4, 3], "Praia ao norte de Maceió, bem turistica e relaxante", "4h", ["Bom para crianças","Natureza","Praia","Pet friendly", "Só para casais", "Bom para Idoso"], ["Aluguel de Stand up"], "Praia do Francês, Marechal Deodoro, Alagoas", [], "praias")

# usuarios = []
# arrayUsuarios = usuarios
# arrayAtividades = [passeioMaragogi, passeioHibiscus, passeioMarape, resturanteJanga, resturanteMaria, resturanteWanchako, praiaDeIpioca, praiaDoFrances, praiaDoGunga]
# arrayPasseios = [passeioMaragogi, passeioMarape, passeioHibiscus]
# arrayPraias = [praiaDeIpioca, praiaDoFrances, praiaDoGunga]
# arrayRestaurantes = [resturanteJanga, resturanteMaria, resturanteWanchako]
# listTudo = [usuarios, arrayAtividades, arrayPasseios, arrayPraias, arrayRestaurantes]
# arrayRoteiros = [[passeioMaragogi, praiaDeIpioca,resturanteJanga],[passeioMarape,praiaDoFrances,resturanteMaria],[passeioHibiscus,praiaDoGunga,resturanteWanchako]]
# dictTudo = {
#     "usuarios" : arrayUsuarios, 
#     "atividades" : arrayAtividades,
#     "passeios" : arrayPasseios,
#     "praias" : arrayPraias,
#     "restaurantes" : arrayRestaurantes,
#     "roteiros":  arrayRoteiros
# }
# saveData(dictTudo)


archive = loadData()

'''
archive["usuarios"].clear()
saveData(archive)
'''
'''usuarios = archive["usuarios"]
passeios = archive["passeios"]
praias = archive["praias"]
restaurantes = archive["restaurantes"]
atividades = archive["atividades"]'''
print("............................................................... ...................................")
print("............................... ............................... ............................... ...")
print("............................................................... ...................................")
print("............... ............... ............... ............... ............... ............... ...")
print("............................................................... ...................................")
print("............................... ............................... ...................//*......... ...")
print("......................................,,*********,,,........... ................,*////*,...........")
print("....... ....... .....,*///*,....*////////////////////////*..... ....... ......*///////////,.... ...")
print("....................*////////////////////////////////////////*....................*///,............")
print("....................*///////////////////////////////////////////*..................*/,...,//*,. ...")
print("....................*//////////////////////////////////////////////,....................*/////,....")
print("............... ....,///////////////////////////////////////////////*.......... ..........,*... ...")
print("...................*//////////////////////////////////////////////////*............................")
print("..................*////////////////////////////////////////////////////*....................... ...")
print(".................*//////////////////////////////////////////////////////*..........................")
print("... ... ... ... ,////////////////////////////////////////////////////////,. ... ... ... ... ... ...")
print("................,////////////////////////////////////////////////////////,.........................")
print("................,////////////////////////(((((((////////////((///////////,..................... ...")
print("................,////////////////////////////(%%%(////////(%%(///////////,.........................")
print("............... ,/////////////////////////(%%%(/(%%%%%%%%%#//////////////,..... ............... ...")
print("................,////////////////////////////////////////////////////////,.........................")
print(" .................,///////////////////////////////////////////////////////,..................... ..")
print("..................,//////////////////////////////////////////////////////,.........................")
print("....... ....... ...,/////////////////////////////////////////////////////,..... ....... ....... ...")
print(".....................///////////////////////////////////////////////////,..........................")
print("...........**........../////////////////////////////////////////////////,..................... ....")
print("..........///,..........,////////////////////////////////////*/////////,...........................")
print("........,*/////,,................,**//////////////////**,......,/////////..........................")
print("..........,//*....*/,.......... ................................*///////*...................... ...")
print("...............,///////........................................ ..,***,............................")
print(". . . . . . . . ..*/*.. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .")
print("............................................................... ...................................")
print("............................... ............................... ............................... ...")
print("............................................................... ...................................")
print("............... ............... ............... ............... ............... ............... ...")
print("............................................................... ...................................")
main()