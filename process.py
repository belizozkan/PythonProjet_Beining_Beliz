import stanza
import spacy
import ufal.udpipe
from conllu import parse
import urllib.request

class process():

    def process_stanza(self, input_file):
        try:
            # Initialise le pipeline Stanza pour la langue française
            nlp = stanza.Pipeline("fr")
            # Ouvre et lit le fichier d'entrée
            with open(input_file, 'r', encoding='utf-8') as f:
                data = f.read()
            # Analyse les données d'entrée en phrases    
            sentences = parse(data)
            # Initialise une liste vide pour stocker les résultats
            results = []
            # Parcourt chaque phrase
            for sentence in sentences:
                words = []
                # Parcourt chaque token de la phrase
                for token in sentence:
                    words.append(token['form'])
                # Effectue une analyse NLP sur la phrase
                doc = nlp(' '.join(words))
                # Parcourt chaque mot et token dans la phrase analysée
                for sentence in doc.sentences:
                    for word, token in zip(sentence.words, sentence.tokens):
                        results.append({
                            'ID': word.id,
                            'FORM': token.text,
                            'LEMMA': word.lemma,
                            'POS': word.pos,
                            'FEA': word.feats,
                            'HEAD':word.head,
                            'DEPREL': word.deprel
                        })
        except Exception as e:
            print(f"Erreur lors du traitement avec Stanza : {str(e)}")
            results = []

        # Retourne les résultats
        return results

    def process_spacy(self, input_file, model):
        try:
            # Charge le modèle de SpaCy
            nlp = spacy.load(model)
            # Ouvre et lit le fichier d'entrée
            with open(input_file, 'r', encoding='utf-8') as f:
                data = f.read()
            # Analyse les données d'entrée en phrases    
            sentences = parse(data)
            # Initialise une liste vide pour stocker les résultats
            results = []

            # Parcourt chaque phrase
            for sentence in sentences:
                words = []
                # Parcourt chaque token de la phrase
                for token in sentence:
                    words.append(token['form'])
                # Effectue une analyse NLP sur la phrase
                doc = nlp(' '.join(words))
                # Parcourt chaque token et token de SpaCy dans la phrase analysée
                for token, spacy_token in zip(sentence, doc):
                    results.append({
                        'ID': token['id'],
                        'FORM': token['form'],
                        'LEMMA': spacy_token.lemma_,
                        'POS': spacy_token.pos_,
                        'FEA': token['feats'],
                        'HEAD': spacy_token.head.i + 1,
                        'DEPREL': token['deprel']
                    })
        except Exception as e:
            print(f"Erreur lors du traitement avec SpaCy : {str(e)}")
            results = []

        # Retourne les résultats
        return results

    
    def process_udpipe(self, input_file, model_path): 
        url='https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-3131/french-partut-ud-2.5-191206.udpipe?sequence=38&isAllowed=y'
        urllib.request.urlretrieve(url,model_path)
        try:
            # Charge le modèle UDPipe       
            model = ufal.udpipe.Model.load(model_path)
            if not model:
                raise Exception("Impossible de charger le modèle à partir du chemin fourni.")
        except Exception as e:
            print("Une erreur s'est produite lors du chargement du modèle :", e)
            return

        # Initialise le pipeline UDPipe
        pipeline = ufal.udpipe.Pipeline(model, "tokenize", "tag", "parse", "conllu")

        try:
            # Ouvre et lit le fichier d'entrée
            with open(input_file, 'r', encoding='utf-8') as f:
                data = f.read()
        except Exception as e:
            print("Une erreur s'est produite lors de la lecture du fichier d'entrée :", e)
            return

        try:
            # Traite les données avec le pipeline UDPipe
            processed_data = pipeline.process(data)
            # Analyse les données traitées en phrases
            sentences = parse(processed_data)
        except Exception as e:
            print("Une erreur s'est produite lors du traitement avec UDPipe :", e)
            return

        # Initialise une liste vide pour stocker les résultats
        results = []

        try:
            # Parcourt chaque phrase
            for sentence in sentences:
                # Parcourt chaque token de la phrase
                for token in sentence:
                    results.append({
                        'ID': token['id'],
                        'FORM': token['form'],
                        'LEMMA': token['lemma'],
                        'POS': token['upostag'],
                        'FEA': token['feats'],
                        'HEAD':token['head'],
                        'DEPREL': token['deprel']
                    })
        except Exception as e:
            print("Une erreur s'est produite lors de l'analyse :", e)
            return

        # Retourne les résultats
        return results

