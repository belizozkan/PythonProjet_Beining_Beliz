import xml.etree.ElementTree as ET

class xml_conll:
    def tokenize(self, text:str)->list:
        # Tokenise le texte en une liste de tokens
        tokens=[]
        word=""
        punctuations=["'",",","?",";",".",":","!","(",")","\"","[","]"]
        # Parcourt chaque caractère du texte
        for (i,car) in enumerate(text+" "):
            if (car == " " or car in punctuations):
                if (word != "") :
                    if (car == '\'') :
                        word += car
                
                    tokens.append(word)
                    if car != " " and car != "'":
                        tokens.append(car)
                    word = ""
                else:
                    if car != " ":
                        tokens.append(car)
            else:
                # Ajoute un caractère de mot dans word
                word += car 
        return (tokens)

    def find_offset(self, tokens, data):
        # Utilise la liste des tokens pour trouver le décalage des tokens dans le fichier source, retourne le résultat
        res = [data.index(tokens[0])]
        index = len(tokens[0])
        # Parcourt la liste des tokens
        for i in range (1,len(tokens)):
            res.append(data.index(tokens[i],index))
            index+=len(tokens[i])
        return res
    
    """input_file in XML format ->  parsed -> tokenized -> formatted to CoNNLu like -> write the output file"""
    def xml_to_conllu(self, input_file, output_file, xpath_expression):
        # Le fichier d'entrée au format XML est analysé, tokenisé, formaté en CoNNLu et écrit dans le fichier de sortie
        parser = ET.XMLParser()
        xml = ET.parse(input_file,parser=parser)
        # Recherche l'élément XML à l'aide de l'expression XPath
        res = xml.find(xpath_expression)
        # Récupère le texte du fichier à l'aide de la formule XPATH en paramètre
        data_to_process = res.text
        # Calcule le décalage initial dans le fichier d'entrée
        start_nb = 0
        with open(input_file, 'r') as f:
            content = f.read()
            start_nb = content.index(data_to_process)
        print( "text = "+data_to_process)
        # Tokenisation du texte 
        tokens=self.tokenize(data_to_process)
        # Calcule le décalage pour chaque token dans le texte à traiter
        off=self.find_offset(tokens,data_to_process)   

        # Formate les données pour avoir le décalage et l'espace après chaque token
        i = 0
        j = 1
        res = []
        while  i < len(tokens):
            space=""
            if off[i]+len(tokens[i]) < len(data_to_process) and data_to_process[off[i]+len(tokens[i])] == " ":
                space =  "Offset="+str(off[i] + start_nb)
            else:
                space = "SpaceAfter=No|Offset=" + str(off[i] + start_nb)
            res.append((j, tokens[i],space))
            j+=1
            i+=1

        # Formatage de la sortie pour l'écrire au format CoNNLu dans le fichier
        coNNLu_file = "text = " + data_to_process.strip() + "\n"
        for i in res:
            line = str(i[0]) + '\t' + i[1] + '\t' + '_' + '\t' + '_' + '\t' + '_' + '\t' + '_' + '\t' + '_' + '\t' + '_' + '\t' + i[2] + '\n'
            coNNLu_file = coNNLu_file + line
        print(coNNLu_file)

        # Ecrire la sortie au format connlu
        with open(output_file, "w", encoding='utf-8') as fichier:
            fichier.write(coNNLu_file)
