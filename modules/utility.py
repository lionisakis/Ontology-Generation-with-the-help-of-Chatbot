import modules.chatbotTalks as talk
import owlready2
from modules.dialogOptions import CheckDialog

def convertStringToLowerTittle(txt):
    # convert the name to lower with capital case
    labels=txt.split()
    theLabel=""
    for label in labels:
        if theLabel=="":
            theLabel=label.lower()
        else:
            theLabel=theLabel+"_"+label.title()
    return theLabel
    

def deleteData(ui,terms,relationships_others,ask=False):
    options=terms
    data=ui.data
    if ask==True and terms!=[]:
        options=[]
        for i in terms:
            options.append(talk.whatToDestroy(i))
        options=CheckDialog(ui,options,"Are you sure you want to delete this items?").run()
        for i in options:
            ui.addTextUser(i)
    for i in options:     
        i=i.split("\"")[1]        
        temp=list(data[0].keys())
        if i in temp:
            owlready2.destroy_entity(data[0][i][0])
            del data[0][i]
            for j in temp:
                if j in data[1].keys():
                    flag=False
                    for item in data[1][j][1]:
                        if item==i:
                            flag=True
                    if data[1][j][2]==i:
                        flag=True
                    if flag==True:
                        owlready2.destroy_entity(data[1][j][0])
                        del data[1][j]
            ui.RemoveTerm(i)

    options=relationships_others
    if ask==True and relationships_others!=[]:
        options=[]
        for i in relationships_others:
            options.append(talk.whatToDestroy(i))
        options=CheckDialog(ui,options,"Are you sure you want to delete this items?").run()
        for i in options:
            ui.addTextUser(i)


    for j in options:
        j=j.split("\"")[1]
        relation=j.split("_")
        if len(relation)!=3:
            continue
        if relation[1] in data[1].keys():
            owlready2.destroy_entity(data[1][relation[1]][0])
            del data[1][relation[1]]
            ui.RemoveRelationship(relation[1])
        else:
            ui.rememberOneTime("No \""+j+"\" was found.")
    
    ui.Menu()