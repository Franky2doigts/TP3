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

def __add_sop_nodes(multiparm, parent):
# boucle pour parcourir la liste des parametres
    for i in range(0,multiparm.multiParmInstancesCount()):
        # creation d'une SopNode ayant le nom attribexpression
        attribexpressionSop:hou.SopNode = parent.createNode("attribexpression")
        # On change le paramètre VEXpression à value constant
        snippet1:hou.Parm = attribexpressionSop.parm("snippet1")
        snippet1.set("value")

def __define_value_in_instance(parent_node, parm_instance,instance_name, parm_name, value):
    # s'assurer que le nom de l'instance contient le nom du param
    if parm_instance.name().find(instance_name) > -1:
        # mettre la valeur dans le param ayant le chemin parm_name
        coord_param = parent_node.parm(parm_name)
        coord_param.set(value)
    return parm_instance.name().find(instance_name) > -1



def deinit(parent:hou.Node):
    # on cherche le parm ayant le chemin d'accès multi, la variable
    # est, alors, assignée à multiparm
    multiparm:hou.Parm = parent.parm("multi")
    # On vérifie que la variable multiparm n'est pas de type None 
    if multiparm is not None: 
        __add_sop_nodes(multiparm, parent)
        count = 1
        # boucle for pour parcourir les paramètres
        for x in multiparm.multiParmInstances():
            parm_instance:hou.Parm = x
            # adapté les valeurs a la bonne node
            curr_attribe_expression_node:hou.Node = parent.node("attribexpression"+str(count))
            value = parm_instance.eval() # recuperer la valeur dans le parm
            __define_value_in_instance(curr_attribe_expression_node, parm_instance, "x", "valv3_1x", value)
            __define_value_in_instance(curr_attribe_expression_node, parm_instance, "y", "valv3_1y", value)
            z_is_set = __define_value_in_instance(curr_attribe_expression_node, parm_instance, "z", "valv3_1z", value)                      
            if z_is_set:
                count+=1
    parm_template_group:hou.ParmTemplateGroup = parent.parmTemplateGroup()
    test_parm:hou.ParmTemplate = parm_template_group.find("test")
    # retirer les parm si ils sont presents
    if test_parm is not None:
        parm_template_group.remove(test_parm)
    multi_parm:hou.ParmTemplate = parm_template_group.find("multi")
    if multi_parm is not None:
        parm_template_group.remove(multi_parm)
    parent.setParmTemplateGroup(parm_template_group)

def update():
    print("updated!")