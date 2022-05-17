import hou
import json


def init(par):
# Suggestions dans vscode
    parent:hou.Node = par
# Je vais chercher le groupe du template
    g:hou.ParmTemplateGroup =  parent.parmTemplateGroup()
# Je créer le bouton "This is a button" et je l'ajoute à l'interface

    if g.find("test") == None:
        p:hou.ButtonParmTemplate = hou.ButtonParmTemplate("test","This is a button")
        # On assigne la fonction update a appeler lorsque le bouton est clicker
        p.setScriptCallback("hou.pwd().hm().update()")
        p.setScriptCallbackLanguage(hou.scriptLanguage.Python)
# J'ajoute le bouton après le menu script
        g.append(p)
    if g.find("link") == None:
        # On creer un multiparm a utiliser
        link:hou.StringParmTemplate = hou.StringParmTemplate("link","chemin",1)
# J'ajoute le multiparm link après le bouton
        g.append(link)
#Mise à jour l'interface
    parent.setParmTemplateGroup(g)
def deinit(par):
    parent:hou.Node = par
    g:hou.ParmTemplateGroup =  parent.parmTemplateGroup()
    test:hou.ParmTemplate = g.find("test")
    link:hou.ParmTemplate = g.find("link")
#On créer une condition pour enlever test et/ou link
    if  test != None:
        g.remove(test)
    if link != None:
        g.remove(link)
    parent.setParmTemplateGroup(g)

def update():
    print("Update was called, do stuff here.")
#Je crée une liste au nom de data avec ces enfants ayant les valeurs en x,y,z sur la clé count
    parent:hou.Node = hou.pwd()
    data = {}
    count = 0
    for child in parent.children():
        point:hou.Node = child
        parmX = point.parm("valv3_1x")
        data[count] = []
        data[count].append(parmX.eval())

        parmY = point.parm("valv3_1y")
        data[count].append(parmY.eval())

        parmZ = point.parm("valv3_1z")
        data[count].append(parmZ.eval())



        count+=1
# Je fini avec le liens link et j'execute la fonction ce qui sera envoyer sur un fichier .json
    fullpath = parent.parm("link").eval()
    file = open(fullpath,"w")
    json.dump(data,file,indent=4)



        
    



        



