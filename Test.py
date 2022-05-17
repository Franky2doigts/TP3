from sqlite3 import paramstyle
import hou

def init(par):
  
    # Pour nous aider à avoir des suggestions dans vscode
    parent:hou.Node = par
    # On va chercher le groupe de l'interface
    g:hou.ParmTemplateGroup =  parent.parmTemplateGroup()
    # Si l'interface ne contient pas le bouton on l'ajoute
    if g.find("test") == None:
        # On créer le bouton 
        p:hou.ButtonParmTemplate = hou.ButtonParmTemplate("test","This is a button")
        # On assigne la fonction update a appeler lorsque le bouton est clicker
        p.setScriptCallback("hou.pwd().hm().update()")
        p.setScriptCallbackLanguage(hou.scriptLanguage.Python)
        # On ajoute le bouton après le menu scripts
        g.append(p)
    if g.find("multi") == None:
        # On creer un multiparm a utiliser
        folder:hou.FolderParmTemplate = hou.FolderParmTemplate("multi","Positions",folder_type=hou.folderType.MultiparmBlock)
        # On creer le type de parm que le multiparm va ajouter
        vec3:hou.FloatParmTemplate = hou.FloatParmTemplate("posf","position",3,naming_scheme=hou.parmNamingScheme.XYZW)
        # On ajoute le type de parm au multiparm
        folder.addParmTemplate(vec3)
        # On ajoute le multiparm après le bouton
        g.append(folder)
    # On met à jour l'interface
    parent.setParmTemplateGroup(g)

def deinit(par):
    # On crée la node Point dans le hda
    parent:hou.Node = par
    multiparm:hou.Parm = parent.parm("multi")
    # Créer une node par nombre de point ajouté 
    if multiparm != None: 
        #boucle pour parcourir la liste des parametres
        for i in range(0,multiparm.multiParmInstancesCount()):
            attribexpressionSop:hou.SopNode = parent.createNode("attribexpression")
            # On change le paramètre VEXpression à value constant
            snippet1:hou.Parm = attribexpressionSop.parm("snippet1")
            snippet1.set("value")

        instances = multiparm.multiParmInstances()
        count = 1
        # boucle for pour parcourir les paramètres
        for x in instances:
            # définir la variable parm
            parametre:hou.Parm = x
            # adapté les valeurs a la bonne node
            n:hou.Node = parent.node("attribexpression"+str(count))
            value = x.eval()

            # vérifie l'information et cherche le caractère x et on compare à -1 si le x est trouvé ou non
            if parametre.name().find("x") > -1:
                xp = n.parm("valv3_1x")
                # donner une valeur à la variable xp
                xp.set(value)
            
            if n.name().find("y") > -1:
                yp = n.parm("valv3_1y")
                # donner une valeur à la variable yp
                yp.set(value)
            
            # vérifie l'information et cherche le caractère z et on compare à -1 si le z est trouvé ou non
            if parametre.name().find("z") > -1:
                zp = n.parm("valv3_1z")
                # donner une valeur à la variable zp
                zp.set(value)   
                                            
                # ajoute 1 à la variable à gauche
                count+=1

    



    #multi.append(parm.eval())    
    # print(instances)
    # multi = []
    # for x in instances:
    #     parm:hou.Parm = x

    # data = {
    #     "points":[]
    # }


    g:hou.ParmTemplateGroup =  parent.parmTemplateGroup()
    test:hou.ParmTemplate = g.find("test")
    multi:hou.ParmTemplate = g.find("multi")
    # Si test et/ou multi existe, on les enlève vu que nous serons un autre script
    if  test != None:
        g.remove(test)
    if multi != None:
        g.remove(multi)
    parent.setParmTemplateGroup(g)

def update():
    print("")

   