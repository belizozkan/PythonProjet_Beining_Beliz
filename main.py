from xml_conll import xml_conll
from process import process
import os

'''Les utilisateurs peuvent personnaliser le processeur ici.'''
lemma_tool="spacy"
lemma_model="fr_core_news_sm"
pos_tool="stanza"
pos_model="standard"
fea_tool="stanza"
fea_model="standard"
depparse_tool="udpipe"
depparse_model="french-gsd-ud-2.5-191206.udpipe"
langue="fr"
processors={ 
"language":langue,
"lemma": {
        "tool":lemma_tool,
        "model":lemma_model
},
"pos": {
        "tool":pos_tool,
        "model":pos_model
},
"fea": {
        "tool":fea_tool,
        "model":fea_model
},
"depparse": {
        "tool":depparse_tool,
        "model":depparse_model
}
}
print("Votre processeur est:"+str(processors))


'''Nous obtenons le chemin absolu du fichier actuel, de sorte qu'il est plus facile d'obtenir le fichier plus tard.'''
current_file_path = os.path.abspath(__file__)
current_folder_path = os.path.dirname(current_file_path)

''' Fonction pour traiter un fichier d'entrée en utilisant différents outils et créer un dictionnaire de tokens'''
def process_dict(input_file, chosen_tools):
    try:
        # Instancier un objet 'process'
        wrapper = process()
        model_path = os.path.join(current_folder_path, 'french-gsd-ud-2.5-191206.udpipe')
        # Appeler différentes méthodes de traitement sur le fichier d'entrée
        results_stanza = wrapper.process_stanza(input_file)
        print(results_stanza)
        results_spacy = wrapper.process_spacy(input_file, lemma_model)
        print(results_spacy)
        results_udpipe = wrapper.process_udpipe(input_file, model_path)
        print(results_udpipe)

        # Liste pour stocker les tokens choisis
        chosen_tokens = []
        for stanza_token, spacy_token, udpipe_token in zip(results_stanza, results_spacy, results_udpipe):
            chosen_token = {
                'ID': stanza_token['ID'],
                'FORM': stanza_token['FORM'],
            }
            for key, tool in chosen_tools.items():
                chosen_token[key] = (
                    stanza_token[key] if tool == 'stanza' else (
                        spacy_token[key] if tool == 'spacy' else udpipe_token[key])
                )
                # Si DEPREL est présent dans chosen_tools, ajoutez également la partie HEAD
                if key == 'DEPREL':
                    chosen_token['HEAD'] = (
                        stanza_token['HEAD'] if tool == 'stanza' else (
                            spacy_token['HEAD'] if tool == 'spacy' else udpipe_token['HEAD'])
                    )
            chosen_tokens.append(chosen_token)

        return chosen_tokens
    except Exception as e:
        print(f"Erreur lors du traitement des données : {str(e)}")
        return []


''' Fonction pour convertir un dictionnaire de token en ligne au format CoNLL-U.'''
def dict_to_conllu_line(token_dict):
    try:
        # Définir les colonnes pour le format CoNLL-U
        columns = ['ID', 'FORM', 'LEMMA', 'POS', '_', 'FEA', '_', 'HEAD', 'DEPREL', '_']

        conllu_line = []
        # Parcourir chaque colonne et ajouter la valeur correspondante du dictionnaire de token à la ligne CoNLL-U
        for column in columns:
            if column in token_dict and token_dict[column] is not None:
                conllu_line.append(str(token_dict[column]))
            else:
                conllu_line.append('_')
        # Convertir la liste en une chaîne et la renvoyer
        return '\t'.join(conllu_line)
    except Exception as e:
        print(f"Erreur lors de la conversion du dictionnaire de token en ligne au format CoNLL-U : {str(e)}")
        return None


''' Fonction pour convertir une liste de dictionnaires de tokens en une phrase au format CoNLL-U.'''
def dicts_to_conllu_sentence(dicts_list):
    try:
        conllu_sentence = []
        for token_dict in dicts_list:
            conllu_line = dict_to_conllu_line(token_dict)
            if conllu_line is not None:
                conllu_sentence.append(conllu_line)
        return '\n'.join(conllu_sentence)
    except Exception as e:
        print(f"Erreur lors de la conversion de la liste de dictionnaires de tokens en phrase au format CoNLL-U : {str(e)}")
        return None

'''Fonction pour écrire des informations telles que le décalage dans un nouveau fichier'''    
def write_offset(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f_source:
            source_lines = f_source.readlines()

        with open(output_file, 'r', encoding='utf-8') as f_target:
            target_lines = f_target.readlines()

        new_target_lines = []
        for source_line, target_line in zip(source_lines, target_lines):
            last_tab_content = source_line[source_line.rfind('\t'):]
            new_target_line = target_line.strip() + last_tab_content
            new_target_lines.append(new_target_line)

        with open(output_file, 'w', encoding='utf-8') as f_target:
            f_target.writelines(new_target_lines)
    except Exception as e:
        print(f"Erreur lors de l'écriture des décalages dans le fichier de sortie : {str(e)}")


def main():
    try:
        ''' Exemple pour tester la fonction XML en utilisant cette formule XPATH => "./{*}parent/{*}version"'''
        input_conll = os.path.join(current_folder_path, 'input_files/input_xml.xml')
        xml = xml_conll()
        xml.xml_to_conllu(input_conll, os.path.join(current_folder_path, 'output_files/output_xml_to_conllu.txt'), "./{*}parent/{*}version")

        input = os.path.join(current_folder_path, 'input_files/input_conllu.txt')
        output = os.path.join(current_folder_path, 'output_files/output_nlp.txt')

        '''Les utilisateurs peuvent personnaliser une seule exigence, ou deux, trois ou quatre. Par exemple, vous pouvez essayer d'ajouter simplement trois colonnes'''
        '''chosen_tools = {
            'LEMMA': 'spacy',
            'POS': 'stanza',
            'FEA': 'stanza',
        }'''
        chosen_tools = {
            'LEMMA': 'spacy',
            'POS': 'stanza',
            'FEA': 'stanza',
            'DEPREL': 'udpipe',
        }

        with open(output, 'w', encoding='utf-8') as f:
            f.write(dicts_to_conllu_sentence(process_dict(input, chosen_tools)) + '\n\n')
        write_offset(input, output)
    except Exception as e:
        print(f"Erreur lors de l'exécution de la fonction principale : {str(e)}")

if __name__ == "__main__":
    main()
